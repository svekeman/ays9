#!/usr/bin/env python

from js9 import j
import random

AYS_TESTRUNNER_REPO_NAME = 'ays_testrunner'
AYS_TESTRUNNER_REPO_GIT = 'https://github.com/ahussein/ays_testrunner.git'
AYS_CORE_BP_TESTS_PATH = 'tests/bp_test_templates/core'
STOP_AT_ERRORS = False

def check_status_code(res, expected_status_code=200):
    """
    Check if a response object has the expected status code

    returns (response object, True/False)
    """
    j.logger.logging.debug('Validating response status code %s with expected status code %s' % (res.status_code, expected_status_code))
    if res.status_code == expected_status_code:
        return res, True
    return res, False

def ensure_test_repo(cli, repo_name):
    """
    Ensure a new repo for running tests is created with unique name
    """
    j.logger.logging.debug('Ensuring test repo with name %s' % repo_name)
    result = None
    name_exist = False
    res, ok = check_status_code(cli.listRepositories())
    if ok:
        for repo_info in res.json():
            if repo_info['name'] == repo_name:
                name_exist = True

                break
        if name_exist:
            j.logger.logging.debug('Repo name %s already exists' % repo_name)
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
        j.logger.logging.info('Failed to list Repositories. Error: %s' % res.text)

    return result

def copy_blueprints(test_bp_path, repo_info):
    """
    Copies the ays core test bluepprints to the test runner ays repo
    """
    dest = j.sal.fs.joinPaths(repo_info['path'], 'blueprints')
    j.sal.fs.copyDirTree(test_bp_path, dest)

def execute_blueprint(cli, blueprint, repo_info):
    """
    Execute a blueprint
    """
    errors = []
    j.logger.logging.info('Executing blueprint [%s]' % blueprint)
    curdir = j.sal.fs.getcwd()
    j.sal.fs.changeDir(repo_info['path'])
    cmd = 'ays blueprint -f %s' % blueprint
    try:
        j.tools.prefab.get().core.run(cmd)
    except Exception as e:
        errors.append('Failed to execute blueprint [%s]. Error: %s' % (blueprint, e))
    finally:
        j.sal.fs.changeDir(curdir)
    return errors

def create_run(cli, repo_info):
    """
    Create a run and executing it
    """
    errors = []
    j.logger.logging.info('Creating a new run')
    curdir = j.sal.fs.getcwd()
    j.sal.fs.changeDir(repo_info['path'])
    cmd = 'ays run create -y --force -f'
    try:
        j.tools.prefab.get().core.run(cmd)
    except Exception as e:
        errors.append('Failed to create run. Error: %s' % (e))

    return errors

def report_run(cli, repo_info):
    """
    Check the created run and services for errors and report them if found
    check run status and report errors and logs if status is not ok
    if run status is ok then check the services result attribute and report errors if found
    """
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
                                msg = 'Actor: %s Action: %s' % (job['actor_name'], job['action_name'])
                                errors.append('\n%s' % msg)
                                errors.append('%s\n' % ('-' * len(msg)))
                                for log in job['logs']:
                                    if log['log']:
                                        errors.append(log['log'])

                else:
                    errors.append('Failed to retieve run [%s]' % runid)

        # after checking the runs, we need to check the services
        res, ok = check_status_code(cli.listServices(repo_info['name']))
        if ok:
            services = res.json()
            for service_info in services:
                res, ok = check_status_code(cli.getServiceByName(service_info['name'], service_info['role'], repo_info['name']))
                if ok:
                    service_details = res.json()
                    if service_details['data'].get('result') and not service_details['data']['result'].startswith('OK'):
                        msg = 'Service role: %s Service instance: %s' % (service_info['role'], service_info['name'])
                        errors.append('\n%s' % msg)
                        errors.append('%s\n' % ('-' * len(msg)))
                        errors.append(service_details['data']['result'])
                else:
                    errors.append('Failed to get service [%s!%s]' % (service_info['role'], service_info['name']))
        else:
            errors.append('Failed to list services')
    else:
        errors.append('Failed to list runs')

    return errors

def execute_blueprints(cli, repo_info):
    """
    Executes all the blueprints in the repo
    For each blueprint:
        - execute the blueprint
        - create a run
        - execute the run
        - wait for the run to finish
        - destory the repo
    """
    errors = {}
    bps_path = j.sal.fs.joinPaths(repo_info['path'], 'blueprints')
    blueprints = map(j.sal.fs.getBaseName, j.sal.fs.listFilesInDir(path=bps_path))
    for blueprint in blueprints:
        errors[blueprint] = {'errors': []}
        bp_errors = errors[blueprint]['errors']
        bp_errors.extend(execute_blueprint(cli, blueprint, repo_info))
        bp_errors.extend(create_run(cli, repo_info))
        bp_errors.extend(report_run(cli, repo_info))
        cli.destroyRepository(data={}, repository=repo_info['name'])
        if STOP_AT_ERRORS:
            raise RuntimeError('Failures while executing blueprint %s. Errors: %s' %(blueprint, bp_errors))
    return errors

def main():
    cli = j.clients.atyourservice.get().api.ays
    repo_info = ensure_test_repo(cli, AYS_TESTRUNNER_REPO_NAME)
    errors = []
    if repo_info:
        try:
            copy_blueprints(AYS_CORE_BP_TESTS_PATH, repo_info)
            result = execute_blueprints(cli, repo_info)
            # report final results
            nr_ok = 0
            nr_errs = 0
            for bp_errors in result.values():
                if bp_errors['errors']:
                    errors.extend(bp_errors['errors'])
                    nr_errs += 1
                else:
                    nr_ok += 1
            nr_of_tests = nr_ok + nr_errs
            print("AYS testrunner results\n---------------------------\n")
            print("Total number of tests: %s" % nr_of_tests)
            print("Number of passed tests: %s" % nr_ok)
            print("Number of failed/error tests: %s" % nr_errs)
            if errors:
                print("\nErrors\n-------\n")
                print('\n'.join(errors))
                raise RuntimeError('Failures while running ays tests')
        finally:
            # clean the created repo
            j.logger.logging.info('Cleaning up ceated repository')
            cli.destroyRepository(data={}, repository=repo_info['name'])
            cli.deleteRepository(repository=repo_info['name'])

if __name__ == '__main__':
    main()
