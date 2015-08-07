import os
import random

import ogre.renderer.OGRE as ogre
#import ogre.sound.OgreAL as OgreAL

import framework
Command = framework.logic.Command

from mahjong import MahjongClient,MahjongServer
import os.path

host = "localhost"
username = "CLIENT"
aspectratio = 16.0/9.0

# TO FIX:
# camera issues
# TO IMPLEMENT:
# interactive avatars (animated emotes, like in skype)
# chat
# better current player marker
# refactor lots of stuff
# reset round (next round without increment)
# better models/textures
# better selection marker
# sound
# special effects
# status line with last action

class MainState(framework.states.PlayState):
    def __init__(self, manager):
        framework.states.PlayState.__init__(self, manager)

    def enter(self):
        framework.states.PlayState.enter(self)

        self.cameras["default"].camera.setAspectRatio(aspectratio)
        self.viewports["default"].setBackgroundColour(ogre.ColourValue(0.3,0.3,0.3))
        self.sceneManager.setAmbientLight(ogre.ColourValue(0.3,0.3,0.3))
        self.factory = framework.util.SceneFactory(self.sceneManager)
        self.factory.createDirectionalLight((0.7,0.4,0.2),ogre.Vector3(-1,-2,-0.5))
        self.factory.createDirectionalLight((0.3,0.5,0.7),ogre.Vector3(0.5,-1,1))

        self.debugString = "DEBUG\n{0}"
        self.debug = self.gui.textBox("debug",self.debugString.format(""),0.30,0.0,0.65,0.1)

        self.camControls = framework.camera.RTSCameraControls(self.cameras["default"],self)
        framework.CEGUI.MouseCursor.getSingleton().show()

        self.actorManager = framework.anim.ActorManager(self)
        self.actorManager.time.initSettings([0.0,0.5,1.0,2.0,5.0],2,0.5)

        self.manager.network.client = MahjongClient(self.manager.network)
        self.manager.network.server = MahjongServer(self.manager.network)

