def init_actions_(service, args):
    """
    This needs to return an array of actions representing the depencies between actions.
    Looks at ACTION_DEPS in this module for an example of what is expected
    """

    # some default logic for simple actions


    return {
        'test': ['install']
    }


def test(job):
    import requests, sys, time
    service = job.service
    RESULT_OK = 'OK : %s '
    RESULT_FAILED = 'FAILED : %s'
    RESULT_ERROR = 'ERROR : %s'
    failures = []
    try:
        cl = j.clients.atyourservice.get().api.ays

        repo = 'sample_repo_account'

        # execute blueprint to setup account
        cl.executeBlueprint(data=None, blueprint='setupaccount.yaml', repository=repo)
        run = cl.createRun(data=None, repository=repo)
        run = cl.executeRun(repository=repo, data=None, runid=run.json()['key']).json()
        run = cl.getRun(repository=repo, runid=run['key']).json()
        while run['state'] != 'ok':
            time.sleep(2)
            run = cl.getRun(repository=repo, runid=run['key']).json()
        g8client = cl.getServiceByName(role="g8client", name="example", repository=repo).json()

        url = 'https://' + g8client['data']['url']
        username = g8client['data']['login']
        password = g8client['data']['password']

        login_url = url + '/restmachine/system/usermanager/authenticate'
        credential = {'name': username,
                      'secret': password}

        session = requests.Session()
        session.post(url=login_url, data=credential)

        account = cl.getServiceByName(role="account", name="acc", repository=repo).json()

        # execute blueprint to add user to account
        res = cl.executeBlueprint(data=None, blueprint='adduser.yaml', repository=repo).json()
        job = cl.getJob(repository=repo, jobid=res['processChangeJobs'][0]).json()
        while job['state'] != 'ok':
            time.sleep(2)
            job = cl.getJob(repository=repo, jobid=res['processChangeJobs'][0]).json()

        account = cl.getServiceByName(role="account", name="acc", repository=repo).json()

        if not account['data']['accountusers']:
            failures.append(RESULT_FAILED % 'user not added to model data')

        accountId = account.model.data.accountID
        API_URL = url + '/restmachine/cloudapi/accounts/get'
        API_BODY = {'accountId': accountId}

        response = session.post(url=API_URL, data=API_BODY)

        # check if user added to account
        if response.status_code == 200:
            content = response.json()
            if len(content['accountusers']) == 1:
                    service.model.data.result = RESULT_OK % 'successfully added user to account'
            else:
                failures.append(RESULT_FAILED % 'failed to add user to account')
        else:
            response_data = {'status_code': response.status_code,
                             'content': response.content}
            failures.append(RESULT_ERROR % str(response_data) + str(accountId))

        account = cl.getServiceByName(role="account", name="acc", repository=repo).json()

        #execute blueprint to change access
        res = cl.executeBlueprint(data=None, blueprint='changeaccess.yaml', repository=repo).json()
        job = cl.getJob(repository=repo, jobid=res['processChangeJobs'][0]).json()
        while job['state'] != 'ok':
            time.sleep(2)
            job = cl.getJob(repository=repo, jobid=res['processChangeJobs'][0]).json()

        account = cl.getServiceByName(role="account", name="acc", repository=repo).json()

        accesstype = 'ACDRUX'
        if account['data']['accountusers'][0]['accesstype'] != accesstype:
            failures.append(RESULT_FAILED % 'accesstype of user not updated in data')

        accountId = account.model.data.accountID
        API_BODY = {'accountId': accountId}

        response = session.post(url=API_URL, data=API_BODY)

        # TODO: check if access is changed


        # execute blueprint to delete user
        res = cl.executeBlueprint(data=None, blueprint='deleteuser.yaml', repository=repo).json()
        job = cl.getJob(repository=repo, jobid=res['processChangeJobs'][0]).json()
        while job['state'] != 'ok':
            time.sleep(2)
            job = cl.getJob(repository=repo, jobid=res['processChangeJobs'][0]).json()

        account = cl.getServiceByName(role="account", name="acc", repository=repo).json()
        API_BODY = {'accountId': accountId}

        response = session.post(url=API_URL, data=API_BODY)

        # check if user removed
        if response.status_code == 200:
            content = response.json()
            if len(content['accountusers']) == 0:
                    service.model.data.result = RESULT_OK % 'successfully deleted user from account'
            else:
                failures.append(RESULT_FAILED % 'failed to delete user from account')
        else:
            response_data = {'status_code': response.status_code,
                             'content': response.content}
            failures.append(RESULT_ERROR % str(response_data) + str(accountId))

        # execute blueprint to update limits
        res = cl.executeBlueprint(data=None, blueprint='updatelimits.yaml', repository=repo).json()
        job = cl.getJob(repository=repo, jobid=res['processChangeJobs'][0]).json()
        while job['state'] != 'ok':
            time.sleep(2)
            job = cl.getJob(repository=repo, jobid=res['processChangeJobs'][0]).json()

        account = cl.getServiceByName(role="account", name="acc", repository=repo).json()

        # check if limits are updated
        if response.status_code == 200:
            content = response.json()
            if content['maxMemoryCapacity'] == 50 and content['maxCPUCapacity'] == 10 and \
                content['maxDiskCapacity'] == 50 and content['maxNumPublicIP'] == 10:
                    service.model.data.result = RESULT_OK % 'successfully updated limimits for account'
            else:
                failures.append(RESULT_FAILED % 'failed to update limits of account')
        else:
            response_data = {'status_code': response.status_code,
                             'content': response.content}
            failures.append(RESULT_ERROR % str(response_data) + str(accountId))

        if failures:
            service.model.data.result = '\n'.join(failures)
    except:
        service.model.data.result = 'ERROR :  %s %s' % ('test_update_accounts_with_specs', str(sys.exc_info()[:2]))
    service.save()
    cl.destroyRepository(data=None, repository=repo)
