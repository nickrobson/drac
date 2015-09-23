import sys
import re
import drac_actor
import drac_config
import drac_game


def run(stdscr):
    if len(sys.argv) <= 1:
        stdscr.addstr('For mode=\'%s\' you must supply a past-plays string in the first argument.\n' % drac_config.mode)
        sys.exit(1)
    pastPlays = sys.argv[1]
    for s in re.findall(' D(C|S)\?', pastPlays):
        stdscr.addstr('ERROR: Past plays contains an unknown city/sea!\n')
        stdscr.addstr('ERROR: You must supply a string given to Dracula\n')
        sys.exit(1)

    for play in re.findall('\S+', pastPlays):
        turnBefore = drac_game.game.turn
        drac_actor.do_turn(stdscr, drac_game.game, play)
        if drac_game.game.turn == turnBefore:
            drac_game.game.turn += 1
        if drac_game.game.turn % 5 == 0 and (drac_config.mode == 't' or drac_config.mode == 'turns'):
            quit = False
            while not quit:
                try:
                    stdscr.addstr(">")
                    text = stdscr.getstr().strip()
                    if text == "":
                        break
                    elif text == "players":
                        for pl in drac_game.game.players:
                            stdscr.addstr("\t%s:\n\t\tLocation: %s\n\t\tHealth: %d\n" % (pl.name, pl.location.disp(True), pl.health))
                    elif text == "traps":
                        for lc in drac_game.game.locations:
                            if len(lc.traps) > 0:
                                stdscr.addstr("%10s has %d trap%s\n" % (lc.name, len(lc.traps), "s" if len(lc.traps) > 1 else ""))
                    elif text == "vamps":
                        for lc in drac_game.game.locations:
                            if len(lc.vampires) > 0:
                                stdscr.addstr("%10s has %d vampire%s\n" % (lc.name, len(lc.vampires), "s" if len(lc.vampires) > 1 else ""))
                    elif text.startswith("see "):
                        text = text[4:].lower().strip()
                        if text != "":
                            locs = []
                            for lc in drac_game.game.locations:
                                if text == lc.abbrev.lower():
                                    locs.append(lc)
                            if len(locs) == 0:
                                for lc in drac_game.game.locations:
                                    if text in lc.name.lower() or text in str(lc.index):
                                        locs.append(lc)
                            if len(locs) == 0:
                                stdscr.addstr("No towns found matching %s\n" % text)
                            for lc in locs:
                                stdscr.addstr("Location: %s" % lc.disp(True))
                                stdscr.addstr("\tTraps: %d\tVampires: %d\n" % (len(lc.traps), len(lc.vampires)))
                                players_on_lc = []
                                for pl in drac_game.game.players:
                                    if pl.location == lc:
                                        players_on_lc.append(pl.name)
                                stdscr.addstr("\tPlayers: " + ', '.join(players_on_lc) if len(players_on_lc) > 0 else "Players: None" + "\n")
                    elif text.startswith("links "):
                        text = text[6:].lower().strip()
                        if text != "":
                            locs = []
                            for lc in drac_game.game.locations:
                                if text == lc.abbrev.lower():
                                    locs.append(lc)
                            if len(locs) == 0:
                                for lc in drac_game.game.locations:
                                    if text in lc.name.lower() or text in str(lc.index):
                                        locs.append(lc)
                            if len(locs) == 0:
                                stdscr.addstr("No towns found matching %s\n" % text)
                            for lc in locs:
                                stdscr.addstr(lc.show_links(drac_game.game, None))
                    elif text == "?" or text == "help":
                        stdscr.addstr("====================== Help =======================\n")
                        stdscr.addstr("|                                                 |\n")
                        stdscr.addstr("|   players          : show player information    |\n")
                        stdscr.addstr("|   see [town]       : show town information      |\n")
                        stdscr.addstr("|   links            : show town connections      |\n")
                        stdscr.addstr("|   traps            : show where the traps are   |\n")
                        stdscr.addstr("|   vamps            : show where the vamps are   |\n")
                        stdscr.addstr("|   q, quit          : quits drac                 |\n")
                        stdscr.addstr("|                                                 |\n")
                        stdscr.addstr("====================== Help =======================\n")
                    elif text == "q" or text == "quit":
                        quit = True
                        break
                except KeyboardInterrupt:
                    stdscr.addstr("\n\nGame terminated\n\n")
                    quit = True
            if quit:
                drac_game.game.ended = True
                return
        if drac_game.game.ended:
            break
