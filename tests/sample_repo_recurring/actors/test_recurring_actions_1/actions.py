def init_actions_ (service, args):
    '''
    this needs to returns an array of actions representing the depencies between actions.

Looks at ACTION_DEPS in this module for an example of what is expected
    '''
    return {
        'execution_gt_period': ['install']
    }
    

def execution_gt_period (job):
    '''
    Tests execution time of a service that takes more than the configured recurring period
    '''
    import time
    print('waiting...')
    time.sleep(5 * 60)
    

def execute_hanging_job (job):
    '''
    Tests managing of hanging jobs
    '''
    import time
    while True:
        time.sleep(5 * 60)
    

def input (job):
    return None
    

def init (job):
    pass
    

def install (job):
    pass
    

def stop (job):
    pass
    

def start (job):
    pass
    

def monitor (job):
    pass
    

def halt (job):
    pass
    

def check_up (job):
    pass
    

def check_down (job):
    pass
    

def check_requirements (job):
    pass
    

def cleanup (job):
    pass
    

def data_export (job):
    pass
    

def data_import (job):
    pass
    

def uninstall (job):
    pass
    

def removedata (job):
    pass
    

def consume (job):
    pass
    

def action_pre_ (job):
    pass
    

def action_post_ (job):
    pass
    

def delete (job):
    j.tools.async.wrappers.sync(job.service.delete())
    

