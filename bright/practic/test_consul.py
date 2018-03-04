import consul
import time


def is_session_exist(name, sessions):
    for s in sessions:
        if s['Name'] == name:
            return True

    return False

def test_consul():
    c = consul.Consul()
    while True:
        index, sessions = c.session.list()
        if is_session_exist('worker', sessions):
            print "worker is alive ..."
        else:
            print 'worker is dead!'
            break
        time.sleep(3)

c = consul.Consul()
print c.session.list()
#c.kv.put("foo", "bar")
print c.kv.get("foo")[1].get("Value")
import pprint
#pprint.pprint( c.catalog.nodes()[1])
#pprint.pprint(c.catalog.datacenters())
pprint.pprint(c.agent.services())
