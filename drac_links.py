class Link:
    a = -1
    b = -1
    t = -1


def haslink(game, a, b, p, t):
    if p is not None and p.index == 4:
        if game.locations[a].abbrev == 'JM' or game.locations[b].abbrev == 'JM':
            return False
    if a == b or not game.links:
        return True
    for link in game.locations[min(a, b)].links:
        if link.t == t and link.b == max(a, b):
            return True
    return False


def hasraillink(game, a, b, p, length):
    if p is not None and p.index == 4:
        return False
    loca = game.locations[min(a, b)]
    if a == b:
        return True
    if length >= 1:
        if haslink(game, a, b, p, 2):
            return True
    if length >= 2:
        for link in loca.links:
            if link.t == 2 and haslink(game, link.a if link.b == a else link.b, max(a, b), p, 2):
                return True
    if length >= 3:
        for link in loca.links:
            if link.t == 2:
                for link_ in game.locations[link.a if link.a != a else link.b].links:
                    if link_.t == 2 and haslink(game, link_.a if link_.b == a else link_.b, max(a, b), p, 2):
                        return True
    return False


def hasanylink(game, a, b, p, max_rails):
    return haslink(game, a, b, p, 1) or hasraillink(game, a, b, p, max_rails) or haslink(game, a, b, p, 3)


def addlink(game, a, b, t):
    link = Link()
    link.a = min(a, b)
    link.b = max(a, b)
    link.t = t
    game.locations[link.a].links.append(link)
    game.locations[link.b].links.append(link)


