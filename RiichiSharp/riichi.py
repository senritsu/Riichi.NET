

tile_short_map = {"numerical":{"m":"Man","p":"Pin","s":"Sou"},
                     "honors":{"t":"Ton","n":"Nan","x":"Xia","p":"Pei","w":"Haku","g":"Hatsu","r":"Chun"}}

ex1 = "11122334444WWW"
a = "111 234 234 44 WWW"
b = "11 123 234 444 WWW"
ex2 = "111222333777HH"
a = "111 222 333 777 HH"
b = "123 123 123 777 HH"

WINDS = ["Ton","Nan","Xia","Pei"]
DRAGONS = ["Haku","Hatsu","Chun"]
NUMERALS = range(1,10)
SUITS = ["Man","Pin","Sou"]

YAKU_VALUES = {"Riichi":1,"Menzen Tsumo":1,"Ippatsu":1,"Chankan":1,"Rinshan Kaihou":1,"Haitei Raoyue":1,"Houtei Raoyui":1,"Pinfu":1,"Iipeikou":1,"Tan'yao":1,"Yakuhai":1,"Kazepai":1,
                "Daburiichi":2,"Open Riichi":2,"Dabukaze":2,"Chii Toitsu":2,"Sanshoku Doujun":2,"Ittsuu":2,"Toitoi":2,"Sanshoku Doukou":2,"San Ankou":2,"San Kantsu":2,"Chanta":2,
                "Hon'itsu":3,"Junchan":3,"Ryanpeikou":3,
                "Honrou":4,"Shousangen":4,
                "Chin'itsu":6}
YAKU_REDUCED = ["Sanshoku Doujun","Ittsuu","Chanta","Hon'itsu","Junchan","Chin'itsu"]
YAKUMAN = ["Tenhou","Chihou","Renhou","Kokushi Musou","Chuuren Poutou","Suu Ankou","Daisangen","Shousuushi","Suu Kantsu","Ryuuisou","Tsuuisou","Chinroutou","Daisharin"]
DOUBLE_YAKUMAN = ["Kokushi Musou (13)","Chuuren Poutou (9)","Daisuushi","Daichisei","Paarenchan"]

