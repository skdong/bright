import timeout
class Task(object):
    def __init__(self, name=None, description=""):
        self.name = name
        self.description = description

@timeout.timeout(2)
def test_timeout():
    print "test"

test_timeout()