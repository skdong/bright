from stevedore import extension

def test_detect_plugins():
    em = extension.ExtensionManager('oslo.config.opts')
    print em.list_entry_points()
    for name in sorted(em.names()):
        print name

test_detect_plugins()