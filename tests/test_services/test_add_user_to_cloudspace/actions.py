def test_user_access(job):
    pass

def test_update_user_access(job):
    pass

def test_delete_user_access(job):
    pass

def test_vdc_user(job):
    import requests, sys, time
    service = job.service
    RESULT_OK = 'OK : %s '
    RESULT_FAILED = 'FAILED : %s'
    RESULT_ERROR = 'ERROR : %s'
    failures = []
    try:
        cl = j.clients.atyourservice.get().api.ays
        repo = 'sample_repo_vdcuser'
        cl.executeBlueprint(data=None, blueprint='setupvdc.yaml', repository=repo)
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

        vdc = cl.getServiceByName(role="vdc", name="testvdc", repository=repo).json()

        res = cl.executeBlueprint(data=None, blueprint='adduser.yaml', repository=repo).json()
        job = cl.getJob(repository=repo, jobid=res['processChangeJobs'][0]).json()
        while job['state'] != 'ok':
            time.sleep(2)
            job = cl.getJob(repository=repo, jobid=res['processChangeJobs'][0]).json()

        vdc = cl.getServiceByName(role="vdc", name="testvdc", repository=repo).json()
        user_name = 'usertest'
        if not vdc['data']['uservdc']:
            failures.append(RESULT_FAILED % 'user not added to model data')
        vdcId = vdc['data']['cloudspaceID']

        API_URL = url + '/restmachine/cloudapi/cloudspaces/get'
        API_BODY = {'cloudspaceId': vdcId}

        response = session.post(url=API_URL, data=API_BODY)

        if response.status_code == 200:
            content = response.json()
            for user in content['acl']:
                if user_name in user['userGroupId']:
                    service.model.data.result = RESULT_OK % 'user added to cloudspace'
                    break
                else:
                    continue
            else:
                failure = '%s not in %i cloudspace' % (username, vdcId)
                failures.append(RESULT_FAILED % failure)
        else:
            response_data = {'status_code': response.status_code,
                             'content': response.content}
            failures.append(RESULT_ERROR % str(response_data) + str(vdcId))
        vdc = cl.getServiceByName(role="vdc", name="testvdc", repository=repo).json()

        res = cl.executeBlueprint(data=None, blueprint='changeaccess.yaml', repository=repo).json()
        job = cl.getJob(repository=repo, jobid=res['processChangeJobs'][0]).json()
        while job['state'] != 'ok':
            time.sleep(2)
            job = cl.getJob(repository=repo, jobid=res['processChangeJobs'][0]).json()
        vdc = cl.getServiceByName(role="vdc", name="testvdc", repository=repo).json()
        accesstype = 'ACDRUX'
        if vdc['data']['uservdc'][0]['accesstype'] != accesstype:
            failures.append(RESULT_FAILED % 'accesstype not updated in data')
        vdcId = vdc['data']['cloudspaceID']
        API_BODY = {'cloudspaceId': vdcId}
        response = session.post(url=API_URL, data=API_BODY)
        if response.status_code == 200:
            content = response.json()
            for user in content['acl']:
                if user_name in user['userGroupId']:
                    if user['right'] == accesstype:
                        service.model.data.result = RESULT_OK % ' successfully updated vdc access right'
                    else:
                        failures.append(RESULT_FAILED % 'failed to update vdc access rights')
                    break
                else:
                    continue
            else:
                failure = '%s not in %i cloudspace' % (username, vdcId)
                failures.append(RESULT_ERROR % failure)
        else:
            response_data = {'status_code': response.status_code,
                             'content': response.content}
            failures.append(RESULT_ERROR % str(response_data) + str(vdcId))
        res = cl.executeBlueprint(data=None, blueprint='deleteuser.yaml', repository=repo).json()
        job = cl.getJob(repository=repo, jobid=res['processChangeJobs'][0]).json()
        while job['state'] != 'ok':
            time.sleep(2)
            job = cl.getJob(repository=repo, jobid=res['processChangeJobs'][0]).json()
        vdc = cl.getServiceByName(role="vdc", name="testvdc", repository=repo).json()
        if vdc['data']['uservdc']:
            failures.append(RESULT_FAILED % 'failed to remove user from  model data')
        vdcId = vdc['data']['cloudspaceID']
        API_BODY = {'cloudspaceId': vdcId}
        response = session.post(url=API_URL, data=API_BODY)
        if response.status_code == 200:
            content = response.json()
            for user in content['acl']:
                if user_name in user['userGroupId']:
                    failures.append(RESULT_FAILED % 'failed to remove user from vdc')
                    break
                else:
                    service.model.data.result = RESULT_OK % 'successfully deleted user from vdc'

        else:
            response_data = {'status_code': response.status_code,
                             'content': response.content}
            failures.append(RESULT_ERROR % str(response_data) + str(vdcId))
        if failures:
            service.model.data.result = '\n'.join(failures)
    except Exception as e:
        service.model.data.result = RESULT_ERROR % (str(sys.exc_info()[:2]) + str(e))
    service.save()
    cl.destroyRepository(data=None, repository=repo)