def addlinks(game):
    addlink(game, 0, 6, 3)
    addlink(game, 0, 32, 3)
    addlink(game, 0, 67, 3)

    addlink(game, 1, 5, 2)
    addlink(game, 1, 30, 1)
    addlink(game, 1, 40, 1)
    addlink(game, 1, 40, 2)
    addlink(game, 1, 43, 3)
    addlink(game, 1, 56, 1)

    addlink(game, 2, 12, 1)
    addlink(game, 2, 19, 1)
    addlink(game, 2, 48, 3)

    addlink(game, 3, 32, 3)
    addlink(game, 3, 65, 1)

    addlink(game, 4, 7, 3)
    addlink(game, 4, 15, 3)
    addlink(game, 4, 23, 3)
    addlink(game, 4, 27, 3)
    addlink(game, 4, 33, 3)
    addlink(game, 4, 37, 3)
    addlink(game, 4, 43, 3)
    addlink(game, 4, 48, 3)

    addlink(game, 5, 43, 3)
    addlink(game, 5, 56, 1)
    addlink(game, 5, 56, 2)
    addlink(game, 5, 63, 1)

    addlink(game, 6, 47, 1)
    addlink(game, 6, 47, 2)
    addlink(game, 6, 53, 1)

    addlink(game, 7, 11, 3)
    addlink(game, 7, 46, 3)
    addlink(game, 7, 55, 3)

    addlink(game, 8, 13, 1)
    addlink(game, 8, 34, 1)
    addlink(game, 8, 57, 1)
    addlink(game, 8, 58, 1)
    addlink(game, 8, 58, 2)
    addlink(game, 8, 59, 1)
    addlink(game, 8, 62, 1)
    addlink(game, 8, 62, 2)

    addlink(game, 9, 31, 1)
    addlink(game, 9, 31, 2)
    addlink(game, 9, 35, 1)
    addlink(game, 9, 35, 2)
    addlink(game, 9, 52, 1)
    addlink(game, 9, 52, 2)

    addlink(game, 10, 20, 3)
    addlink(game, 10, 32, 3)
    addlink(game, 10, 66, 3)

    addlink(game, 11, 18, 1)
    addlink(game, 11, 46, 1)
    addlink(game, 11, 50, 2)
    addlink(game, 11, 56, 1)
    addlink(game, 11, 56, 2)
    addlink(game, 11, 63, 1)

    addlink(game, 12, 19, 1)
    addlink(game, 12, 19, 2)
    addlink(game, 12, 36, 1)
    addlink(game, 12, 50, 1)
    addlink(game, 12, 50, 2)
    addlink(game, 12, 60, 1)

    addlink(game, 13, 20, 1)
    addlink(game, 13, 20, 2)
    addlink(game, 13, 26, 1)
    addlink(game, 13, 26, 2)
    addlink(game, 13, 34, 1)
    addlink(game, 13, 58, 1)
    addlink(game, 13, 62, 2)

    addlink(game, 14, 34, 1)
    addlink(game, 14, 62, 1)
    addlink(game, 14, 62, 2)
    addlink(game, 14, 68, 1)
    addlink(game, 14, 68, 2)
    addlink(game, 14, 69, 1)

    addlink(game, 15, 30, 1)
    addlink(game, 15, 37, 1)
    addlink(game, 15, 40, 1)

    addlink(game, 16, 43, 3)
    addlink(game, 16, 64, 3)

    addlink(game, 17, 26, 1)
    addlink(game, 17, 34, 1)

    addlink(game, 18, 28, 1)
    addlink(game, 18, 42, 1)
    addlink(game, 18, 46, 1)
    addlink(game, 18, 50, 1)
    addlink(game, 18, 63, 1)

    addlink(game, 19, 25, 1)
    addlink(game, 19, 25, 2)
    addlink(game, 19, 31, 1)
    addlink(game, 19, 35, 1)
    addlink(game, 19, 60, 1)

    addlink(game, 20, 26, 1)
    addlink(game, 20, 66, 1)

    addlink(game, 21, 27, 1)
    addlink(game, 21, 33, 3)

    addlink(game, 22, 41, 1)
    addlink(game, 22, 41, 2)
    addlink(game, 22, 48, 3)

    addlink(game, 23, 36, 3)
    addlink(game, 23, 39, 3)
    addlink(game, 23, 48, 3)
    addlink(game, 23, 51, 3)

    addlink(game, 24, 29, 1)
    addlink(game, 24, 44, 2)
    addlink(game, 24, 53, 1)
    addlink(game, 24, 53, 2)
    addlink(game, 24, 67, 1)

    addlink(game, 25, 35, 1)
    addlink(game, 25, 35, 2)
    addlink(game, 25, 49, 1)
    addlink(game, 25, 60, 1)
    addlink(game, 25, 60, 2)

    addlink(game, 26, 34, 1)

    addlink(game, 28, 42, 1)
    addlink(game, 28, 44, 2)
    addlink(game, 28, 50, 1)
    addlink(game, 28, 60, 1)
    addlink(game, 28, 70, 1)

    addlink(game, 29, 42, 1)
    addlink(game, 29, 44, 1)
    addlink(game, 29, 44, 2)
    addlink(game, 29, 64, 3)
    addlink(game, 29, 67, 1)

    addlink(game, 30, 40, 1)

    addlink(game, 31, 35, 1)
    addlink(game, 31, 48, 3)

    addlink(game, 32, 54, 3)
    addlink(game, 32, 64, 3)
    addlink(game, 32, 65, 3)

    addlink(game, 33, 38, 3)
    addlink(game, 33, 61, 3)

    addlink(game, 34, 62, 1)

    addlink(game, 36, 46, 1)
    addlink(game, 36, 50, 1)
    addlink(game, 36, 50, 2)

    addlink(game, 35, 49, 1)
    addlink(game, 35, 49, 2)

    addlink(game, 37, 40, 1)
    addlink(game, 37, 40, 2)
    addlink(game, 37, 55, 1)

    addlink(game, 38, 41, 1)
    addlink(game, 38, 41, 2)
    addlink(game, 38, 61, 1)

    addlink(game, 39, 41, 1)
    addlink(game, 39, 41, 2)
    addlink(game, 39, 51, 1)
    addlink(game, 39, 61, 1)
    addlink(game, 39, 61, 2)

    addlink(game, 40, 55, 1)
    addlink(game, 40, 55, 2)
    addlink(game, 40, 56, 1)
    addlink(game, 40, 56, 2)

    addlink(game, 42, 43, 3)
    addlink(game, 42, 44, 1)
    addlink(game, 42, 50, 2)
    addlink(game, 42, 63, 1)
    addlink(game, 42, 70, 1)

    addlink(game, 43, 64, 3)

    addlink(game, 44, 45, 1)
    addlink(game, 44, 67, 1)
    addlink(game, 44, 70, 1)
    addlink(game, 44, 70, 2)

    addlink(game, 45, 49, 1)
    addlink(game, 45, 49, 2)
    addlink(game, 45, 60, 1)
    addlink(game, 45, 67, 1)
    addlink(game, 45, 68, 1)
    addlink(game, 45, 69, 1)
    addlink(game, 45, 70, 1)

    addlink(game, 46, 50, 1)

    addlink(game, 47, 53, 1)
    addlink(game, 47, 53, 2)
    addlink(game, 47, 64, 3)

    addlink(game, 49, 52, 1)
    addlink(game, 49, 60, 1)

    addlink(game, 50, 60, 1)

    addlink(game, 52, 68, 1)
    addlink(game, 52, 68, 2)

    addlink(game, 53, 64, 3)

    addlink(game, 54, 58, 1)
    addlink(game, 54, 58, 2)
    addlink(game, 54, 65, 1)

    addlink(game, 55, 56, 1)

    addlink(game, 56, 63, 1)

    addlink(game, 57, 58, 1)
    addlink(game, 57, 59, 1)
    addlink(game, 57, 65, 1)
    addlink(game, 57, 69, 1)

    addlink(game, 58, 65, 1)
    addlink(game, 58, 66, 1)
    addlink(game, 58, 66, 2)

    addlink(game, 59, 62, 1)
    addlink(game, 59, 69, 1)

    addlink(game, 60, 70, 1)
    addlink(game, 60, 70, 2)

    addlink(game, 62, 69, 1)

    addlink(game, 67, 68, 2)

    addlink(game, 68, 69, 1)
