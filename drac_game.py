import drac_common
import drac_config


game = drac_common.Game()
game.trail = drac_common.DracTrail()
game.trail.locs = []
game.players = []
game.locations = []

for i in range(len(drac_common.places)):
    l = drac_common.Location()
    l.index = i
    name = ''
    for j in range(len(drac_common.places[i])):
        if j == 0 or drac_common.places[i][j - 1] == '_':
            name += drac_common.places[i][j].capitalize()
        elif drac_common.places[i][j] == '_':
            name += ' '
        else:
            name += drac_common.places[i][j]
    l.name = name
    l.abbrev = drac_common.abbrevs[i]
    l.traps = []
    l.vampires = []
    l.links = []
    game.locations.append(l)

for i in range(5):
    p = drac_common.Player()
    p.index = i
    p.letter = drac_common.players[i]
    p.name = drac_common.names[i]
    p.prevLoc = None
    p.location = None
    p.health = 40 if drac_common.players[i] == 'D' else 9
    game.players.append(p)

if drac_config.links:
    try:
        import drac_links
    except ImportError:
        drac_links = None
else:
    drac_links = None

if drac_links is not None:
    try:
        drac_links.addlinks(game)
        game.links = True
    except Exception:
        pass

game.drac_links = drac_links
