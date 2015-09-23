import sys, re

import drac_game, drac_plays, drac_config

def run(stdscr):
    if len(sys.argv) <= 1:
        stdscr.addstr('For mode=\'%s\' you must supply a pastPlays string.\n' % drac_config.mode)
        sys.exit(1)
    pastPlays = sys.argv[1]
    for s in re.findall(' D(C|S)\?', pastPlays):
        stdscr.addstr('ERROR: Past plays contains an unknown city/sea!\n')
        stdscr.addstr('ERROR: You must supply a string given to Dracula\n')
        sys.exit(1)

    for play in re.findall('\S+', pastPlays):
        drac_plays.do_turn(stdscr, drac_game.game, play, drac_config.mode == 'steps', True)
        if drac_game.game.ended:
            break