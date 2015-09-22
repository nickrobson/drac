import drac_common, drac_links

def do_turn(stdscr, game, play, steps, print_turns):
    game.lastValid = True

    while len(play) < 7:
        play = play + "."

    if game.score <= 0:
        stdscr.addstr("\n\nScore hit 0! Dracula wins!\n")
        stdscr.addstr("Score hit 0! Dracula wins!\n")
        stdscr.addstr("Score hit 0! Dracula wins!\n")
        stdscr.addstr("Score hit 0! Dracula wins!\n\n")
        game.ended = True
        return

    actualTurn = game.turn / 5
    if actualTurn > game.lastTurn:
        game.lastTurn = actualTurn
        if actualTurn > 0 and steps:
            quit = False
            while True:
                try:
                    text = stdscr.getstr().strip()
                    if text == "":
                        break
                    elif text == "players":
                        for pl in game.players:
                            stdscr.addstr("%s:\n\t\tLocation: %s\n\t\tHealth: %d\n" % (pl.name, pl.location.disp(True), pl.health))
                    elif text == "traps":
                        for lc in game.locations:
                            if len(lc.traps) > 0:
                                stdscr.addstr("%10s has %d trap%s\n" % (lc.name, len(lc.traps), "s" if len(lc.traps) > 1 else ""))
                    elif text == "vamps":
                        for lc in game.locations:
                            if len(lc.vampires) > 0:
                                stdscr.addstr("%10s has %d vampire%s\n" % (lc.name, len(lc.vampires), "s" if len(lc.vampires) > 1 else ""))
                    elif text.startswith("see "):
                        text = text[4:].lower().strip()
                        if text != "":
                            locs = []
                            for lc in game.locations:
                                if text == lc.abbrev.lower():
                                    locs.append(lc)
                            if len(locs) == 0:
                                for lc in game.locations:
                                    if text in lc.name.lower() or text in str(lc.index):
                                        locs.append(lc)
                            if len(locs) == 0:
                                stdscr.addstr("No towns found matching %s\n" % text)
                            for lc in locs:
                                stdscr.addstr("Location: %s" % lc.disp(True))
                                stdscr.addstr("\tTraps: %d\tVampires: %d\n" % (len(lc.traps), len(lc.vampires)))
                                players_on_lc = []
                                for pl in game.players:
                                    if pl.location == lc:
                                        players_on_lc.append(pl.name)
                                stdscr.addstr("\tPlayers: " + ', '.join(players_on_lc) if len(players_on_lc) > 0 else "Players: None" + "\n")
                    elif text.startswith("links "):
                        text = text[6:].lower().strip()
                        if text != "":
                            locs = []
                            for lc in game.locations:
                                if text == lc.abbrev.lower():
                                    locs.append(lc)
                            if len(locs) == 0:
                                for lc in game.locations:
                                    if text in lc.name.lower() or text in str(lc.index):
                                        locs.append(lc)
                            if len(locs) == 0:
                                stdscr.addstr("No towns found matching %s\n" % text)
                            for lc in locs:
                                stdscr.addstr("Location: %s\n" % lc.disp(True))
                                stdscr.addstr("Links:\n")
                                types = ["road", "rail", "boat"]
                                for link in lc.links:
                                    other = game.locations[link.b if link.a == lc.index else link.a]
                                    stdscr.addstr("\t%s to %s" % (types[link.t-1].upper(), other.disp(True)))
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
                game.ended = True
                return
        if print_turns:
            stdscr.addstr("###########################\n")
            stdscr.addstr("######## Turn %4d ########\n" % (actualTurn+1))
            stdscr.addstr("###########################\n")
    player = -1
    for i in range(5):
        if play[0] == game.players[i].letter:
            player = i
    if player == -1:
        stdscr.addstr("Invalid player: " + play[0] + "!\n")
        game.lastValid = False
        return
    p = game.players[player]

    abbrev = play[1] + play[2]
    place  = -1

    for i in range(len(drac_common.abbrevs)):
        if abbrev == drac_common.abbrevs[i]:
            place = i

    special = False

    if abbrev in drac_common.specials:
        special = True

    if special and p.letter != 'D':
        special = False

    if p.letter == 'D' and place >= 0 and place < len(game.locations) and game.locations[place].abbrev == 'JM':
        place = -1;
        special = False

    if place == -1 and not special:
        stdscr.addstr("Invalid location for " + p.name + ": " + abbrev + "!\n")
        game.turn += 1
        game.lastValid = False
        return

    loc = game.locations[place] if place >= 0 else None

    if p.letter == 'G' or p.letter == 'D':
        for l in game.locations:
            if p.letter == 'D':
                for trap in l.traps:
                    if trap.expires == actualTurn-1:
                        l.traps.remove(trap)
                        stdscr.addstr("%17s vanishes from %s.\n" % ("A trap", l.disp(False)))
            else:
                for vamp in l.vampires:
                    if vamp.matures == actualTurn-1:
                        game.score -= 13
                        l.vampires.remove(vamp)
                        stdscr.addstr("%17s matures in %s! (score -13)\n" % ("A vampire", l.disp(False)))

    if p.letter == 'D':
        trap    = True
        vampire = actualTurn > 0 and actualTurn % 13 == 12
        action  = play[5]

        if special:
            if abbrev == 'TP':
                p.prevLoc  = p.location
                p.location = game.locations[17]
            elif abbrev == 'HI':
                p.prevLoc = p.location
                stdscr.addstr("%17s hides in %s.\n" % ("Dracula", p.location.disp(False)))
            elif abbrev[0] == 'D':
                back = int(abbrev[1])
                if back <= len(game.trail.locs):
                    p.prevLoc  = p.location
                    p.location = game.locations[game.trail.locs[back-1]]
        else:
            if p.prevLoc is not None:
                if not drac_links.haslink(game, p.location.index, loc.index, p, 1) and not drac_links.haslink(game, p.location.index, loc.index, p, 3):
                    stdscr.addstr("%17s has an invalid move (no links %s -> %s\n)" % (p.name, p.prevLoc.disp(False), game.get_location(play[1:2])))
                    game.turn += 1
                    game.lastValid = False
                    return
            p.prevLoc  = p.location
            p.location = loc
            if p.prevLoc == p.location:
                stdscr.addstr("%17s stays in %s.\n" % ("Dracula", p.location.disp(False)))
            else:
                if p.prevLoc is None:
                    stdscr.addstr("%17s begins in %s.\n" % ("Dracula", p.location.disp(False)))
                else:
                    stdscr.addstr("%17s moves %s -> %s.\n" % ("Dracula", p.prevLoc.disp(False), p.location.disp(False)))

        if trap and not p.location.index in drac_common.seas and len(p.location.traps) < 3:
            t         = drac_common.Trap()
            t.expires = actualTurn + 6
            p.location.traps.append(t)
            stdscr.addstr("%17s drops off a trap in %s.\n" % ("Dracula", p.location.disp(False)))

        if vampire and not p.location.index in drac_common.seas and len(p.location.vampires) == 0:
            v         = drac_common.Vampire()
            v.matures = actualTurn + 6
            p.location.vampires.append(v)
            stdscr.addstr("%17s makes a vampire at %s.\n" % ("Dracula", p.location.disp(False)))
        if p.location.abbrev == "CD":
            prevHealth = p.health
            p.health += 10
            stdscr.addstr("%17s stays at Castle Dracula. +10 BP (%d -> %d)\n" % ("Dracula", prevHealth, p.health))

        game.trail.locs.insert(0, p.location.index)
        if len(game.trail.locs) > 5:
            game.trail.locs.remove(game.trail.locs[5])

        if p.location.index in drac_common.seas:
            p.health -= 2
            stdscr.addstr("%17s takes 2 damage from the %s. (%d remaining)\n" % ("Dracula", p.location.disp(False), p.health))

        game.score -= 1
        stdscr.addstr("%17s ended turn. (score -1)\n" % "Dracula")

    else:

        if p.location is not None and p.location.index == 60 and p.health <= 0:
            p.health = 9

        if p.location is not None:
            if not drac_links.hasraillink(game, p.location.index, loc.index, p, (actualTurn+p.index)%4) and not drac_links.haslink(game, p.location.index, loc.index, p, 1) and not drac_links.haslink(game, p.location.index, loc.index, p, 3):
                stdscr.addstr("%17s has an invalid move: %s\n" % (p.name, play))
                game.turn += 1
                game.lastValid = False
                return

        p.prevLoc  = p.location
        p.location = loc

        if p.prevLoc == p.location:
            health = p.health
            p.health = min(p.health + 3, 9)
            dhealth = p.health - health
            if dhealth > 0:
                stdscr.addstr("%17s stays in %s. +%d HP (%d -> %d)\n" % (p.name, p.location.disp(False), dhealth, health, p.health))
            else:
                stdscr.addstr("%17s stays in %s.\n" % (p.name, p.location.disp(False)))
        else:
            if p.prevLoc is None:
                stdscr.addstr("%17s begins in %s.\n" % (p.name, p.location.disp(False)))
            else:
                stdscr.addstr("%17s moves %s -> %s.\n" % (p.name, p.prevLoc.disp(False), p.location.disp(False)))

            if p.location.index in game.trail.locs:
                stdscr.addstr("%17s finds %s on Dracula's trail!\n" % (p.name, p.location.disp(False)))

        hunt_health = p.health
        drac_health = game.players[4].health

        for trap in p.location.traps:
            p.health -= 2
            if p.health > 0:
                p.location.traps.remove(trap)

        for vamp in p.location.vampires:
            if p.health > 0:
                p.location.vampires.remove(vamp)

        if p.health > 0 and p.location == game.players[4].location:
            stdscr.addstr("%17s finds %s in %s! A skirmish follows!\n" % (p.name, "Dracula", p.location.disp(False)))
            p.health -= 4
            game.players[4].health -= 10

        hunt_dhealth = hunt_health - p.health
        drac_dhealth = drac_health - game.players[4].health

        if hunt_dhealth > 0:
            stdscr.addstr("%17s takes %d damage! (%d remaining)\n" % (p.name, hunt_dhealth, p.health if p.health >= 0 else 0))
        if drac_dhealth > 0:
            stdscr.addstr("%17s takes %d damage! (%d remaining)\n" % ("Dracula", drac_dhealth, game.players[4].health if game.players[4].health >= 0 else 0))

        if p.health <= 0:
            p.health = 0
            game.score -= 6
            p.location = game.locations[60]
            stdscr.addstr("%17s dies, and is reborn at St Joseph and St Marys (JM).\n" % p.name)

    if game.players[4].health <= 0:
        stdscr.addstr("\n\nDracula died! Hunters win!\n")
        stdscr.addstr("Dracula died! Hunters win!\n")
        stdscr.addstr("Dracula died! Hunters win!\n")
        stdscr.addstr("Dracula died! Hunters win!\n\n")
        game.ended = True
        return

    game.turn += 1