class MahjongHand(object):
    def __init__(self, melds, winningTile = None):
        self.melds = melds
        self.tiles = [tile for meld in melds for tile in meld.tiles]
        self.yakuList = []
        self.dora = 0
        self.uradora = 0
        self.closed = all([tile.closed or tile is winningTile for meld in melds for tile in meld])

    def fu(self):
        return self.fu

    def han(self):
        han = sum([YAKU_VALUES[yaku[:yaku.index(" (")-1]] - 1*(yaku in YAKU_REDUCED and not self.closed) for yaku in self.yakuList if yaku[:yaku.index(" (")-1] in YAKU_VALUES])
        han += self.dora + self.uradora
        han = min(2+han,13)

        yakuman = len(set(YAKUMAN).intersection(self.yakuList)) + 2 * len(set(DOUBLE_YAKUMAN).intersection(self.yakuList))
        if yakuman >= 2:
            han = 14
        elif yakuman:
            han = 13

        return han

    def recalculate(self, roundWind, seatWind, dora = [], uradora = [], riichi = 0, tsumo = False, ippatsu = False, kan = False, tileTiming = 0):
        self.fu = 20
        dora = map(Tile,dora)
        uradora = map(Tile,uradora)

        self.dora = sum([dora.count(tile) for tile in self.tiles])
        self.uradora = sum([uradora.count(tile) for tile in self.tiles])

        yaku = []

        if tsumo and self.closed:
            yaku.append("Menzen Tsumo")
        if riichi >= 2:
            if self.closed:
                yaku.append("Daburiichi")
            else:
                yaku.append("Open Riichi")
        elif riichi:
            yaku.append("Riichi")
        if riichi and ippatsu:
            yaku.append("Ippatsu")
        if kan:
            if self.closed:
                yaku.append("Chankan")
            else:
                yaku.append("Rinshan Kaihou")
        if tileTiming == -1:
            if tsumo:
                yaku.append("Haitei Raoyui")
            else:
                yaku.append("Houtei Raoyui")
        elif tileTiming == 1:
            if seatWind.name == "Ton" and self.closed:
                yaku.append("Tenhou")
            elif self.closed:
                yaku.append("Chihou")
            else:
                yaku.append("Renhou")
        if all([type(meld) == Sequence or type(meld) == Pair for meld in solution]) and self.closed:
            yaku.append("Pinfu")
        if all([not meld.honors() and not meld.terminals() for meld in solution]):
            yaku.append("Tan'yao")

        ankou = len([meld for meld in solution if type(meld) == Triplet and meld.closed()])
        kan = len([meld for meld in solution if type(meld) == Quad])

        if ankou >= 4:
            yaku.append("Suu Ankou")
        elif ankou >= 3:
            yaku.append("San Ankou")
        if kan >= 4:
            yaku.append("Suu Kantsu")
        elif kan >= 3:
            yaku.append("San Kantsu")

        itsuu = False
        for suit in SUITS:
            valid = True
            for i in range(3):
                meld = Sequence()
                for j in range(1,4):
                    meld.extend([SuitTile("{0}{1}".format(j+i*3,suit))])
                if meld not in self.melds:
                    valid = False
            if valid:
                ittsuu = True
                break
        if itsuu:
            yaku.append("Ittsuu")

        dragon_triplets = [meld for meld in self.melds if type(meld) in [Quad,Triplet] and meld.tiles[0].name in DRAGONS]
        dragon_pair = any([meld.tiles[0].name in DRAGONS for meld in self.melds if type(meld) == Pair])
        if len(dragon_triplets) >= 3:
            yaku.append("Daisangen")
        elif len(dragon_triplets) >= 2 and dragon_pair:
            yaku.append("Shousangen")

        iipeikou = 0
        iipeikou_checked = []
        sanshoku_doujun = False
        sanshoku_douko = False
        yakuhai = []
        seen_suits = []
        honors = False
        for meld in self.melds:
            suit = meld.tiles[0].suit
            if suit is None:
                honors = True
            elif suit not in seen_suits:
                seen_suits.append(suit)

            if self.closed and type(meld) == Sequence and meld not in iipeikou_checked:
                if self.melds.count(meld) >= 4:
                    iipeikou += 2
                elif  self.melds.count(meld) >= 2:
                    iipeikou += 1
                iipeikou_checked.append(meld)

            if type(meld) in [Triplet,Sequence] and not meld.honors():
                sanshoku = True
                tiles = meld.tiles
                new = [[type(tiles[0])("%s%s"%(tile.rank,SUITS[(SUITS.index(suit)+1)%3])) for tile in tiles] for i in range(2)]
                for suit in new:
                    sequence = Sequence()
                    while suit:
                        if not sequence.extend(suit):
                            break
                    if sequence not in solution:
                        sanshoku = False
                if sanshoku:
                    if type(meld) == Sequence:
                        sanshoku_doujun = True
                    elif type(meld) == Triplet:
                        sanshoku_douko = True

            if type(meld) in [Triplet,Quad] and meld.honorsOnly():
                name = meld.tiles[0].name
                if name in DRAGONS and not ("Daisangen" in yaku or "Shousangen" in yaku):
                    yakuhai.append("Yakuhai ({0})".format(name))
                elif name == roundWind and name == seatWind:
                    yaku.append("Dabukaze ({0})".format(name))
                elif name == roundWind or name == seatWind:
                    yaku.append("Kazepai ({0})".format(name))

        if iipeikou >= 2:
            yaku.append("Ryanpeikou")
        elif iipeikou >= 1:
            yaku.append("Iipeikou")

        if sanshoku_doujun:
            yaku.append("Sanshoku Doujun")
        if sanshoku_douko:
            yaku.append("Sanshoku Doukou")

        hon_itsu = len(seen_suits) == 1
        chin_itsu = hon_itsu and not honors
        if chin_itsu:
            yaku.append("Chin'itsu")
        elif hon_itsu:
            yaku.append("Hon'itsu")

        junchan = all([meld.terminals() for meld in solution])
        chanta = all([meld.terminals() or meld.honors() for meld in solution])
        toitoi = not (Sequence in melds or Meld in melds)
        chiitoi = all([type(meld) == Pair for meld in solution]) and closed

        if melds.count(Pair) == 1 and melds.count(Meld) == 12:
            pair = solution.melds[melds.index(Pair)]
            double = pair.tiles[0] is self.winningtile or pair.tiles[1] is self.winningtile
            yaku.append("Kokushi Musou"+double*" (13)")
        elif not seen_suits:
            yaku.append("Tsuuiisou")
        elif junchan and (toitoi or chiitoi):
            yaku.append("Chinroutou")
        elif chanta and (toitoi or chiitoi):
            yaku.append("Honrou")
        elif chiitoi:
            yaku.append("Chii Toitsu")
            self.fu = 25
        elif toitoi:
            yaku.append("Toitoi")
        elif junchan:
            yaku.append("Junchan")
        elif chanta:
            yaku.append("Chanta")

        if not chiitoi:
            fu = 0
            for meld in self.melds:
                x = 0
                if type(meld) == Pair:
                    x = 2*(self.roundwind in meld) + 2*(self.seatwind in meld)
                    # hack for single wait
                    x = 2*(meld.tiles[0] is self.winningtile or meld.tiles[1] is self.winningtile)
                elif type(meld) == Triplet:
                    x = 2
                elif type(meld) == Quad:
                    x = 8
                if type(meld) in [Triplet,Quad]:
                    if meld.terminalsOnly() or meld.honorsOnly:
                        x *= 2
                    if meld.closed():
                        x *= 2
                fu += x
            if not tsumo and self.closed:
                fu += 10
            elif tsumo and not "Pinfu" in yaku:
                fu += 2
            self.fu += fu + 10-fu%10 if fu%10 else fu

    def yaku(self):
        return self.yakuList + (["Dora %s"%self.dora] if self.dora else []) + (["Uradora %s"%self.uradora] if self.uradora else [])

