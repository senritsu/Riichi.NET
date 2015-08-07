

from fw_networking import Client,Server
import pickle
import random

def shuffled(objList):
    source = [obj for obj in objList]
    result = []
    while source:
        choice = random.choice(source)
        source.remove(choice)
        result.append(choice)
    return result

class Tile(object):
    def __init__(self, suit, value, name):
        self.id = None
        self.suit = suit
        self.name = name
        self.value = value
        self.displayName = self.name
        if self.suit != "Honors":
            self.displayName += self.suit
        self.flipped = 1
        self.rotated = 0

        self.area = 0
        self.location = 0
        self.index = 0

    def updateLocation(self, area, location, index):
        a,b,c = self.area,self.location,self.index
        self.area = area
        self.location = location
        self.index = index
        return (self.id,0,a,b,c,area,location,index)

    def updateOrientation(self, flipped = None, rotated = None):
        a,b = self.flipped,self.rotated
        if flipped is not None:
            self.flipped = flipped
        if rotated is not None:
            self.rotated = rotated
        return (self.id,1,a,b,self.flipped,self.rotated)

suitOrder = ["Pin","Sou","Man","Honors"]
numericValues = [str(i+1) for i in range(9)]
honorValues = ["Haku","Hatsu","Chun","Ton","Nan","Xia","Pei"]

class Field(object):
    def __init__(self):
        # wall, hand, open, pond
        self.areas = [[[] for j in range(4)] for i in range(4)]
##        self.walls = [[],[],[],[]]
##        self.hands = [[],[],[],[]]
##        self.ponds = [[],[],[],[]]
##        self.open = [[],[],[],[]]
        self.areas.extend([[[]],[[]]])
        self.liveWall = []
        self.createTiles()

    def createTiles(self):
        tiles = []
        for suit in ["Pin","Sou","Man"]:
            for i in numericValues:
                value = 1
                if i in ["1","9"]:
                    value = 2
                for j in range(4):
                    tiles.append(Tile(suit,value,i))
        for name in honorValues:
            for i in range(4):
                tiles.append(Tile("Honors",2,name))

        for i,tile in enumerate(tiles):
            tile.id = i
        self.tiles = tiles
        print "generated",len(tiles),"tiles"

    def shuffle(self):
        print "shuffled the tiles"
        tiles = shuffled(self.tiles)
        print len(self.tiles)
        for i in range(4):
            for tile in tiles[34*i:34*i+34]:
                self.areas[i][0].append(tile)
                tile.updateLocation(i,0,self.areas[i][0].index(tile))

            print len(self.areas[i][0])
        #self.areas[0][0][0].flipped = False

    def updateLocation(self, area, location):
        for tile in self.areas[area][location]:
            tile.updateLocation(area,location,self.areas[area][location].index(tile))

    def split(self, i):
        left = -2 * i
        right = -2*(i >= 7)*(i - 7) or None
        rest = 2*(7-i)
        print i,left,right,rest
        # create dead wall
        self.areas[4][0] = list(self.areas[(i-1)%4][0][left:right])
        if i < 7:
            # extend dead wall and truncate right wall
            self.areas[4][0].extend(self.areas[(i)%4][0][:rest])
            self.areas[(i)%4][0] = self.areas[(i)%4][0][rest:]
            for tile in self.areas[(i)%4][0]:
                tile.updateLocation((i)%4,0,self.areas[(i)%4][0].index(tile))
        if i > 7:
            # create remains
            self.areas[5][0] = self.areas[(i-1)%4][0][right:]
        self.areas[4][0].reverse()

        for j in [4,5]:
            self.updateLocation(j,0)

##        for j in range(7):
##            a = 2*j
##            b = 2*j + 1
##            self.areas[4][0][a],self.areas[4][0][b] = self.areas[4][0][b],self.areas[4][0][a]

        self.liveWall = []
        if i < 7:
            self.liveWall.extend(self.areas[(i-4)%4][0])
        else:
            self.liveWall.extend(self.areas[5][0])
            self.liveWall.extend(self.areas[(i-4)%4][0])
        self.liveWall.extend(self.areas[(i-3)%4][0])
        self.liveWall.extend(self.areas[(i-2)%4][0])
        # truncate original wall
        self.areas[(i-1)%4][0] = self.areas[(i-1)%4][0][:left]
        self.liveWall.extend(self.areas[(i-1)%4][0])
        return (i)

    def draw(self):
        tile = self.liveWall.pop()
        return tile

    def tileOrder(self, tile):
        suit = suitOrder.index(tile.suit)
        value = 0
        if tile.suit == "Honors":
            value = honorValues.index(tile.name)
        else:
            value = numericValues.index(tile.name)
        return (suit,value)

    def sortHand(self, player):
        self.areas[player][1].sort(key=self.tileOrder)
        for tile in self.areas[player][1]:
            tile.index = self.areas[player][1].index(tile)

