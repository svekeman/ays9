 def test(job):
    
    #try to remove service knotused which is not consumed by anyone.
    try:
        cl.deleteServiceByName(name='knotconsumed', role='sshkey', repository=repo)
    except Exception as e:
        failures.append("Couldn't remove service knotconsumed even it's not consumed by anyone.")

    # now try to remove service kid which is consumed by cons1
    try:
        cl.deleteServiceByName(name='kid', role='chi', repository=repo).json()
    except Exception as e:
        pass
    else:
        failures.append("Was able to remove service kid even it's consumed by service cons1")

    # now try to remove service kp which will remove kid which is consumed by cons1
    try:
        cl.deleteServiceByName(name='kp', role='sshkey', repository=repo).json()
    except Exception as e:
        pass
    else:
        failures.append("Was able to remove service kp even it's a parent of kid which is consumed by service cons1")

    try:
        cl.deleteServiceByName(name='k1', role='sshkey', repository=repo).json()
    except Exception as e:
        failures.append("Wasn't able to remove service k1 even if won't break the minimum consumption required service cons1")

    try:
        cl.deleteServiceByName(name='k2', role='sshkey', repository=repo).json()
    except Exception as e:
        pass
    else:
        failures.append("Was able to remove service k2 even it will break the minimum consumption required service cons1")


    if failures:
        model.data.result = RESULT_FAILED % '\n'.join(failures)