class DummyHand(MahjongHand):
    def __init__(self, fu, yaku, dora = 0, uradora = 0, closed = True):
        MahjongHand.__init__(self,[])
        self.fu = fu
        self.yakuList = yaku
        self.dora = dora
        self.uradora = uradora if "Riichi" in yaku else 0
        self.closed = closed

    def fu(self):
        return self.fu

class MahjongGameState(object):
    def __init__(self, players, tonpuusen = False):
        if len(players) > 4:
            players = players[:4]
        players.extend(["Unnamed%s"%i for i in range(4-len(players))])
        self.players = players
        self.round = 0
        self.tonpuusen = tonpuusen
        self.points = dict([(player,20000 if tonpuusen else 25000) for player in players])
        self.richi = dict([(player,0) for player in players])
        self.yakitori = dict([(player,True) for player in players])
        self.renchan = 0
        self.pool = 0
        self.handHistory = {}

    def isDealer(self, player):
        return player == self.players[self.round%4]

    def roundUp(self, points):
        return points+100-points%100 if points%100 else points

    @staticmethod
    def calculateBasePoints(fu,han):
        basepoints = fu * 2 ** (2+han)
        if basepoints >= 2000:
            print(han)
            basepoints = int(2 + 1*(han >= 6) + 1*(han >= 8) + 2*(han >= 11) + 2*(han >= 13) + 8*(han >= 14))*1000
        return basepoints

    def calculatePayments(self, winningPlayers,losingPlayers, fu, han):
        payment = dict([(player,0) for player in self.players])

        if not winningPlayers:
            payment = [(-1)**(player in losingPlayers) * 3000/(4-len(losingPlayers)) for player in self.players]
        for i,winner in enumerate(winningPlayers):
            self.yakitori[player] = False
            basepoints = self.calculateBasePoints(fu[i],han[i])

            print(basepoints)
            total = 0
            for loser in losingPlayers:
                factor = (1 + self.isDealer(loser) * 1) if len(losingPlayers) > 1 else 4
                factor = int(factor * 1.5**(self.isDealer(winner)) + 0.5)
                points = self.roundUp(factor * basepoints) + self.renchan * (300/len(losingPlayers))
                payment[loser] -= points
                total += points
            payment[winner] += total
        return payment

    def riichi(self, player, doubleOrOpen = False):
        factor = 1 + doubleOrOpen
        if self.riichi[player] + factor > 2:
            factor = -self.riichi[player]
        points = 1000 * factor
        self.pool += points
        self.points[player] -= points
        self.riichi[player] += factor

    def endHand(self, winningPlayers, losingPlayers, hands = [], dora = [], uradora = [], ippatsu = False, kan = False, tileTiming = 0):
        fu = []
        han = []
        for i,player in enumerate(winningPlayers):
            hands[i].checkYaku(self.round%4,self.players.index(player), dora, uradora, ippatsu,kan,tileTiming)
            fu.append(hands[i].fu())
            han.append(hands[i].han())

        payments = self.calculatePayments(winningPlayers,losingPlayers,fu,han)
        print(payments)
        self.pay(payments)

        for player in winningPlayers:
            self.points[player] += self.pool / len(winningPlayers)
            self.pool = 0

        self.riichi = dict([(player,0) for player in self.players])

        self.handHistory.setdefault(self.round,[]).append(hands)
        dealer = self.players[self.round%4]
        self.advance(dealer in winningPlayers or (not winningPlayers and dealer not in losingPlayers))

    def endGame(self, uma = [20,10,-10,-20]):
        uma = list(reversed(uma))
        scores = []
        for i,data in enumerate(sorted(zip(self.points,self.players))):
            points,player = data
            if points < (25000 if self.tonpuusen else 30000):
                points = ((points + 1000-points%1000) / 1000) if points%1000 else points / 1000
            else:
                points = points/1000
            points -= 25 if self.tonpuusen else 30
            if i == 3:
                points += 20

            scores.insert(0,(player,points+uma[i]))
        return scores

    def advance(self, renchan = False):
        if renchan:
            self.renchan += 1
        else:
            self.round += 1
            self.renchan = 0

    def pay(self,amounts):
        for i in range(4):
            self.points[self.players[i]] += amounts[i]