class MahjongGameState(object):
    def __init__(self):
        self.players = [None for i in range(4)]
        self.avatars = [None for i in range(4)]
        self.points = [[],[],[],[]]
        self.pool = 0
        self.originalDealer = 0
        self.round = 0
        self.dealer = 0
        self.oyarenchan = 0
        self.split = 0
        self.turnhistory = []
        self.running = False
        self.reset()

    def reset(self):
        self.riichi = [0,0,0,0]
        self.handstate = [0,0,0,0]
        self.kan = [0,0,0,0]
        self.open = [0,0,0,0]
        self.uradora = 0

class History(object):
    def __init__(self, initial = None):
        self.initial = initial
        self.history = []
        self.timeline = []

    def start(self, initial):
        self.initial = initial

    def event(self, origin, event):
        if self.initial:
            self.history[-1].append((origin,event))

    def step(self, time):
        if self.initial:
            self.timeline.append(time)
            self.history.append([])
            print "now player",time

class MahjongServer(Server):

    def initialize(self):

        self.setUserLimit(4)
        self.state = MahjongGameState()
        self.field = Field()
        self.history = History()
        self.requester = None
        self.areasToBroadcast = []

    def deal(self, dealer = 0):
        for i in range(53):
            tile = self.field.draw()
            if i < 48:
                i/=4
            area = (i+dealer)%4
            self.moveTile(tile,area,1, update = False)

        self.modifyTile(self.field.areas[4][0][-5],flip = 1,update = False)
        print "deal complete, live wall",len(self.field.liveWall),"tiles long"

    def nextRound(self, oyarenchan = False):
        if not self.state.running or self.state.round > 1:
            self.state.round = 0
            pool = [p for p in self.state.players]
            for i in range(4):
                player = pool.pop(random.randint(0,len(pool)-1))
                self.changeSeat(player,i)
            self.state.points = [[1,2,4,10] for i in range(4)]
        else:
            self.state.pool += sum(self.state.riichi)
            if oyarenchan:
                if self.state.points[self.state.dealer][3]:
                    self.state.points[self.state.dealer][3] -= 1
                    self.state.oyarenchan += 1
            else:
                self.state.points[self.state.dealer][3] += self.state.oyarenchan
                self.state.oyarenchan = 0
                self.state.dealer += 1
                if self.state.dealer == 4:
                    self.state.round += 1
                    self.state.dealer -= 4

        self.field.__init__()
        self.state.reset()
        self.field.shuffle()
        a,b = [random.randint(1,6) for i in range(2)]
        print "split at",a,"+",b
        self.broadcast("Roll result for wall split: {0}, {1}".format(a,b))
        self.state.split = a+b
        self.field.split(a+b)
        self.deal(self.state.dealer)

        self.state.turnhistory = [self.state.dealer]
        initial = {}
        for tile in self.field.tiles:
            initial[tile.id] = (tile.area,tile.location,tile.index,tile.flipped,tile.rotated)
        self.history = History(initial)
        self.history.step(self.state.dealer)

        print "starting round with players:",str(self.state.players)
        self.broadcast("sending full gamestate")
        print "preparing to broadcast gamestate"
        self.broadcastState()
        for player in self.state.players:
            print "preparing to send tiles to player",player
            self.sendTiles(player)
