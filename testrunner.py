#!/usr/bin/env python

from js9 import j
import random

AYS_TESTRUNNER_REPO_NAME = 'ays_testrunner'
AYS_TESTRUNNER_REPO_GIT = 'https://github.com/ahussein/ays_testrunner.git'

def check_status_code(res, expected_status_code=200):
    """
    Check if a response object has the expected status code

    returns (response object, True/False)
    """
    print('Validating response status code %s with expected status code %s' % (res.status_code, expected_status_code))
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
        j.logger.logging.log('Failed to list Repositories. Error: %s' % res.text)

    return result


def main():
    cli = j.clients.atyourservice.get().api.ays
    repo_info = ensure_test_repo(cli, AYS_TESTRUNNER_REPO_NAME)

    if repo_info:
        try:
            copy_blueprints()
        finally:
            # clean the created repo
            j.logger.logging.log('Cleaning up ceated repository')
            cli.destroyRepository(repository=repo_info['name'])
            cli.deleteRepository(repository=repo_info['name'])

if __name__ == '__main__':
    main()
