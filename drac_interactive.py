import curses

import drac, drac_common, drac_config, drac_plays

def run(game, stdscr):

    curses.echo()

    stdscr.clear()
    stdscr.addstr('Preparing game...\n')

    if drac_config.links:
        stdscr.addstr('Links are enabled in config.\nSearching for links module...')
        try:
            import drac_links
            stdscr.addstr(' Found!\n')
        except ImportError:
            drac_links = None
            stdscr.addstr(' Missing!\n')
    else:
        drac_links = None
        stdscr.addstr('Links disabled in config!\n')

    if drac_links is not None:
        stdscr.addstr('Loading links...')
        try:
            drac_links.addlinks(game)
            game.links = True
            stdscr.addstr(' Done!\n')
        except Exception:
            stdscr.addstr(' Failed!\n')

    stdscr.refresh()

    stdscr.addstr('\nWelcome to drac interactive!\n\n')
    stdscr.addstr('When you\'re ready to start, press [ENTER]\n')
    try:
        stdscr.getstr()
        stdscr.clear()
    except KeyboardInterrupt:
        return
    pl = 0
    quit = False
    while not game.ended:
        if pl == 0:
            stdscr.addstr('###########################\n')
            stdscr.addstr('######## Turn %4d ########\n' % (game.turn/5+1))
            stdscr.addstr('###########################\n')
            stdscr.addstr('\nType \'?\' to see what you can do!\n\n')
        pl_letter = drac_common.players[pl]
        p = game.players[pl]
        game.lastValid = False
        while not game.lastValid:
            move = ''
            loop = True
            prevFirstRow = -1
            while loop:
                try:
                    move = 'cmd'
                    stdscr.addstr(p.name + ' > ')
                    text = ''
                    cursor_pos = stdscr.getyx()
                    while text == '':
                        text = stdscr.getstr().lower().strip()
                        stdscr.move(cursor_pos[0], cursor_pos[1])
                    stdscr.deleteln()
                    stdscr.move(cursor_pos[0], 0)
                    if prevFirstRow >= 0:
                        while stdscr.getyx()[0] - prevFirstRow > 0:
                            stdscr.deleteln()
                            stdscr.move(stdscr.getyx()[0]-1, stdscr.getyx()[1])
                    prevFirstRow = stdscr.getyx()[0]
                    if text != '':
                        if text == '?' or text == 'help':
                            stdscr.addstr('====================== Help =======================\n')
                            stdscr.addstr('|                                                 |\n')
                            stdscr.addstr('|   <town_abbrev>    : move to the specified town |\n')
                            stdscr.addstr('|   moves            : see valid moves            |\n')
                            stdscr.addstr('|   players          : show player information    |\n')
                            stdscr.addstr('|   links            : show town connections      |\n')
                            if pl == 4:
                                stdscr.addstr('|   see [town]       : show town information      |\n')
                                stdscr.addstr('|   traps            : show where the traps are   |\n')
                                stdscr.addstr('|   vamps            : show where the vamps are   |\n')
                                stdscr.addstr('|   trail            : show your trail            |\n')
                            else:
                                stdscr.addstr('|   look             : show town information      |\n')
                            stdscr.addstr('|    ?, help         : show this help menu        |\n')
                            stdscr.addstr('|                                                 |\n')
                            stdscr.addstr('====================== Help =======================\n')
                        elif text == 'moves':
                            if p.location is None:
                                stdscr.addstr('Valid cities for you to set down in\n')
                                for i in range((len(game.locations) + len(game.locations)%2)/2):
                                    stdscr.addstr('%30s %30s\n' % (game.locations[i*2].disp(False), game.locations[i*2+1].disp(False) if len(game.locations) > i*2+1 else ''))
                            else:
                                stdscr.addstr('Valid moves:\n')
                                seen_moves = []
                                if game.links:
                                    for loc in game.locations:
                                        if drac_links.haslink(game, loc.index, p.location.index, p, 1) or drac_links.haslink(game, loc.index, p.location.index, p, 3):
                                            seen_moves.append(loc)
                                        if pl != 4 and drac_links.hasanylink(game, loc.index, p.location.index, p, (game.turn/5+pl)%4):
                                            #if loc not in seen_moves:
                                            seen_moves.append(loc)
                                else:
                                    for loc in game.locations:
                                        seen_moves.append(loc)
                                counter = 0
                                for move in seen_moves:
                                    stdscr.addstr('\t%25s\t' % move.disp(False))
                                    counter += 1
                                    if counter % 2 == 0 or counter == len(seen_moves):
                                        stdscr.addstr('\n')
                        elif text == 'players':
                            stdscr.addstr('Players:\n')
                            for player in game.players:
                                if player.location is None:
                                    stdscr.addstr('%17s hasn\'t set down yet\n' % player.name)
                                elif player.index == 4:
                                    if pl == 4:
                                        stdscr.addstr('%17s is in %s\n' % (player.name, player.location.disp(False)))
                                    else:
                                        m_abbrev = 'S?' if player.location.index in drac_common.seas else 'C?'
                                        if m_abbrev == 'S?':
                                            stdscr.addstr('%17s is over water (S?)\n' % player.name)
                                        else:
                                            stdscr.addstr('%17s is in a city (C?)\n' % player.name)
                                else:
                                    stdscr.addstr('%17s is in %s\n' % (player.name, player.location.disp(False)))
                        elif text == 'links':
                            if p.location is None:
                                stdscr.addstr('You are not in a town\n')
                            else:
                                types = ['road', 'rail', 'boat']
                                stdscr.addstr('%s links:\n' % p.location.disp(True))
                                for loc in game.locations:
                                    if drac_links.haslink(drac.game, loc.index, p.location.index, p, 1):
                                        stdscr.addstr('\troad to %s\n' % loc.disp(False))
                                    if p.index != 4 and drac_links.haslink(drac.game, loc.index, p.location.index, p, 2):
                                        stdscr.addstr('\trail to %s\n' % loc.disp(False))
                                    if drac_links.haslink(drac.game, loc.index, p.location.index, p, 3):
                                        stdscr.addstr('\tboat to %s\n' % loc.disp(False))
                        elif text == 'trail' and pl == 4:
                            if len(game.trail.locs) == 0:
                                stdscr.addstr('Your trail is empty!\n')
                            else:
                                st = ''
                                for i in range(len(game.trail.locs)):
                                    if i > 0:
                                        st += ' -> '
                                    st += game.locations[game.trail.locs[len(game.trail.locs) - i - 1]].disp(False)
                                stdscr.addstr('%s\n' % st)
                        elif text.startswith('see') and pl == 4:
                            if len(text) == 3:
                                stdscr.addstr('Usage: see <town_abbrev>\n')
                            else:
                                text = text[4:].lower().strip()
                                if text != '':
                                    locs = []
                                    for lc in game.locations:
                                        if text == lc.abbrev.lower():
                                            locs.append(lc)
                                    if len(locs) == 0:
                                        for lc in game.locations:
                                            if text in lc.name.lower() or text in str(lc.index):
                                                locs.append(lc)
                                    if len(locs) == 0:
                                        stdscr.addstr('No towns found matching %s\n' % text)
                                    for lc in locs:
                                        stdscr.addstr('\t====== Town Information ======\n\tLocation: %s\n' % lc.disp(True))
                                        stdscr.addstr('\tTraps: %d\tVampires: %d\n' % (len(lc.traps), len(lc.vampires)))
                                        players_on_lc = []
                                        for pla in game.players:
                                            if pla.location == lc:
                                                players_on_lc.append(pla.name)
                                        stdscr.addstr('\tPlayers: ' + ', '.join(players_on_lc) + '\n' if len(players_on_lc) > 0 else 'Players: None\n')
                        elif text == 'look':
                            if p.location is None:
                                stdscr.addstr('You are not in a town\n')
                            else:
                                stdscr.addstr('Town: %s\n' % p.location.disp(True))
                                pls = []
                                for player in game.players:
                                    if player.location == p.location and player != p:
                                        if p.index == 4 or player.index != 4:
                                            pls.append(player.name)
                                if len(pls) == 0:
                                    stdscr.addstr('No other hunters\n')
                                else:
                                    stdscr.addstr('Players where you are: ' + ', '.join(pls) + '\n')
                        elif text == 'traps' and pl == 4:
                            for lc in game.locations:
                                if len(lc.traps) > 0:
                                    stdscr.addstr('%10s has %d trap%s\n' % (lc.name, len(lc.traps), 's' if len(lc.traps) > 1 else ''))
                        elif text == 'vamps' and pl == 4:
                            for lc in game.locations:
                                if len(lc.vampires) > 0:
                                    stdscr.addstr('%10s has %d vampire%s\n' % (lc.name, len(lc.vampires), 's' if len(lc.vampires) > 1 else ''))
                        else:
                            move = ''
                            for loc in game.locations:
                                if loc.abbrev.lower() == text:
                                    move = text
                                    loop = False
                            if move == '':
                                for loc in game.locations:
                                    if loc.name.lower() == text:
                                        move = loc.abbrev.lower()
                                        loop = False
                            if move == '' and pl == 4:
                                for sp in drac_common.specials:
                                    if sp.lower() == text:
                                        move = sp
                                        loop = False
                    if move == '':
                        stdscr.addstr('%s is not a valid move. Type \'?\' for help.\n' % text)
                except KeyboardInterrupt:
                    stdscr.addstr('\n\nGame terminated.\n')
                    quit = True
                    break
            if quit:
                break
            drac_plays.do_turn(stdscr, game, pl_letter + move.upper(), False, False)
        if quit:
            break
        if pl == 4:
            stdscr.addstr('\nPress [ENTER] when you\'re done, Dracula')
            stdscr.getstr()
            stdscr.clear()
        pl += 1
        if pl > 4: pl = 0
    if not quit:
        stdscr.getstr()



def run_interactive(stdscr):
    run(drac.game, stdscr)