##        self.state.oyarenchan = 3
##        self.state.pool = 1
##        self.state.points[0][2] -= 1
##        self.state.points[0][3] -= 3
        self.state.running = True

    def sendTiles(self,player):
        print "sending tiles"
        self.sendMessage("",player,"CLEAR")
        for tile in self.field.tiles:
            tile = pickle.dumps(tile)
            self.sendMessage(tile,player,"TILE")

    def broadcastState(self):
        print "current avatars:",self.state.avatars
        state = pickle.dumps(self.state)
        self.broadcast(state,messageType = "STATE")

    def broadcastArea(self, area, location):
        for tile in self.field.areas[area][location]:
            tile.index = self.field.areas[area][location].index(tile)
            self.broadcastTileUpdate(tile)

    def broadcastTileUpdate(self, tile):
        self.broadcastRequest("UPDATE:TILE:{0}:{1}:{2}:{3}:{4}:{5}".format(self.field.tiles.index(tile),tile.area,tile.location,tile.index,tile.flipped,tile.rotated))

    def moveTile(self, tile, area, location, index = -1, update = True):
        if type(tile) == int:
            tile = self.field.tiles[tile]
        a,b,c = area,location,index
        d,e,f = tile.area,tile.location,tile.index
        debug = "moving tile "
        debug += "{0}{1} from {2} {3} to {4} {5}".format(tile.suit,tile.name,d,e,a,b)
        other = None
        if c >= 0:
            other = self.field.areas[a][b][c]
            debug += "\n inverse move for tile {0}{1}".format(other.suit,other.name)
            self.field.areas[a][b][c] = tile
            self.field.areas[d][e][f] = other
            flipped = int(e in [0,1])
            rotated = None
            if e in [0,1]:
                rotated = 0
            self.history.event(self.requester,other.updateLocation(d,e,f))
            self.history.event(self.requester,other.updateOrientation(flipped,rotated))
            if update:
                self.broadcastTileUpdate(other)
        else:
            self.field.areas[d][e].remove(tile)
            self.field.areas[a][b].append(tile)
            if b == 0 and a != 4:
                print "extended live wall"
                self.field.liveWall.append(tile)
            c = self.field.areas[a][b].index(tile)

            if b == 2:
                self.state.open[a] += 1 * (not (d == a and e == b))
            if e == 2:
                self.state.open[d] -= 1 * (not (d == a and e == b))
        # hack
        print debug
        debugTarget = None
        if self.requester is not None:
            debugTarget = self.state.players[self.requester]
        if not debugTarget:
            debugTarget = [user for user in self.state.players if user is not None][0]
        self.sendMessage(debug,debugTarget)
        # hack

        flipped = int(b in [0,1])
        rotated = None
        if b in [0,1]:
            rotated = 0
        self.history.event(self.requester,tile.updateLocation(a,b,c))
        self.history.event(self.requester,tile.updateOrientation(flipped,rotated))
        if update:
            if b == 2 or e == 2:
                self.broadcastState()
            self.broadcastTileUpdate(tile)
            if b == 2:
                self.areasToBroadcast.append((a,b))
            if e == 1:
                self.areasToBroadcast.append((d,e))

    def modifyTile(self, tile, flip = 0, rotate = 0, update = True):
        if type(tile) == int:
            tile = self.field.tiles[tile]
        flipped = None
        rotated = None
        hand = False
        if flip:
            if tile.location == 1:
                self.moveTile(tile,tile.area,2)
            else:
                flipped = int(not tile.flipped)
        if rotate:
            rotated = int(not tile.rotated)
        self.history.event(self.requester,tile.updateOrientation(flipped, rotated))
        if update:
            self.broadcastTileUpdate(tile)
            if rotate:
                self.areasToBroadcast.append((tile.area,tile.location))

    def changeSeat(self, user, seat, switch = False):
        players = self.state.players
        avatars = self.state.avatars
        old = players.index(user)
        if seat != old:
            if players[seat] is None or (switch and players[seat]):
                players[old],players[seat] = players[seat],players[old]
                avatars[old],avatars[seat] = avatars[seat],avatars[old]

                self.broadcastState()
            else:
                self.sendMessage("Seat change declined, seat already occupied",user)

    def userLeft(self, name):
        Server.userLeft(self,name)
        print name,"left, commencing cleanup"
        if name in self.state.players:
            print "removing",name,"from playerlist"
            i = self.state.players.index(name)
            self.state.avatars[i] = None
            self.state.players[i] = None
            self.broadcastState()

    def networkMessage(self, messageType, line, sender, protocol):
        Server.networkMessage(self,messageType, line, sender, protocol)
        if sender in self.users and self.users[sender].ack and messageType == "REQUEST":
            tokens = line.split(":")
            request = tokens.pop(0)
            arguments = map(int,tokens)

            print "request",line,"from",sender
            if request == "ACK":
                self.state.players[random.choice([seat for seat in range(len(self.state.players)) if self.state.players[seat] == None or self.state.players[seat].startswith("Dummy")])] = sender
                print "entered",sender,"into playerlist",self.state.players
                self.broadcastState()
                if self.state.running:
                    self.sendTiles(sender)
                for avatar in self.state.avatars:
                    if avatar:
                        self.sendFile(avatar,sender)
                self.sendMessage("AVATAR",sender,"REQUEST")
            elif request != "AUTH":
                self.processUserRequest(sender,request,arguments)

        if messageType == "FILE":
            filename = line[:line.find(".")+4]
            print "broadcasting file",filename
            self.users[sender].avatar = filename
            self.state.avatars[self.state.players.index(sender)] = filename
            for user in self.users:
                self.sendFile(filename,user)
            self.broadcastState()

    def processUserRequest(self, user, request, arguments):
        self.areasToBroadcast = []
        if request == "FULLSTATE":
            self.sendMessage("CLEAR",sender,"REQUEST")
            self.broadcastState()
            if self.state.running:
                self.sendTiles(sender)

        elif request == "NEXTROUND":
            oyarenchan = arguments[0]
            i = 0
            #hack
            while None in self.state.players:
                self.state.players[self.state.players.index(None)] = "Dummy"+str(i)
                i += 1
            #hack end
            if len([player for player in self.state.players if player is not None]) == 4:
                self.nextRound(oyarenchan)

        if not self.state.running or (request == "SEATCHANGE" and (self.state.players[arguments[0]] is None or self.state.players[arguments[0]].startswith("Dummy"))): #hack
            if request == "SEATCHANGE":
                #self.changeSeat(user,arguments[0])
                self.changeSeat(user,arguments[0],True)

        if self.state.running:
            i,player = self.state.players.index(user),user