##        for j in range(4):
##            for i in range(34):
##                mesh = "tile.mesh"
##                entity,node = self.factory.createEntity("test."+str(j)+"."+str(i),"default", mesh)
##                position = ogre.Vector3(0,0.6+(i+1)%2*1.2,0)
##                tilesize = 1.8*0.75
##
##                if j == 0:
##                    position.z = 12.5
##                    position.x = (i%17-8)*tilesize
##                if j == 1:
##                    position.x = 12.5
##                    position.z = (-i%17-8)*tilesize
##                if j == 2:
##                    position.z = -12.5
##                    position.x = (-i%17-8)*tilesize
##                if j == 3:
##                    position.x = -12.5
##                    position.z = (i%17-8)*tilesize
##                node.setPosition(position)
##                node.yaw(ogre.Degree(90 * j))
##                if i != 0 or j != 0:
##                    node.roll(ogre.Degree(180))
##                entity.setQueryFlags(framework.MASK_SELECTABLE)

        mesh = "mahjong_table.mesh"
        entity,node = self.factory.createEntity("table","default", mesh)
        node.setPosition(0,0,0)
        entity.setQueryFlags(framework.MASK_SYSTEM)
        self.plane = framework.ogre.Plane(framework.ogre.Vector3(0,0,0),framework.ogre.Vector3(1,0,0),ogre.Vector3(0,0,1))

        self.overlayManager.loadFont(os.getcwd() + "/assets/","testfont2")

        self.selectionManager.changeMarkingMethod()

        #self.sounds = OgreAL.SoundManager() # DONT REMOVE, OTHERWISE TWISTED BREAKS

        self.state = None
        self.tiles = []
        self.tileNodes = {}
        self.tilesByName = {}
        self.tilesByEntity = {}
        self.tileMats = []
        self.buildGeometryInformation()
        self.buildFixpoints()
        self.buildMarkers()
        self.buildPlayers()

        self.cameraMode = 1
        self.currentPosition = 0
        self.split = None
        self.cycleCamera()

        self.mainSheet = framework.CEGUI.WindowManager.getSingleton().loadWindowLayout("mahjong.layout")
        self.GUIsystem.setGUISheet(self.mainSheet)
        for i in range(4):
            spinner = self.gui.getWindow("spinner"+str(i))
            spinner.subscribeEvent(spinner.EventValueChanged,self,"pointTransfer")
        transferButton = self.gui.getWindow("transfer")
        transferButton.subscribeEvent(transferButton.EventClicked, self, "pointTransfer")

        self.controls.loadKeyBindings("mahjong_client")
        self.gui.textBox("keyBindings",self.controls.bindingListString,x = 0.725, y = 0.2, size_y = "auto", parent = "UI")
        self.gui.toggle("keyBindings")
        self.gui.toggle("PointTransfer")

        self.manager.log("state entered")

    def buildGeometryInformation(self):
        self.tilesize = (1.8 * 0.75, 2.5 * 0.75, 1.6 * 0.75)
        self.tablesize = 78 * 0.75
        self.tesserasize = (3.72,2.6,0.375)
        self.tenbousize = (8.0 * 0.75, 0.656 * 0.75, 0.375 * 0.75)

    def buildFixpoints(self):
        self.fixpoints = {}
        for i in range(4):
            root = self.sceneManager.getRootSceneNode().createChildSceneNode()
            sign = i/2
            root.yaw(ogre.Degree(i*90))
            pos = ogre.Vector3(i%2 * (1 * (not sign) -1 * (sign)), 0, (i+1)%2 * (1 * (not sign) -1 * (sign)))
            pos *= (self.tablesize * 0.5 - self.tilesize[1] * 0.5)
            root.setPosition(pos)

            campos1 = root.createChildSceneNode()
            campos1.setPosition(ogre.Vector3(0,15,10))
            campos2 = root.createChildSceneNode()
            campos2.setPosition(ogre.Vector3(0,30,-self.tablesize * 0.5 + self.tilesize[1]))
            avatar = root.createChildSceneNode()
            avatar.setPosition(ogre.Vector3(0,15,11))
            wall = root.createChildSceneNode()
            wall.setPosition(ogre.Vector3(-8 * self.tilesize[0], 0, - pos.length() + 8.5 * self.tilesize[0] + self.tilesize[1]*0.5))
            hand = root.createChildSceneNode()
            hand.setPosition(ogre.Vector3(-6* self.tilesize[0], 0, -10))
            openMelds = root.createChildSceneNode()
            openMelds.setPosition(ogre.Vector3(self.tablesize * 0.5 - self.tilesize[0] * 0.5, 0, 0))
            tessera = root.createChildSceneNode()
            tessera.setPosition(ogre.Vector3(-self.tablesize * 0.5 + self.tesserasize[0] * 0.5 + self.tilesize[1]*1.2,self.tesserasize[2] * 0.5, (self.tilesize[1]-self.tesserasize[1]) * 0.5))
            pond = root.createChildSceneNode()
            pond.setPosition(ogre.Vector3(-self.tilesize[0], 0, - pos.length() + 2.5 * self.tilesize[0]))
            riichi = root.createChildSceneNode()
            riichi.setPosition(0, 0.5*self.tenbousize[2], - pos.length() + 7.5 * self.tilesize[0] + self.tilesize[1]*0.5)

            # fixpoint markers
