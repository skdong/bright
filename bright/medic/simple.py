from automaton import machines

def show_machine(machine):
    print m.pformat()
    print m.current_state
    print m.terminated

m = machines.FiniteMachine()
m.add_state('up')
m.add_state('down')
m.add_transition('down', 'up','jump')
m.add_transition('up', 'down', 'fail')
m.default_start_state = 'down'

show_machine(m)

m.initialize()
m.process_event('jump')

show_machine(m)

m.process_event('fail')
show_machine(m)