##        if sender in self.state.players:
##            i = self.state.players.index(player)
##        else:
##            return

            handFull = len(self.field.areas[i][1]) + len(self.field.areas[i][2]) == 14 + self.state.kan[i]

            self.requester = i
            advance = False

            self.areasToBroadcast = []

            if request == "SWAP":
                # TODO: make permuting tiles possible
                # a,b tile indices
                a,b = arguments
                a = self.field.tiles[a]
                target = self.field.areas[a.area][a.location][-1]
                if b >= 0:
                    target = self.field.tiles[b]
                if a != target and (a.area== target.area and a.location == target.location) and a.location in [1,2]:
                    self.moveTile(a,target.area,target.location,target.index)

            elif request == "TRANSFERPOINTS":
                target = arguments.pop(0)
                for j in range(4):
                    self.state.points[i][j] -= arguments[j]
                    self.state.points[target][j] += arguments[j]

            elif request == "URADORA":
                self.state.uradora = int(not self.state.uradora)
                self.areasToBroadcast.append((4,0))
                print "uradora now",{0:"hidden",1:"revealed"}[self.state.uradora]

            elif request == "SORT":
                self.field.sortHand(i)
                self.areasToBroadcast.append((i,1))

            elif request == "SMART" and self.state.turnhistory[-1] == i:

                # a,b tile indices
                a,b = arguments
                debug = "smart key with "
                if a>0:
                    debug += "{0}{1} in {2} {3}".format(self.field.tiles[a].suit,self.field.tiles[a].name,self.field.tiles[a].area,self.field.tiles[a].location)
                if b>0:
                    debug += "and {0}{1} in {2} {3}".format(self.field.tiles[b].suit,self.field.tiles[b].name,self.field.tiles[b].area,self.field.tiles[b].location)
                if a < 0 and b < 0:
                    debug += "nothing"
                debug += " selected"
                print debug
                self.sendMessage(debug,user)
                if handFull:
                    nextPlayer = (self.state.turnhistory[-1]+1)%4
                    advance = True
                    if a >= 0:
                        a = self.field.tiles[a]
                        if b < 0:
                            if a.location == 1:
                                print "smart a"
                                # discard selected tile
                                self.moveTile(a,i,3)
                                advance = True
                            else:
                                print "smart b"
                                # discard 14th tile to selected tiles location
                                self.moveTile(self.field.areas[i][1][-1],a.area,a.location)
                                if a.area == i and a.location == 3:
                                    advance = True
                        else:
                            print "smart c"
                            # discard selected tile to location of other selected tile
                            b = self.field.tiles[b]
                            self.moveTile(a,b.area,b.location)
                            if a.area == i and a.location == 3:
                                advance = True
                    else:
                        print "smart d"
                        # discard 14th tile
                        self.moveTile(self.field.areas[i][1][-1],i,3)
                        advance = True
                else:
                    if b < 0:
                        if a >= 0 and self.field.tiles[a] not in self.field.liveWall:
                            print "smart e"
                            a = self.field.tiles[a]
                            # draw selected tile or from selected wall, TODO: prevent open areas from being targeted
                            if a.location == 0:
                                a = self.field.areas[a.area][a.location][-1]
                            if a == self.field.areas[a.area][a.location][-1] or a.location == 2:
                                self.moveTile(a,i,1)
                        elif self.field.liveWall:
                            print "smart f"
                            # draw from wall
                            self.moveTile(self.field.draw(),i,1)
                print "live wall",len(self.field.liveWall),"tiles long"

            elif request == "CALL":
                lastPlayer = self.state.turnhistory[-2]
                currentPlayer = self.state.turnhistory[-1]
                if handFull:
                    print "call a"
                    # discard 14th tile to last players pond
                    self.moveTile(self.field.areas[i][1][-1],lastPlayer,3)
                    self.state.turnhistory.append(lastPlayer)
                    self.state.turnhistory.append((lastPlayer+1)%4)
                    self.history.step(lastPlayer)
                    self.history.step((lastPlayer+1)%4)
                else:
                    print "call b"
                    # call from last player
                    self.moveTile(self.field.areas[lastPlayer][3][-1],i,1)
                    if currentPlayer != i:
                        self.state.turnhistory.append(lastPlayer)
                        self.state.turnhistory.append(i)
                        self.history.step(lastPlayer)
                        self.history.step(i)

            elif request == "MODIFY":
                # a tile index, b,c flip/rotate flags
                a,b,c = arguments
                tile = self.field.tiles[a]
                if not (c and tile.location == 0):
                    self.modifyTile(a,b,c)

            elif request == "RETURN":
                # a tile index
                a = arguments[0]
                if handFull:
                    wall = self.field.liveWall[-1].area
                    if len(self.field.areas[wall][0]) == 34 - (wall == (self.state.split)%4 and self.state.split < 7)*2*(7-self.state.split):
                        wall = (wall+1)%4
                    if a >= 0:
                        a = self.field.tiles[a]
                        if a.location == 1:
                            print "return a"
                            # return selected tile from hand to wall
                            self.moveTile(a,wall,0)
                        elif a.location == 2:
                            print "return b"
                            # return selected tile from pond or open to hand
                            if a.area == i and a.location in [1,2]:
                                self.moveTile(a,i,1)
                    else:
                        print "return c"
                        # return 14th tile from hand to wall
                        self.moveTile(self.field.areas[i][1][-1],wall,0)
                else:
                    if a >= 0:
                        print "return d"
                        # return last discard to player after rollback
                        a = self.field.tiles[a]
                        if a.area == i and a.location == 3 and i == self.state.turnhistory[-1]:
                            self.moveTile(a,i,1)

            elif request == "ROLLBACK":
                # step back turn
                lastPlayer = self.state.turnhistory[-2]
                secondToLastPlayer = lastPlayer
                if len(self.state.turnhistory) > 2:
                    secondToLastPlayer = self.state.turnhistory[-3]
                self.history.event(i,-1)
                self.state.turnhistory.append(secondToLastPlayer)
                self.state.turnhistory.append(lastPlayer)
                self.history.step(secondToLastPlayer)
                self.history.step(lastPlayer)

            elif request == "KAN":
                self.state.kan[i] += 1

            elif request == "RIICHI":
                if self.state.riichi[i] < 2 and self.state.points[i][2] > 0:
                    self.state.points[i][2] -= 1
                    self.state.riichi[i] += 1

            elif request == "AGARI":
                self.state.points[i][2] += self.state.pool
                self.state.pool = 0
                self.state.points[i][2] += sum(self.state.riichi)
                self.state.riichi = [0,0,0,0]

            elif request == "CHANGEHAND":
                self.state.handstate[i] -= arguments[0]
                if self.state.handstate[i] > 1:
                    self.state.handstate[i] = 1
                elif self.state.handstate[i] < -1:
                    self.state.handstate[i] = -1

            if advance:
                self.state.turnhistory.append(nextPlayer)
                self.history.step(nextPlayer)

            self.broadcastState()

        for area,location in self.areasToBroadcast:
            self.broadcastArea(area,location)