##            for j,fixpoint in enumerate([wall, hand, openMelds, pond]):
##                mesh = "cube.mesh"
##                entity,node = self.factory.createEntity("fixpoint."+str(i)+"."+str(j),"default", mesh)
##                node.setPosition(fixpoint._getDerivedPosition() + ogre.Vector3(0,2.9,0))
##                node.setScale(0.3,0.3,0.3)
##                entity.setQueryFlags(framework.MASK_SYSTEM)

            self.fixpoints[i] = {   "root": root,
                                    "tessera": tessera,
                                    "riichi": riichi,
                                    0: wall,
                                    1: hand,
                                    2: openMelds,
                                    3: pond,
                                    "cameraPositions": [campos1,campos2],
                                    "avatar": avatar}
        self.fixpoints[4] = [None]
        self.fixpoints[5] = [None]
        pool = root.createChildSceneNode()
        pool.setPosition(0.5*self.tenbousize[0],0.5*(-self.tesserasize[2]+self.tenbousize[2]),-0.5*self.tenbousize[0])
        pool.yaw(ogre.Degree(-45))
        self.fixpoints[6] = pool

##        self.deadNodes = []
##        for i in range(2):
##            mesh = "cube.mesh"
##            entity,node = self.factory.createEntity("fixpoint."+str(4)+"."+str(i),"default", mesh)
##            node.setScale(0.3,0.3,0.3)
##            self.deadNodes.append(node)
##            entity.setQueryFlags(framework.MASK_SYSTEM)



    def buildMarkers(self):
        self.markers = {}

        mesh = "cube.mesh"
        entity,node = self.factory.createEntity("cube1","default", mesh)
        entity.setQueryFlags(framework.MASK_SYSTEM)
        node.setPosition(ogre.Vector3(0,-5,0))
        node.setScale(0.5,1.5,0.5)
        self.markers["currentPlayer"] = node

        mesh = "tessera.mesh"
        entity,node = self.factory.createEntity("tessera","default", mesh)
        entity.setQueryFlags(framework.MASK_SYSTEM)
        self.markers["dealer"] = node
        node.setPosition(0,-5,0)

        tenbouAmounts = [4,8,16,40]
        tenbouMats = []
        self.tenbou = []
        for i in range(4):
            tenbou = []
            for j in range(tenbouAmounts[i]):
                mesh = "tenbou.mesh"
                entity,node = self.factory.createEntity(mesh = mesh)
                matName = "tiles/tenbou"+str(i)
                if matName not in tenbouMats:
                    mat = entity.getSubEntity(0).getMaterial().clone(matName)
                    t = mat.getTechnique(0).getPass(0).getTextureUnitState(0)
                    t.setTextureName(matName+".jpg")
                    tenbouMats.append(matName)
                entity.getSubEntity(0).setMaterialName(matName)
                entity.setQueryFlags(framework.MASK_SYSTEM)
                node.setPosition(0,-5,0)
                tenbou.append(node)
            self.tenbou.append(tenbou)

        mesh = "cube.mesh"
        entity,node = self.factory.createEntity("cube2","default", mesh)
        entity.setQueryFlags(framework.MASK_SYSTEM)
        node.setPosition(ogre.Vector3(0,-5,0))
        node.setScale(1.5,0.5,1.5)
        self.currentPlayerMarker = node
        self.markers["originalDealer"] = node


    def buildPlayers(self):
        self.factory.createQuad("avatar",ogre.Vector3(0,0,0),ogre.Vector3(-1,1,0),ogre.Vector3(1,1,0))
        self.avatars = []

        for i in range(4):
            name = "avatar"+str(i)
            marker,node = self.factory.createEntity(name, mesh = "avatar.mesh", parent = self.fixpoints[i]["avatar"])
            node.setScale(10,10,10)

            mat = self.factory.createMaterial(name,textures = ["anonymous.png"])
            mat.getTechnique(0).setSceneBlending(ogre.SBT_TRANSPARENT_ALPHA)
            mat.getTechnique(0).setLightingEnabled(False)
            marker.setMaterial(mat)
            self.avatars.append(mat.getTechnique(0).getPass(0).getTextureUnitState(0))

            label = self.overlayManager.addTextBlock(name,"",ogre.Vector3(0,-1.3,0),"testfont2")
            label.node.getParentSceneNode().removeChild(label.node)
            self.fixpoints[i]["avatar"].addChild(label.node)

    def clearTiles(self):
        for node in self.tileNodes.values():
            entity = node.getAttachedObject(0)
            node.detachObject(entity)
            self.sceneManager.destroyEntity(entity)
            self.sceneManager.destroySceneNode(node)
        self.tiles = []
        self.tileNodes = {}
        self.tilesByName = {}
        self.tilesByEntity = {}

    def clickTile(self, command, points = [ogre.Vector2(0,0),ogre.Vector2(0,0)]):
        entities = self.selectionManager.clickCheck(points)
        if not entities:
            return
        tile = [self.tiles.index(self.tilesByEntity[e.getName()]) for e in entities][0]
        self.clientCommand(command,tile)

    def clientCommand(self, command, *args):
        client = self.manager.network.client
        tiles = [self.tiles.index(self.tilesByEntity[e]) for e in self.selectionManager.selection]

        if command == "NEXTROUND":
            client.nextRound(*args)

        elif command == "URADORA":
            client.uradora()

        elif command == "SEATCHANGE":
            client.seatChange(args[0])

        elif command == "TRANSFERPOINTS":
            client.transferPoints(*args)

        elif command == "SMART" and len(tiles) <= 2:
            client.smartKey(*tiles)

        elif command == "CALL" and len(tiles) <= 1:
            client.callTile(*tiles)

        elif command == "FLIP":
            client.modifyTile(args[0],1,0)

        elif command == "ROTATE":
            client.modifyTile(args[0],0,1)

        elif command == "RETURN" and len(tiles) <= 1:
            client.returnTile(*tiles)

        elif command == "ROLLBACK":
            client.rollbackTurn()

        elif command == "SWAP" and len(tiles) in [1,2]:
            client.swapTiles(*tiles)

        elif command == "SORT":
            client.sortHand()

        elif command == "KAN":
            client.kan()

        elif command == "RIICHI":
            client.riichi()

        elif command == "AGARI":
            client.agari()

        elif command == "CHANGEHAND":
            client.changeHand(args[0])

        self.selectionManager.clearSelection()

    def buildTile(self, tile):
        self.tileNodes[tile] = self.sceneManager.getRootSceneNode().createChildSceneNode()
        if tile.name not in self.tilesByName:
            self.tilesByName[tile.name] = [tile]
        else:
            self.tilesByName[tile.name].append(tile)
        entity,node = self.factory.createEntity("tile."+tile.suit+tile.name+"."+str(self.tilesByName[tile.name].index(tile)), mesh = "tile.mesh", parent = self.tileNodes[tile])
        self.tilesByEntity[entity.getName()] = tile
        #tileface = entity.getSubEntity(1)
        tileface = entity.getSubEntity(0)
        self.tiles.append(tile)
        matName = tile.name
        if tile.suit != "Honors":
            matName = matName + tile.suit
        if matName not in self.tileMats:
            mat = tileface.getMaterial().clone(matName)
            t = mat.getTechnique(0).getPass(0).getTextureUnitState(0)
            t.setTextureName("tiles/"+matName+".jpg")
            self.tileMats.append(matName)
        tileface.setMaterialName(matName)
        #print "built",len(self.tileNodes),"tiles"

    def getScore(self, player):
        if type(player) == "str":
            player = self.state.players.index(player)
        return 10000 * self.state.points[player][0] + 5000 * self.state.points[player][1] + 1000 * self.state.points[player][2] + 100 * self.state.points[player][3]

    def pointTransfer(self, e):
        transfer = e.window.getName() == "transfer"
        total = self.gui.getWindow("total")
        amount = 0
        multipliers = [10000,5000,1000,100]
        sticks = [0,0,0,0]
        for i in range(4):
            spinner = self.gui.getWindow("spinner"+str(i))
            if transfer:
                sticks[i] = int(spinner.getCurrentValue())
                spinner.setCurrentValue(0)
            else:
                amount += multipliers[i] * int(spinner.getCurrentValue())
        total.setText(str(amount))

        if transfer:
            target = None
            selectBox = self.gui.getWindow("playerSelect")
            selection = selectBox.getSelectedItem()
            if selection:
                target = selection.Text
                if target in self.state.players:
                    target = self.state.players.index(target)
                selectBox.setSelection(0,0)
                if target is not None:
                    self.clientCommand("TRANSFERPOINTS",target,*sticks)

    def loadTexture(self, filename):
        print filename
        img = ogre.Image()
        print "trying to load texture",filename
        img.load(filename,"General")
        ogre.TextureManager.getSingleton().loadImage(filename,"General",img)
        #ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups()

    def updateState(self, state):
        print "updating client-side gamestate"
        self.state = state

        player = self.state.players.index(self.manager.network.id)

        if player != self.currentPosition:
            self.currentPosition = player
            self.cycleCamera(True)

        for i in range(4):
            playername = self.state.players[i]
            label = "avatar"+str(i)
            if playername is None:
               playername = "unoccupied"
            self.overlayManager.setText(label,playername.lower(),"testfont2")

            if self.state.avatars[i]:
                avatar = self.state.avatars[i]
                print "trying to display avatar, filename:",avatar
                self.avatars[i].setTextureName(avatar)
            else:
                self.avatars[i].setTextureName("anonymous.png")

            self.fixpoints[i][1].resetOrientation()
            self.fixpoints[i][1].setPosition(ogre.Vector3(-6* self.tilesize[0], 0, -10))
            if self.state.handstate[i]:
                self.fixpoints[i][1].setPosition(self.fixpoints[i][1].getPosition() + ogre.Vector3(0,0.5*self.tilesize[2],0))
                self.fixpoints[i][1].pitch(ogre.Degree(self.state.handstate[i] * 90))

        if self.state.running:
            self.gui.getWindow("scores").setText("    ".join(["{0} : {1}".format(self.state.players[i],self.getScore(i)) for i in range(4)]))
            self.gui.populateBox("playerSelect",self.state.players)
            for i in range(4):
                x_max = self.state.points[player][i]
                available = self.gui.getWindow("available"+str(i))
                available.setText(str(x_max))
                spinner = self.gui.getWindow("spinner"+str(i))
                x = spinner.getCurrentValue()
                spinner.setMaximumValue(x_max)
                spinner.setCurrentValue(min(x,x_max))

            for name,marker in self.markers.items():
                marker.getParent().removeChild(marker)
                if name == "dealer":
                    marker.resetOrientation()
                marker.setPosition(0,0,0)
            self.fixpoints[self.state.dealer]["tessera"].addChild(self.markers["dealer"])
            self.fixpoints[self.state.originalDealer]["root"].addChild(self.markers["originalDealer"])
            if self.state.round:
                self.markers["dealer"].roll(ogre.Degree(180))
            self.fixpoints[self.state.turnhistory[-1]]["root"].addChild(self.markers["currentPlayer"])
            # TODO: somehow dispose of old scenenodes

            pool = self.fixpoints[6]
            pool.getParent().removeChild(pool)
            self.fixpoints[self.state.dealer]["tessera"].addChild(pool)
            counter = [0,0,0,0]
            if self.state.oyarenchan:
                for j in range(self.state.oyarenchan):
                    node = self.tenbou[3][counter[3]]
                    node.resetToInitialState()
                    node.getParent().removeChild(node)
                    pool.addChild(node)

                    node.setPosition(0,0,- j * self.tenbousize[1] * 1.4)

                    counter[3] += 1

            if self.state.pool:

                for j in range(self.state.pool):
                    node = self.tenbou[2][counter[2]]
                    node.resetToInitialState()
                    node.getParent().removeChild(node)
                    pool.addChild(node)

                    node.setPosition(0,0,- (self.state.oyarenchan + j + 1) * self.tenbousize[1] * 1.4)

                    counter[2] += 1

            for i in range(4):
                if self.state.riichi[i]:
                    for j in range(self.state.riichi[i]):
                        node = self.tenbou[2][counter[2]]
                        node.resetToInitialState()
                        node.getParent().removeChild(node)
                        self.fixpoints[i]["riichi"].addChild(node)

                        node.setPosition(0,0,- j * self.tenbousize[1] * 1.4)

                        counter[2] += 1

                for j in range(4):
                    for k in range(self.state.points[i][j]):
                        node = self.tenbou[j][counter[j]]
                        node.resetToInitialState()
                        small_distance = k%8 * self.tenbousize[1] * 1.4
                        offset = self.tenbousize[0]* 0.4
                        table_offset = -1.2*self.tilesize[1]
                        node.setPosition((-1.5+j)*1.2 * self.tenbousize[0],self.tenbousize[2]*0.5 + k/8 * self.tenbousize[2],table_offset - small_distance)
                        if (k/8)%2:
                            node.yaw(ogre.Degree(-90))
                            pos = node.getPosition()
                            node.setPosition(pos.x + offset - small_distance ,pos.y,table_offset - offset )
                        node.getParent().removeChild(node)
                        self.fixpoints[i]["root"].addChild(node)
                        counter[j] += 1

        if state.split != self.split:
            self.split = state.split
            # update fixpoints for dead wall and remains
            i = (state.split-1)%4

            for j in range(4):
                self.fixpoints[j][0].setPosition(ogre.Vector3((-8 + (j == (i+1)%4 and state.split < 7) * (7-state.split)) *self.tilesize[0], 0, -(self.tablesize * 0.5 - self.tilesize[1] * 0.5) + 8.5 * self.tilesize[0] + self.tilesize[1]*0.5))
            node = self.fixpoints[4][0]
            if node:
                node.getParent().removeChild(node)
                self.fixpoints[i]["root"].addChild(node)
            else:
                node = self.fixpoints[i]["root"].createChildSceneNode()
                self.fixpoints[4][0] = node
            pos = self.fixpoints[i][0].getPosition() + ogre.Vector3(16.3*self.tilesize[0],0,0)

            if state.split < 7:
                #node.yaw(ogre.Degree(-90))
                pos += ogre.Vector3( 0, 0, 0.3*self.tilesize[0])
            else:
                if state.split == 7:
                    pos += ogre.Vector3(0,0,0.3)
                pos += ogre.Vector3(-(self.state.split-7) * self.tilesize[0], 0, 0)
            node.setPosition(pos)

