from bright.sinnetcloud.ceilometer import get_resources

def migrate_meters():
    resources = get_resources()
    create_resources(resources)

def get_meters():
    pass

def get_samples():
    pass

def create_resource():
    pass

def create_metric():
    pass

def push_measures():
    pass