class MahjongClient(Client):

    def nextRound(self, oyarenchan = 0):
        self.request("NEXTROUND:{0}".format(oyarenchan))

    def uradora(self):
        self.request("URADORA")

    def seatChange(self, seat):
        self.request("SEATCHANGE:{0}".format(seat))

    def transferPoints(self, *args):
        self.request("TRANSFERPOINTS:{0}:{1}:{2}:{3}:{4}".format(*args))

    def smartKey(self, index1 = -1, index2 = -1):
        self.request("SMART:{0}:{1}".format(index1,index2))

    def callTile(self, index = -1):
        self.request("CALL".format(index))

    def modifyTile(self, index, flip = 0, rotate = 0):
        print "MODIFY",index,flip,rotate
        self.request("MODIFY:{0}:{1}:{2}".format(index, flip, rotate))

    def returnTile(self, index = -1):
        self.request("RETURN:{0}".format(index))

    def rollbackTurn(self):
        self.request("ROLLBACK")

    def riichi(self, index):
        self.request("RIICHI:{0}".format(index))

##    def rollback(self, index1 = -1, index2 = -1, index3 = -1, index4 = -1):
##        self.request("ROLLBACK:{0}:{1}:{2}:{3}".format(index1,index2,index3, index4))
##
##    def drawTile(self, index):
##        self.request("DRAWDISCARD:{0}".format(index))
##
##    def callTile(self, index1, index2, index3 = -1, index4 = -1):
##        self.request("CALL:{0}:{1}:{2}:{3}".format(index1,index2,index3, index4))

    def swapTiles(self, a,b = -1):
        self.request("SWAP:{0}:{1}".format(a,b))

    def sortHand(self):
        self.request("SORT")

    def kan(self):
        self.request("KAN")

    def riichi(self):
        self.request("RIICHI")

    def agari(self):
        self.request("AGARI")

    def changeHand(self, i):
        self.request("CHANGEHAND:{0}".format(i))

    def networkMessage(self, messageType, line, sender):
        Client.networkMessage(self, messageType, line, sender)
        if sender == "SERVER":
            if messageType == "REQUEST":
                tokens = line.split(":")
                request = tokens.pop(0)
                arguments = tokens

                if request == "UPDATE":
                    updateType = arguments.pop(0)
                    if updateType == "TILE":
                        tile = self.controller.parent.states[-1].tiles[int(arguments.pop(0))]
                        arguments = map(int,arguments)
                        tile.updateLocation(*arguments[:3])
                        tile.updateOrientation(*arguments[3:])
                        self.controller.parent.states[-1].updateTile(tile)

                elif request == "AVATAR":
                    try:
                        self.sendFile("avatar{0}.png".format(self.controller.uid),"SERVER", source = "avatar.png")
                        print "sent avatar as","avatar{0}.png".format(self.controller.uid)
                    except:
                        raise

            elif messageType == "FILE":
                filename = line[:line.find(".")+4]
                print "saved avatar"
                self.controller.parent.states[-1].loadTexture(filename)

            elif messageType == "CLEAR":
                print "Clearing Tiles."
                self.controller.parent.states[-1].clearTiles()

            elif messageType == "STATE":
                print "beginning to load state..."
                state = pickle.loads(line)
                self.controller.parent.states[-1].updateState(state)
                print "...finished loading state"

            elif messageType == "TILE":
                #print "beginning to load tiles..."
                tile = pickle.loads(line)
                self.controller.parent.states[-1].buildTile(tile)
                self.controller.parent.states[-1].updateTile(tile)
                #print "...finished loading tiles"

if __name__ == "__main__":
    f = Field()
    f.shuffle()
    f.split()
    f.deal()
    print [t.displayName for t in f.hands[0]]
    f.sortHand(0)
    print [t.displayName for t in f.hands[0]]