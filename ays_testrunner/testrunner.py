"""
Test runner module for AYS9
"""
from js9 import j
import os

AYS_CORE_BP_TESTS_PATH = j.sal.fs.joinPaths(j.sal.fs.getParent(j.sal.fs.getParent(__file__)), 'tests', 'bp_test_templates', 'core')


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
        self._name = path
        if logger is None:
            self._logger = j.logger.get('aystestrunner.AYSTest.{}'.format(name))
        else:
            self._logger = logger


    def replace_placehlders(self, config):
        """
        Use a given configuration to replace the content of the bp after replacing all the placeholder with values
        from the configuration
        """
        self._logger.info('Replacing placeholders for test blueprint {}'.format(self._path))




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
        self._logger = j.logger.get('aystestrunner.{}'.format(name))


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
        self._tests = self._collect_tests(paths=self._config.get('bp_paths', [AYS_CORE_BP_TESTS_PATH]))
        self._pre_process_tests()