##            self.deadNodes[0].setPosition(node._getDerivedPosition() + ogre.Vector3(0,3,0))

            if state.split > 7:
                node = self.fixpoints[5][0]
                if node:
                    node.getParent().removeChild(node)
                    self.fixpoints[i]["root"].addChild(node)
                else:
                    node = self.fixpoints[i]["root"].createChildSceneNode()
                    self.fixpoints[5][0] = node
                pos = self.fixpoints[4][0].getPosition()
                pos += ogre.Vector3(1.3 * self.tilesize[0],0,0)
                node.setPosition(pos)

##                self.deadNodes[1].setPosition(node._getDerivedPosition() + ogre.Vector3(0,3.1,0))

    def updateTile(self, tile):
        w,h,d = self.tilesize
        i,j,k = tile.area,tile.location,tile.index

        node = self.tileNodes[tile]
        node.getParent().removeChild(node)
        node.resetToInitialState()
        self.fixpoints[i][j].addChild(node)

        r_shift = (h-w) * 0.5
        if j == 0:
            if i == 4:
                pos = ogre.Vector3(0,0,0)
                if k/2 < 5 and self.state.uradora and k%2:
                    pos += ogre.Vector3(0,-d, self.tilesize[1])
                if self.state.split < 7 and j == 0 and k/2 < 7 - self.state.split:
                    pos.x,pos.z = pos.z,pos.x
                    pos += ogre.Vector3(0.7*w + r_shift, 0.5 * d + k%2 * d, -r_shift + (-7+ self.state.split + k/2)*w)
                    node.yaw(ogre.Degree(90))
                else:
                    if j == 0 and self.state.split < 7:
                        k -= 2*(7-self.state.split)
                    pos += ogre.Vector3(-(k/2) * w, 0.5* d + k%2 * d,0)
                node.setPosition(pos)
            else:
                node.setPosition(ogre.Vector3(k/2 * w, 0.5* d + k%2 * d,0))
        elif j == 1:
            # TODO: rework so that fixpoint is upright and therefore position setting is more general
            last = 13 + self.state.kan[i] - self.state.open[i]
            node.setPosition(ogre.Vector3(k*w + (k==last) * 0.5 * w + 0.5*self.tilesize[0]*self.state.open[i], 0.5 * h, 0))
            node.pitch(ogre.Degree(-90))
            node.yaw(ogre.Degree(180))
        elif j == 2:
            preceding = [t for t in self.tileNodes if t.area == i and t.location == j and t.index < k and t.rotated]
            node.setPosition(ogre.Vector3(-k*w - 2 * r_shift * len(preceding) - tile.rotated * r_shift, 0.5*d, tile.rotated * r_shift))
        elif j == 3:
            row = k/6
            preceding = [t for t in self.tileNodes if t.area == i and t.location == j and t.index >= 6*row and t.index < 6*row + k%6 and t.rotated]
            node.setPosition(ogre.Vector3((k%6)*w + 2 * r_shift * len(preceding), 0.5*d, h * row + tile.rotated * r_shift))

        if tile.flipped:
            node.roll(ogre.Degree(180))
        if tile.rotated:
            node.yaw(ogre.Degree(90))

    def tile(self):
        mesh = "tile.mesh"
        entity = self.sceneManager.createEntity(mesh)
        node = self.sceneManager.getRootSceneNode().createChildSceneNode()
        node.attachObject(entity)
        entity.setQueryFlags(framework.MASK_SELECTABLE)

    def toggleMenu(self):
        pass

    def cycleCamera(self, position = False):
        if not position:
            self.cameraMode = not self.cameraMode
            self.toggleMode("Freelook")
        self.camControls.camera.setPosition(self.fixpoints[self.currentPosition]["cameraPositions"][self.cameraMode]._getDerivedPosition())
        self.camControls.camera.lookAt(ogre.Vector3(0,0,0))

    def host(self):
        self.manager.network.connect("CLIENT", server = True)

    def connect(self):
        self.manager.network.connect(username, host)

    def sendMessage(self):
        print "trying to send message"
        self.manager.network.client.sendMessage("test")

    def getUserList(self):
        self.manager.network.client.getConnectedUsers()

    def changeSpeed(self, change):
        self.actorManager.time.change(change)

    def frameRenderingQueued(self, eventData):
        statistics = self.manager.renderWindow
        self.debug.setText(self.debugString.format("Triangles: {0}\nBatches: {1}".format(statistics.getTriangleCount(),statistics.batchCount)))
        return True

if __name__ == "__main__":
    import sys
    if "-h" in sys.argv:
        host = sys.argv[sys.argv.index("-h")+1]
    if "-n" in sys.argv:
        username = sys.argv[sys.argv.index("-n")+1]
    if "-a" in sys.argv:
        x,y = map(float,sys.argv[sys.argv.index("-a")+1].split(":"))
        aspectratio = x/y
    from framework import GameStateManager
    manager = framework.GameStateManager("Mahjong Client",{"Main":MainState})
    manager.start("Main")
