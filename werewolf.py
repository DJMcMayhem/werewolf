import random
from roles import Action
import roles

class Game():
    def __init__(self, usernames, roles):
        #random.shuffle(roles)
        self.players = []
        self.middleCards = []

        for i in range(3):
            cardClass = roles.pop(0)
            self.middleCards.append(cardClass("", -1))

        for i in range(len(usernames)):
            playerClass = roles[i]
            playerName = usernames[i]

            self.players.append(playerClass(playerName, i))

    def play(self):
        numPlayers = len(self.players)

        for player in sorted(self.players, key=lambda p: p.turnOrder):
            for actionNumber, action, in enumerate(player.actions(numPlayers)):
                resp = self.handleAction(action)
                player.respond(resp, actionNumber)

    def handleAction(self, action):
        if action.action == Action.playerSwap:
            p1, p2 = action.args
            temp = self.players[p1].role
            self.players[p1].setRole(self.players[p2].role)
            self.players[p2].setRole(temp)

        elif action.action == Action.middleSwap:
            p1, p2 = action.args
            temp = self.players[p1].role
            self.players[p1].setRole(self.middleCards[p2].role)
            self.middleCards[p2].setRole(temp)

        elif action.action == Action.playerPeek:
            return self.players[action.args[0]].role

        elif action.action == Action.middlePeek:
            return self.middleCards[action.args[0]].role

        elif action.action == Action.copyPlayer:
            #implement later
            pass

        elif action.action == Action.listClass:
            return list(filter(lambda p: p.role.name == action.args[0], self.players))

            for player in self.players:
                print(player.role.name)


        return ""

    def printAllPlayers(self):
        print("")
        for player in self.players:
            print("{}:\t{}".format(player.username, player.role.name))
        print("")

game = Game(["DJ", "IceDagger"], [roles.Villager, roles.Villager, roles.Robber, roles.Werewolf, roles.Insomniac])

game.play()
