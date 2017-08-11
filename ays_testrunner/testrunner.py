"""
Test runner module for AYS9
"""
from js9 import j
import os
import random
from redis import Redis
from rq import Queue
import logging
import time

AYS_CORE_BP_TESTS_PATH = j.sal.fs.joinPaths(j.sal.fs.getParent(j.sal.fs.getParent(__file__)), 'tests', 'bp_test_templates', 'core')
# AYS_DEFAULT_PLACEHOLDERS = ['G8_URL', 'G8_LOGIN', 'G8_ACCOUNT', 'G8_PASSWORD', 'G8_LOCATION']
AYS_TESTRUNNER_REPO_NAME = 'ays_testrunner'
AYS_TESTRUNNER_REPO_GIT = 'https://github.com/ahussein/ays_testrunner.git'
DEFAULT_TEST_TIMEOUT = 600 # 10 min timeout per test

def check_status_code(res, expected_status_code=200, logger=None):
    """
    Check if a response object has the expected status code

    returns (response object, True/False)
    """
    if logger is None:
        logger = j.logger.logging

    logger.debug('Validating response status code {} with expected status code {}'.format(res.status_code, expected_status_code))
    if res.status_code == expected_status_code:
        return res, True
    return res, False


def ensure_test_repo(cli, repo_name, logger=None):
    """
    Ensure a new repo for running tests is created with unique name
    """
    if logger is None:
        logger = j.logger.logging

    logger.debug('Ensuring test repo with name {}'.format(repo_name))
    result = None
    name_exist = False
    res, ok = check_status_code(cli.listRepositories())
    if ok:
        for repo_info in res.json():
            if repo_info['name'] == repo_name:
                name_exist = True

                break
        if name_exist:
            logger.debug('Repo name {} already exists'.format(repo_name))
            # generate new rpeo name
            suffix = random.randint(1, 10000)
            repo_name = '%s%s' % (repo_name, suffix)
            result = ensure_test_repo(cli, repo_name)
        else:
            # create repo with that name
            res, ok = check_status_code(cli.createRepository(data={'name': repo_name, 'git_url': AYS_TESTRUNNER_REPO_GIT}), 201)
            if ok is True:
                result = res.json()
    else:
        logger.info('Failed to list Repositories. Error: {}'.format(res.text))

    return result


def execute_blueprint(cli, blueprint, repo_info, logger=None):
    """
    Execute a blueprint
    """
    if logger is None:
        logger = j.logger.logging

    errors = []
    logger.info('Executing blueprint [{}]'.format(blueprint))
    curdir = j.sal.fs.getcwd()
    j.sal.fs.changeDir(repo_info['path'])
    cmd = 'ays blueprint -f %s' % blueprint
    try:
        j.tools.prefab.get().core.run(cmd)
    except Exception as e:
        errors.append('Failed to execute blueprint [{}]. Error: {}'.format(blueprint, e))
    finally:
        j.sal.fs.changeDir(curdir)
    return errors


def create_run(cli, repo_info, logger=None):
    """
    Create a run and execute it
    """
    if logger is None:
        logger = j.logger.logging

    errors = []
    logger.info('Creating a new run')
    curdir = j.sal.fs.getcwd()
    j.sal.fs.changeDir(repo_info['path'])
    cmd = 'ays run create -y --force -f'
    try:
        j.tools.prefab.get().core.run(cmd)
    except Exception as e:
        errors.append('Failed to create run. Error: {}'.format(e))

    return errors


def report_run(cli, repo_info, logger=None):
    """
    Check the created run and services for errors and report them if found
    check run status and report errors and logs if status is not ok
    if run status is ok then check the services result attribute and report errors if found
    """
    if logger is None:
        logger = j.logger.logging

    errors = []
    # check the run itself if there were errors while executing it
    res, ok = check_status_code(cli.listRuns(repository=repo_info['name']))
    if ok:
        runs_info = res.json()
        for run_info in runs_info:
            runid = run_info['key']
            if run_info['state'] == 'error':
                # get run
                res, ok = check_status_code(cli.getRun(runid, repo_info['name']))
                if ok:
                    run_details = res.json()
                    # run has steps and each step consists of jobs
                    for step in run_details['steps']:
                        if step['state'] == 'error':
                            for job in step['jobs']:
                                msg = 'Actor: {} Action: {}'.format(job['actor_name'], job['action_name'])
                                errors.append('\n%s' % msg)
                                errors.append('%s\n' % ('-' * len(msg)))
                                for log in job['logs']:
                                    if log['log']:
                                        errors.append(log['log'])

                else:
                    errors.append('Failed to retieve run [{}]'.format(runid))

        # after checking the runs, we need to check the services
        res, ok = check_status_code(cli.listServices(repo_info['name']))
        if ok:
            services = res.json()
            for service_info in services:
                res, ok = check_status_code(cli.getServiceByName(service_info['name'], service_info['role'], repo_info['name']))
                if ok:
                    service_details = res.json()
                    if service_details['data'].get('result') and not service_details['data']['result'].startswith('OK'):
                        msg = 'Service role: {} Service instance: {}'.format(service_info['role'], service_info['name'])
                        errors.append('\n%s' % msg)
                        errors.append('%s\n' % ('-' * len(msg)))
                        errors.append(service_details['data']['result'])
                else:
                    errors.append('Failed to get service [{}!{}]'.format(service_info['role'], service_info['name']))
        else:
            errors.append('Failed to list services')
    else:
        errors.append('Failed to list runs')

    return errors



