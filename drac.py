#!/usr/bin/python

import drac_listener, drac_config

try:
    import curses
except ImportError:
    curses = drac_listener.dummy_curses()

stdscr = drac_listener.dummy_stdscr()

if drac_config.mode == 'i' or drac_config.mode == 'interactive':
    import drac_interactive
    curses.wrapper(drac_interactive.run_interactive)
elif drac_config.mode in ['n', 'networked']:
    import drac_network
    curses.wrapper(drac_network.setup)
elif drac_config.mode in ['p', 'plays', 't', 'turns']:
    import drac_turnbyturn
    drac_turnbyturn.run(stdscr)
else:
    print "Invalid mode chosen: %s" % drac_config.mode