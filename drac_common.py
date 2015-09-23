import drac_listener

players   = ['G', 'S', 'H', 'M', 'D']
seas      = [0, 4, 7, 10, 23, 32, 33, 43, 48, 64]
specials  = ['HI', 'TP', 'D1', 'D2', 'D3', 'D4', 'D5']
names     = ["Lord Godalming", "Dr. Seward", "Dr. Van Helsing", "Mina Harker", "Dracula"]
abbrevs   = ["AS", "AL", "AM", "AT", "AO", "BA", "BI", "BB", "BE", "BR", "BS", "BO", "BU", "BC", "BD", "CA", "CG", "CD", "CF", "CO", "CN", "DU", "ED", "EC", "FL", "FR", "GA", "GW", "GE", "GO", "GR", "HA", "IO", "IR", "KL", "LI", "LE", "LS", "LV", "LO", "MA", "MN", "MR", "MS", "MI", "MU", "NA", "NP", "NS", "NU", "PA", "PL", "PR", "RO", "SA", "SN", "SR", "SJ", "SO", "JM", "ST", "SW", "SZ", "TO", "TS", "VA", "VR", "VE", "VI", "ZA", "ZU"]
places    = ["adriatic_sea", "alicante", "amsterdam", "athens", "atlantic_ocean", "barcelona", "bari", "bay_of_biscay", "belgrade", "berlin", "black_sea", "bordeaux", "brussels", "bucharest", "budapest", "cadiz", "cagliari", "castle_dracula", "clermont_ferrand", "cologne", "constanta", "dublin", "edinburgh", "english_channel", "florence", "frankfurt", "galatz", "galway", "geneva", "genoa", "granada", "hamburg", "ionian_sea", "irish_sea", "klausenburg", "leipzig", "le_havre", "lisbon", "liverpool", "london", "madrid", "manchester", "marseilles", "mediterranean_sea", "milan", "munich", "nantes", "naples", "north_sea", "nuremburg", "paris", "plymouth", "prague", "rome", "salonica", "santander", "saragossa", "sarajevo", "sofia", "st_joseph_and_st_marys", "strasbourg", "swansea", "szeged", "toulouse", "tyrrhenian_sea", "valona", "varna", "venice", "vienna", "zagreb", "zurich"]

valid_modes = ["p", "plays", "t", "turns", "i", "interactive", "n", "networked", "g", "pygame", "ai", "ai_mode"]

class Trap:
    expires  = 0

class Vampire:
    matures  = 0

class Location:
    index    = 0
    name     = ''
    abbrev   = ''
    traps    = []
    vampires = []
    links    = []
    def disp(self, ident):
        if ident:
            return "%s (%s) (%d)" % (self.name, self.abbrev, self.index)
        else:
            return "%s (%s)" % (self.name, self.abbrev)

class Player:
    index    = -1
    letter   = 'D'
    name     = 'Dracula'
    location = None
    prevLoc  = None
    health   = 9

class DracTrail:
    locs     = []

class Game:
    turn      = 0
    lastTurn  = -1
    score     = 366
    players   = []
    locations = []
    trail     = None
    links     = False
    ended     = False
    lastValid = True
    listener  = drac_listener.SimpleListener()

    def get_location(i):
        for loc in game.locations:
            if loc.name == str(i) or loc.abbrev == str(i) or str(loc.index) == str(i):
                return loc