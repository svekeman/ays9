def init_actions_(service, args):
    return {
        'test_create': ['init'],
        'test_delete': ['init'],
    }


def test_create(job):
    import requests
    import sys
    RESULT_OK = 'OK : %s '
    RESULT_FAILED = 'FAILED : %s'
    RESULT_ERROR = 'ERROR : %s'

    service = job.service
    try:
        g8client = service.producers['g8client'][0]
        url = 'https://' + g8client.model.data.url
        username = g8client.model.data.login
        password = g8client.model.data.password
        login_url = url + '/restmachine/system/usermanager/authenticate'
        credential = {'name': username,
                      'secret': password}
        session = requests.Session()
        session.post(url=login_url, data=credential)

        vm = service.producers['node'][0]
        vm_id = vm.model.data.machineId

        api_url = url + '/restmachine/cloudapi/machines/get'
        api_body = {'machineId': vm_id}

        response = session.post(url=api_url, data=api_body)

        if response.status_code == 200:
            content = response.json()
            if vm.name != content['name']:
                failure = vm.name + '!=' + content['name']
                service.model.data.result = RESULT_FAILED % failure
            elif vm.model.data.osImage != content['osImage']:
                failure = service.model.data.osImage + '!=' + content['osImage']
                service.model.data.result = RESULT_FAILED % failure
            elif vm.model.data.bootdiskSize != content['disks'][0]['sizeMax']:
                failure = service.model.data.bootdiskSize + '!=' + content['disks'][0]['sizeMax']
                service.model.data.result = RESULT_FAILED % failure
            else:
                service.model.data.result = RESULT_OK % 'test_create_virtualmachine'
        else:
            response_data = {'status_code': response.status_code,
                             'content': response.content}
            service.model.data.result = RESULT_ERROR % str(response_data)+str(vm_id)
    except Exception as e:
        service.model.data.result = RESULT_ERROR % (str(sys.exc_info()[:2]) + str(e))
    service.save()


def test_delete(job):
    import requests
    import sys
    RESULT_OK = 'OK : %s '
    RESULT_ERROR = 'ERROR : %s'

    service = job.service
    try:
        g8client = service.producers['g8client'][0]
        url = 'https://' + g8client.model.data.url
        username = g8client.model.data.login
        password = g8client.model.data.password
        login_url = url + '/restmachine/system/usermanager/authenticate'
        credential = {'name': username,
                      'secret': password}
        session = requests.Session()
        session.post(url=login_url, data=credential)

        vm = service.producers['node'][0]
        vm_id = vm.model.data.machineId

        api_url = url + '/restmachine/cloudapi/machines/get'
        api_body = {'machineId': vm_id}

        response = session.post(url=api_url, data=api_body)

        if response.status_code == 404:
            service.model.data.result = RESULT_OK % 'test_delete_virtualmachine'
        else:
            response_data = {'status_code': response.status_code,
                             'content': response.content}
            service.model.data.result = RESULT_ERROR % str(response_data)+str(vm_id)
    except Exception as e:
        service.model.data.result = RESULT_ERROR % (str(sys.exc_info()[:2]) + str(e))
    service.save()