class AYSTest:
    """
    Represents an AYS test bp
    """
    def __init__(self, name, path, logger=None):
        """
        Initialize the test

        @param path: Path to the test bp
        """
        self._path = path
        self._name = name
        self._prefab = j.tools.prefab.get()
        if logger is None:
            # FIXME: problem with using the js logger when pickling the object
            # self._logger = j.logger.get('aystestrunner.AYSTest.{}'.format(name))
            self._logger = logging.getLogger()
        else:
            self._logger = logger


    def replace_placehlders(self, config):
        """
        Use a given configuration to replace the content of the bp after replacing all the placeholder with values
        from the configuration
        """
        sed_base_command = 'sed -i s/\<{key}\>/{value}/g {path}'
        self._logger.info('Replacing placeholders for test blueprint {}'.format(self._path))
        for item, value in config.items():
            cmd = sed_base_command.format(key=item, value=value, path=self._path)
            j.tools.prefab.get().core.run(cmd)


    def setup(self):
        """
        Execute any setup setps
        """
        pass

    def teardown(self):
        """
        Execute any teardown steps
        """
        pass


    def run(self):
        """
        Run test by executing the following steps
        - Create a repo
        - Copy the blueprint to the repo
        - Execute the blueprint
        - Create a run and execute it
        - Collect run results
        - Destroy repo
        """
        self.setup()
        errors = []
        cli = j.clients.atyourservice.get().api.ays
        repo_info = ensure_test_repo(cli, AYS_TESTRUNNER_REPO_NAME, logger=self._logger)
        if repo_info is None:
            errors.append('Failed to create new ays repository for test {}'.format(self._name))
        else:
            j.sal.fs.copyFile(self._path, j.sal.fs.joinPaths(repo_info['path'], 'blueprints', self._name))
            # execute bp
            errors.extend(execute_blueprint(cli, self._name, repo_info, logger=self._logger))
            # create run and execute it
            errors.extend(create_run(cli, repo_info, logger=self._logger))
            # report run
            errors.extend(report_run(cli, repo_info, logger=self._logger))
            self._errors = errors
            # destroy repo
            cli.destroyRepository(data={}, repository=repo_info['name'])

        self.teardown()
        return errors


    @property
    def name(self):
        return self._name


class BaseRunner:
    """
    Base class for test runners
    """
    def __init__(self, name, config=None):
        """
        Intialize test runner
        """
        if config is None:
            config = {}
        self._config = config
        self._name = name
        self._task_queue = Queue(connection=Redis(), default_timeout=self._config.get('TEST_TIMEOUT', DEFAULT_TEST_TIMEOUT))
        self._logger = j.logger.get('aystestrunner.{}'.format(name))
        self._failed_tests = {}
        self._tests = []


    def run(self):
        """
        Run tests and report their results
        collects tests
        pre-process tests
        execute setup steps
        execute test
        execute teardown setps
        report tests
        """
        raise NotImplementedError("Not Implemented")



class AYSCoreTestRunner(BaseRunner):
    """
    Test Runner to run ays core tets
    """

    def _collect_tests(self, paths):
        """
        Collects all test bp from the given paths
        This will only scan only one level of the paths and collect all the files that that ends with .yaml and .bp files
        """
        result = []
        self._logger.info('Collecting tests from paths {}'.format(paths))
        for path in paths:
            if not j.sal.fs.exists(path):
                self._logger.error('Path {} does not exist'.format(path))
                continue
            for root, _, files in os.walk(path):
                for file_ in [file__ for file__ in files if not file__.startswith('_') and  (file__.endswith('{}yaml'.format(os.path.extsep)) or
                                                            file__.endswith('{}bp'.format(os.path.extsep))
                                                            )]:
                    result.append(AYSTest(name=file_, path=j.sal.fs.joinPaths(root, file_)))
        return result


    def _pre_process_tests(self):
        """
        Execute any required pre-processing steps
        """
        for test in self._tests:
            test.replace_placehlders(self._config.get('G8ENV', {}))


    def run(self):
        """
        Run tests and report their results
        collects tests
        pre-process tests
        execute setup steps
        execute test
        execute teardown setps
        report tests
        """
        jobs = {}
        self._tests = self._collect_tests(paths=self._config.get('bp_paths', [AYS_CORE_BP_TESTS_PATH]))
        self._pre_process_tests()
        for test in self._tests:
            self._logger.info('Scheduling test {}'.format(test.name))
            jobs[test.name] = self._task_queue.enqueue(test.run)
        # block until all jobs are done
        while True:
            for name, job in jobs.copy().items():
                self._logger.debug('Checking status of test {}'.format(name))
                if job.result is None:
                    self._logger.info('Test {} still running'.format(name))
                elif job.result == []:
                    self._logger.info('Test {} completed successfully'.format(name))
                    jobs.pop(name)
                elif job.result is not None or job.exc_info is not None:
                    self._logger.error('Test {} failed'.format(name))
                    jobs.pop(name)
                    self._failed_tests[name] = job
            if jobs:
                time.sleep(30)
            else:
                break

        # report final results
        self._report_results()


    def _report_results(self):
        """
        Report final results after running all tests
        """
        nr_of_tests = len(self._tests)
        nr_of_failed = len(self._failed_tests)
        nr_of_ok = nr_of_tests - nr_of_failed
        print("AYS testrunner results\n---------------------------\n")
        print("Total number of tests: {}".format(nr_of_tests))
        print("Number of passed tests: {}".format(nr_of_ok))
        print("Number of failed/error tests: %s" % nr_of_failed)
        if self._failed_tests:
            print("Errors:\n")
            for name, failed_test in self._failed_tests.items():
                header = 'Test {}'.format(name)
                print(header)
                print('-' * len(header))
                if failed_test.result:
                    print('\n'.join(failed_test.result))
                if failed_test.exc_info:
                    print(failed_test.exc_info)
            raise RuntimeError('Failures while running ays tests')
