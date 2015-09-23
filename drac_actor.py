import drac_common
import drac_links


def do_turn(stdscr, game, play):

    if game.turn == 0:
        game.listener.on_game_start(game)

    game.lastValid = True

    while len(play) < 3:
        play = play + "."

    if game.score <= 0:
        game.listener.on_dracula_win(game)
        game.ended = True
        return

    actualTurn = game.turn / 5
    if actualTurn > game.lastTurn:
        game.lastTurn = actualTurn
        game.listener.on_turn_start(game)

    player = -1
    for i in range(5):
        if play[0] == game.players[i].letter:
            player = i

    if player == -1:
        game.listener.on_invalid_player(game, play[0])
        game.lastValid = False
        return

    p = game.players[player]

    abbrev = play[1] + play[2]
    place = -1

    for i in range(len(drac_common.abbrevs)):
        if abbrev == drac_common.abbrevs[i]:
            place = i

    special = False

    if abbrev in drac_common.specials:
        special = True

    if special and p.letter != 'D':
        special = False

    if p.letter == 'D' and place >= 0 and place < len(game.locations) and game.locations[place].abbrev == 'JM':
        game.listener.on_invalid_move_cant_go(game, player, player.location.disp(False), game.locations[place].disp(False))
        game.lastValid = False
        return

    if place == -1 and not special:
        game.listener.on_invalid_move_unknown(game, player, place)
        game.lastValid = False
        return

    loc = game.locations[place] if place >= 0 else None

    if p.letter == 'G' or p.letter == 'D':
        for l in game.locations:
            if p.letter == 'D':
                for trap in l.traps:
                    if trap.expires == actualTurn - 1:
                        l.traps.remove(trap)
                        game.listener.on_trap_vanish(game, l)
            else:
                for vamp in l.vampires:
                    if vamp.matures == actualTurn - 1:
                        game.score -= 13
                        l.vampires.remove(vamp)
                        game.listener.on_vampire_mature(game, l)

    if p.letter == 'D':
        trap = True
        vampire = actualTurn % 13 == 0
        action = ""  # play[5]

        if special:
            if abbrev == 'TP':
                p.prevLoc = p.location
                p.location = game.locations[17]
            elif abbrev == 'HI':
                p.prevLoc = p.location
                game.listener.on_player_stay(game, p, p.location, 0)
            elif abbrev[0] == 'D':
                back = int(abbrev[1])
                if back <= len(game.trail.locs):
                    p.prevLoc = p.location
                    p.location = game.locations[game.trail.locs[back - 1]]
        else:
            if p.prevLoc is not None:
                if not drac_links.haslink(game, p.location.index, loc.index, p, 1) and not drac_links.haslink(game, p.location.index, loc.index, p, 3):
                    game.listener.on_invalid_move_links(game, p, p.location, game.get_location(play[1:2]))
                    game.lastValid = False
                    return
            if p.location == loc:
                game.listener.on_invalid_move_dracula_stay(game, p, p.location)
                game.lastValid = False
                return
            else:
                if p.location is None:
                    game.listener.on_player_begin(game, p, loc)
                else:
                    game.listener.on_player_move(game, p, p.location, loc)

            p.prevLoc = p.location
            p.location = loc

        if trap and not vampire and p.location.index not in drac_common.seas and len(p.location.traps) < 3:
            t = drac_common.Trap()
            t.expires = actualTurn + 6
            p.location.traps.append(t)
            game.listener.on_trap_place(game, p.location)

        if vampire and p.location.index not in drac_common.seas and len(p.location.vampires) == 0:
            v = drac_common.Vampire()
            v.matures = actualTurn + 6
            p.location.vampires.append(v)
            game.listener.on_vampire_place(game, p.location)

        if p.location.abbrev == "CD":
            prevHealth = p.health
            p.health += 10
            game.listener.on_stay_castle_dracula(game, p)

        game.trail.locs.insert(0, p.location.index)
        if len(game.trail.locs) > 5:
            game.trail.locs.remove(game.trail.locs[5])

        if p.location.index in drac_common.seas:
            p.health -= 2
            game.listener.on_dracula_water_damage(game, p, p.location)

        game.score -= 1
        game.listener.on_turn_end(game)

    else:

        if p.location is not None and p.location.index == 60 and p.health <= 0:
            p.health = 9

        if p.location is not None:
            if not drac_links.hasraillink(game, p.location.index, loc.index, p, (actualTurn + p.index) % 4) and not drac_links.haslink(game, p.location.index, loc.index, p, 1) and not drac_links.haslink(game, p.location.index, loc.index, p, 3):
                game.listener.on_invalid_move_links(game, p, p.location, loc)
                game.lastValid = False
                return

        p.prevLoc = p.location
        p.location = loc

        if p.prevLoc == p.location:
            health = p.health
            p.health = min(p.health + 3, 9)
            dhealth = p.health - health
            game.listener.on_player_stay(game, p, p.location, dhealth)
        else:
            if p.prevLoc is None:
                game.listener.on_player_begin(game, p, p.location)
            else:
                game.listener.on_player_move(game, p, p.prevLoc, p.location)

            if p.location.index in game.trail.locs:
                game.listener.on_hunter_find_trail(game, p, p.location)

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
            p.health -= 4
            game.players[4].health -= 10
            game.listener.on_hunter_find_dracula(game, p, p.location)

        hunt_dhealth = hunt_health - p.health
        drac_dhealth = drac_health - game.players[4].health

        if hunt_dhealth > 0:
            game.listener.on_player_damage(game, p, hunt_dhealth, p.health if p.health >= 0 else 0)
        if drac_dhealth > 0:
            game.listener.on_player_damage(game, game.players[4], drac_dhealth, game.players[4].health if game.players[4].health >= 0 else 0)

        if p.health <= 0:
            p.health = 0
            game.score -= 6
            p.location = game.locations[60]
            game.listener.on_hunter_respawn(game, p)

    if game.players[4].health <= 0:
        game.listener.on_hunters_win(game)
        game.ended = True
        return

    game.turn += 1
