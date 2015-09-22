#!/usr/bin/python

import sys, os, re, drac, drac_common, drac_config, drac_plays

class dummy_stdscr:
    def getstr(self):
        return raw_input('').lower().strip()
    def addstr(self, s):
        print s,
    def clear(self):
        print '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
    def deleteln(self):
        return
    def delch(self, y, x):
        return
    def move(self, y, x):
        return
    def getyx(self):
        return (0, 0)
    def refresh(self):
        return

class dummy_curses:
    def echo(self):
        return
    def wrapper(self, main):
        dummy = dummy_stdscr()
        main(dummy)

try:
    import curses
except ImportError:
    curses = dummy_curses()

stdscr = dummy_stdscr()

if drac_config.mode == 'i' or drac_config.mode == 'interactive':
    import drac_interactive
    curses.wrapper(drac_interactive.run_interactive)
elif drac_config.mode in ['n', 'networked']:
    import drac_network
    curses.wrapper(drac_network.setup)
else:
    if drac_config.mode in ['p', 'plays', 't', 'turns']:
        if len(sys.argv) <= 1:
            stdscr.addstr('For mode=\'%s\' you must supply a pastPlays string.\n' % drac_config.mode)
            sys.exit(1)
        pastPlays = sys.argv[1]
        for s in re.findall(' D(C|S)\?', pastPlays):
            stdscr.addstr('ERROR: Past plays contains an unknown city/sea!\n')
            stdscr.addstr('ERROR: You must supply a string given to Dracula\n')
            sys.exit(1)

        for play in re.findall('\S+', pastPlays):
            drac_plays.do_turn(stdscr, game, play, drac_config.mode == 'steps', True)
            if game.ended:
                break