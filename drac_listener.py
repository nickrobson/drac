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

class Listener:
    def on_game_start(self, game):
        return
    def on_dracula_win(self, game):
        return
    def on_hunters_win(self, game):
        return

    def on_turn_start(self, game):
        return
    def on_turn_end(self, game):
        return

    def on_invalid_player(self, game, player):
        return
    def on_invalid_move_unknown(self, game, player, move):
        return
    def on_invalid_move_links(self, game, player, fro, to):
        return

    def on_trap_place(self, game, loc):
        return
    def on_trap_vanish(self, game, loc):
        return
    def on_vampire_place(self, game, loc):
        return
    def on_vampire_mature(self, game, loc):
        return

    def on_hunter_find_trail(self, game, player, loc):
        return
    def on_hunter_find_dracula(self, game, player, loc):
        return
    def on_hunter_damage(self, game, player, damage, old_health, new_health):
        return
    def on_hunter_respawn(self, game, player):
        return

    def on_player_begin(self, game, player, loc):
        return
    def on_player_move(self, game, player, fro, to):
        return
    def on_player_stay(self, game, player, loc, heal):
        return

    def on_dracula_water_damage(self, game, loc):
        return

class SimpleListener(Listener):

    stdscr = None

    def __init__(self, stdscr=None):
        self.stdscr = stdscr if stdscr is not None else dummy_stdscr()

    def on_game_start(self, game):
        return
    def on_dracula_win(self, game):
        self.stdscr.addstr("\n\nScore hit 0! Dracula wins!\n")
        self.stdscr.addstr("Score hit 0! Dracula wins!\n")
        self.stdscr.addstr("Score hit 0! Dracula wins!\n")
        self.stdscr.addstr("Score hit 0! Dracula wins!\n\n")
    def on_hunters_win(self, game):
        self.stdscr.addstr("\n\nDracula died! Hunters win!\n")
        self.stdscr.addstr("Dracula died! Hunters win!\n")
        self.stdscr.addstr("Dracula died! Hunters win!\n")
        self.stdscr.addstr("Dracula died! Hunters win!\n\n")

    def on_turn_start(self, game):
        self.stdscr.addstr("###########################\n")
        self.stdscr.addstr("######## Turn %4d ########\n" % (game.turn/5))
        self.stdscr.addstr("###########################\n")
    def on_turn_end(self, game):
        self.stdscr.addstr("%17s ended turn. (score -1)\n" % "Dracula")

    def on_invalid_player(self, game, player):
        self.stdscr.addstr("Invalid player: %s!\n" % player)
    def on_invalid_move_unknown(self, game, player, move):
        self.stdscr.addstr("Invalid location for %s: %s!\n" % (player.name, move))
    def on_invalid_move_links(self, game, player, fro, to):
        self.stdscr.addstr("%17s has an invalid move (no links %s -> %s\n)" % (p.name, fro.disp(False), to.disp(False)))

    def on_trap_place(self, game, loc):
        self.stdscr.addstr("%17s drops off a trap in %s.\n" % ("Dracula", loc.disp(False)))
    def on_trap_vanish(self, game, loc):
        self.stdscr.addstr("%17s vanishes from %s.\n" % ("A trap", loc.disp(False)))
    def on_vampire_place(self, game, loc):
        self.stdscr.addstr("%17s makes a vampire at %s.\n" % ("Dracula", loc.disp(False)))
    def on_vampire_mature(self, game, loc):
        self.stdscr.addstr("%17s matures in %s! (score -13)\n" % ("A vampire", loc.disp(False)))

    def on_hunter_find_trail(self, game, player, loc):
        self.stdscr.addstr("%17s finds %s on Dracula's trail!\n" % (player.name, loc.disp(False)))
    def on_hunter_find_dracula(self, game, player, loc):
        self.stdscr.addstr("%17s finds %s in %s! A skirmish follows!\n" % (player.name, "Dracula", loc.disp(False)))
    def on_hunter_damage(self, game, player, damage, old_health, new_health):
        self.stdscr.addstr("%17s takes %d damage! (%d remaining)\n" % (player.name, min(old_health, damage), max(0, new_health)))
    def on_hunter_respawn(self, game, player):
        self.stdscr.addstr("%17s dies, and is reborn at %s.\n" % (player.name, game.locations[59].disp(False)))

    def on_player_begin(self, game, player, loc):
        self.stdscr.addstr("%17s begins in %s.\n" % (player.name, loc.disp(False)))
    def on_player_move(self, game, player, fro, to):
        self.stdscr.addstr("%17s moves %s -> %s.\n" % ("Dracula", fro.disp(False), to.location.disp(False)))
    def on_player_stay(self, game, player, loc, heal):
        if player.index == 4 and loc.abbrev == 'CD':
            self.stdscr.addstr("%17s stays at Castle Dracula. +10 BP (%d -> %d)\n" % (player.name, max(0, player.health - heal), player.health))
        else:
            self.stdscr.addstr("%17s stays in %s.\n" % (player.name, loc.disp(False)))

    def on_dracula_water_damage(self, game, player, loc):
        self.stdscr.addstr("%17s takes 2 damage from the %s. (%d remaining)\n" % (player.name, loc.disp(False), max(0, p.health)))