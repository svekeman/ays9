"""
Run tests
"""
from Jumpscale9 import j
import random

AYS_TESTRUNNER_REPO_NAME = 'ays_testrunner'
AYS_TESTRUNNER_REPO_GIT = 'https://github.com/ahussein/ays_testrunner.git'

def check_status_code(res, expected_status_code=200):
    """
    Check if a response object has the expected status code

    returns (response object, True/False)
    """
    if res.status_code == expected_status_code:
        return True
    return False

def ensure_test_repo(cli, repo_name):
    """
    Ensure a new repo for running tests is created with unique name
    """
    result = None
    name_exist = False
    res, ok = check_status_code(cli.listRepositories())
    if ok:
        for repo_info in res.json():
            if repo_info['name'] == repo_name:
                name_exist = True
                break
        if name_exist:
            # generate new rpeo name
            suffix = random.randint(1, 10000)
            repo_name = '%s%s' % (repo_name, suffix)
            ensure_test_repo(cli, repo_name)
        else:
            # create repo with that name
            result = repo_name
    else:
        j.logger.logging.log('Failed to list Repositories. Error: %s' % res.text)
    return result


cli = j.clients.atyourservice.get().api.ays


repo_name = ensure_test_repo(cli, AYS_TESTRUNNER_REPO_NAME)

if repo_name:
