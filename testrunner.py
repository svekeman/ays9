#!/usr/bin/env python

from js9 import j
import random

AYS_TESTRUNNER_REPO_NAME = 'ays_testrunner'
AYS_TESTRUNNER_REPO_GIT = 'https://github.com/ahussein/ays_testrunner.git'
AYS_CORE_BP_TESTS_PATH = 'tests/bp_test_templates/core'

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



def main():
    cli = j.clients.atyourservice.get().api.ays
    repo_info = ensure_test_repo(cli, AYS_TESTRUNNER_REPO_NAME)

    if repo_info:
        try:
            copy_blueprints(AYS_CORE_BP_TESTS_PATH, repo_info)
        finally:
            # clean the created repo
            j.logger.logging.info('Cleaning up ceated repository')
            # cli.destroyRepository(data={}, repository=repo_info['name'])
            # cli.deleteRepository(repository=repo_info['name'])

if __name__ == '__main__':
    main()