class Tile(object):
    def __init__(self, name, closed=True):
        self.name = name
        self.suit = None
        self.rank = None
        self.closed = closed

    def __repr__(self):
        return ("{0}" if self.closed else "<{0}>").format(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

class HonorTile(Tile):
    def __init__(self, name, closed = True):
        Tile.__init__(self,name,closed)

    def __lt__(self, other):
        return False

    def __le__(self, other):
        return self.__eq__(other)

    def __gt__(self,other):
        return False

    def __ge__(self,other):
        return self.__eq__(other)

class SuitTile(Tile):
    def __init__(self, name, closed = True):
        Tile.__init__(self,name,closed)
        self.suit = name[1:]
        self.rank = int(name[0])

    def __lt__(self, other):
        return (self.suit,self.rank) < (other.suit,other.rank)

    def __le__(self, other):
        return (self.suit,self.rank) <= (other.suit,other.rank)

    def __gt__(self,other):
        return (self.suit,self.rank) > (other.suit,other.rank)

    def __ge__(self,other):
        return (self.suit,self.rank) >= (other.suit,other.rank)

    def __add__(self, other):
        if type(other) == int:
            return SuitTile("%s%s"%((self.rank+other)%9 or 9,self.suit), self.closed)
        else:
            raise TypeError

class Meld(object):
    length = 0
    def __init__(self, parent = None):
        self.parent = parent
        self.tiles = []
        self.failure = False

    def extend(self, tiles):
        """returns True if tile was extracted from stack, False if no fitting tile could be found or meld is full"""
        if not self.tiles:
            self.tiles.append(tiles.pop(0))
            return True
        return False

    def full(self):
        """return True if meld is full"""
        return NotImplemented

    def closed(self):
        return all([t.closed for t in self.tiles])

    def mixed(self):
        return 0 < len([True for t in self.tiles if t.closed]) < self.length

    def full(self):
        return len(self.tiles) >= self.length

    def terminals(self):
        count = 0
        for tile in self:
            if type(tile) == SuitTile and tile.rank in [1,9]:
                count += 1

    def terminalsOnly(self):
        return self.terminals() == self.length

    def honors(self):
        count = 0
        for tile in self:
            if type(tile) == HonorTile:
                count += 1

    def honorsOnly(self):
        return self.honors() == self.length

    def terminalsOrHonorsOnly(self):
        return (self.honors() + self.terminals()) == self.length

    def __iter__(self):
        return self.tiles.__iter__()

    def __contains__(self,obj):
        return self.tiles.__contains__(obj)

    def __repr__(self):
        o = not self.closed()
        return o*"<"+"{0}".format(self.__class__.__name__)+o*">"+ "({0})".format(str(self.tiles))

    def __eq__(self, other):
        if type(other) == type(self) and self.tiles == other.tiles:
            return True
        else:
            return False

    def __ne__(self,other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return (self.__class__.__name__,self.tiles[0]) < (other.__class__.__name__,other.tiles[0])

    def __le__(self, other):
        return (self.__class__.__name__,self.tiles[0]) <= (other.__class__.__name__,other.tiles[0])

    def __gt__(self,other):
        return (self.__class__.__name__,self.tiles[0]) > (other.__class__.__name__,other.tiles[0])

    def __ge__(self,other):
        return (self.__class__.__name__,self.tiles[0]) >= (other.__class__.__name__,other.tiles[0])

class Pair(Meld):
    length = 2
    def extend(self, tiles):
        if not Meld.extend(self, tiles):
            if not self.full() and self.tiles[-1] in tiles:
                self.tiles.append(tiles.pop(tiles.index(self.tiles[-1])))
                return True
            else:
                return False
        else:
            return True

class Triplet(Pair):
    length = 3

class Quad(Pair):
    length = 4

class Sequence(Meld):
    length = 3
    def extend(self, tiles):
        if not Meld.extend(self, tiles):
            if not isinstance(self.tiles[-1],HonorTile) and not self.full() and self.tiles[-1]+1 in tiles:
                self.tiles.append(tiles.pop(tiles.index(self.tiles[-1]+1)))
                return True
            else:
                return False
        else:
            return True

class Solution(object):
    def __init__(self, melds):
        self.melds = sorted(melds)

    def valid(self):
        pairs = len([True for m in self.melds if type(m) == Pair])
        mixed = len([True for m in self.melds if m.mixed()])
        return len(self.melds) == 5 and (pairs < 2 or pairs == 7) and mixed < 2

    def __eq__(self, other):
        return len(self.melds) == len(other.melds) and all([a==b for a,b in zip(self.melds,other.melds)])

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<<{0} {1}>>".format(self.__class__.__name__,str(self.melds))

    def __iter__(self):
        return self.melds.__iter__()

    def __contains__(self, obj):
        return self.melds.__contains__(obj)

def analyze(tiles):
    def fork(node, stack, parent = None):
        """create a new quadruple fork by generating one of each type of meld with the next tile in the stack"""
        for meld in Pair,Triplet,Quad,Sequence:
            node[meld(parent)] = {}
        for meld,subnode in node.items():
            substack = [t for t in stack]
            while meld.extend(substack):
                pass
            if meld.full() and substack:
                fork(subnode,substack, meld)
            elif not meld.full():
                meld.failure = True

    def trace(tree):
        """walks through tree and returns all valid combinations"""
        stack = [tree]
        endpoints = []
        while stack:
            current = stack.pop(0)
            for item,children in current.items():
                if children:
                    stack.append(children)
                else:
                    endpoints.append(item)
        variants = []
        for endpoint in endpoints:
            if endpoint.failure:
                continue
            chain = []
            while endpoint is not None:
                chain.append(endpoint)
                endpoint = endpoint.parent
            solution = Solution(reversed(chain))
            if solution.valid() and not any([v == solution for v in variants]):
                variants.append(solution)

        return variants

    # run hand analysis, return possible variants
    tree = {}
    fork(tree,sorted([t for t in tiles]))
    solutions = trace(tree)
    # kokushi hack
    orphans = [SuitTile(i+suit) for suit in tile_short_map["numerical"].values() for i in ["1","9"]]
    orphans.extend([HonorTile(name) for name in tile_short_map["honors"].values()])
    if all([tiles.count(tile) >= 1 for tile in orphans]) and len([tile for tile in orphans if tiles.count(tile) == 2]) == 1:
        melds = []
        tiles = [tile for tile in tiles]
        while tiles:
            meld = Meld()
            if tiles.count(tiles[0]) == 1:
                meld.extend(tiles)
            else:
                meld = Pair()
                meld.extend(tiles)
                meld.extend(tiles)
            melds.append(meld)
        solutions.append(Solution(melds))
    # kokushi hack end
    return solutions

class Hand(object):
    def __init__(self):
        self.owner = ""
        self.tiles = []
        self.winningtile = None
        self.winningmode = None
        self.riichi = 0
        self.variants = []

        # situationals
        self.oyarenchan = 0
        self.roundwind = None
        self.seatwind = None
        self.ippatsu = False
        self.rinshan = False
        self.chankan = False
        self.haitei = False
        self.houtei = False
        self.dora = []

    def parseHand(self, hand):
        import string

        self.tiles = []
        index = 0
        section = 0

        self.owner,situation,hand = hand.split(":")
        self.roundwind = HonorTile(tile_short_map["honors"][situation[0]])
        self.seatwind = HonorTile(tile_short_map["honors"][situation[1]])
        if len(situation) > 2:
            self.oyarenchan = int(situation[2])

        tile = None
        while index < len(hand):
            numeral = ""
            char = hand[index]

            index += 1

            if section < 0:
                if char == ":":
                    section = 0
                continue

            if char=="/":
                section += 1
                continue
            elif char == " ":
                continue

            if char in string.digits:
                numeral = char
                char = hand[index]
                index += 1
            else:
                char = char.lower()
            if section < 3:
                tile = SuitTile(numeral+tile_short_map["numerical"][char],section>0) if numeral else HonorTile(tile_short_map["honors"][char],section > 0)
            elif not self.winningmode:
                self.riichi = section - 3
                self.winningmode = {"r":"Ron","t":"Tsumo"}[char]
                tile.closed = self.winningmode == "Tsumo"
                tile = None
            else:
                if char == "1":
                    self.ippatsu = True
                if self.winningmode == "Tsumo":
                    if char == "k":
                        self.rinshan = True
                    elif char == "h":
                        self.haitei = True
                elif self.winningmode == "Ron":
                    if char == "k":
                        self.chankan = True
                    elif char == "h":
                        self.houtei = True
            if tile:
                self.tiles.append(tile)
                if section == 2:
                    self.winningtile = tile

        self.variants = analyze(self.tiles)
        solutions = []
        for v in self.variants:
            print(v)
            solutions.append(self.calculateYaku(v))
        if solutions:
            return sorted(solutions)[0]
        else:
            return (0,[])

    def calculateYaku(self, solution):
        fu = 20
        han = 2
        yaku = []
        hand = MahjongHand(solution,self.winningtile)
        basepoints = fu * 2**(2+han)
        dealer = self.seatwind.name == "Ton"
        points_main = 0
        points_other = 0
        if dealer:
            if self.winningmode == "Ron":
                points_other = basepoints * 6
            else:
                points_other = basepoints * 2
        else:
            if self.winningmode == "Ron":
                points_main = basepoints * 4
            else:
                points_main = basepoints * 2
                points_other = basepoints * 1

        # rounding
        points_main,points_other = [p + (100 - p%100)*bool(p%100) for p in (points_main, points_other)]

        # oyarenchan adjustment

        if self.oyarenchan:
            if points_main:
                points_main += (300 if self.winningmode == "Ron" else 100)
            if points_other:
                points_other += 100*self.oyarenchan

        print(yaku)
        print("{0} Fu, {1} Han > {2} / {3}{4}".format(fu,han,points_main,points_other,bool(self.oyarenchan)*(" (Oyarenchan %s)"%self.oyarenchan)))
        return basepoints,yaku

    def __repr__(self):
        return ", ".join([str(tile) for tile in sorted(self.tiles)])

if __name__=="__main__":
    h = Hand()
    tiles = "Dummy:tx:/2s2s2s3m4m5m4m5m6m8p8p5p5p/8p/r/h"
    print(tiles)
    h.parseHand(tiles)