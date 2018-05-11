class Action:
    playerSwap = 1
    middleSwap = 2
    playerPeek = 3
    middlePeek = 4
    copyPlayer = 5
    listClass = 6

    def __init__(self, action, args):
        self.action = action
        self.args = [*args]

class WinConditions:
    villager = 1
    werewolf = 2
    tanner = 3

class RoleBase():
    def __init__(self, username, playerIndex):
        self.username = username
        self.playerIndex = playerIndex

    def actions(self, numPlayers):
        yield from []

    def respond(self, resp, i):
        pass

    def setRole(self, role):
        self.role = role
        self.name = role.name

class Robber(RoleBase):
    name = "Robber"
    turnOrder = 5
    win = WinConditions.villager

    def __init__(self, username, playerIndex):
        super().__init__(username, playerIndex)
        self.role = Robber

    def actions(self, numPlayers):
        print("Hello {}, you are player number {}".format(self.username, self.playerIndex))
        choice = input("Which card do you want to steal? ")
        yield Action(Action.playerSwap, [int(choice), self.playerIndex])

        yield Action(Action.playerPeek, [self.playerIndex])

    def respond(self, newRole, i):
        if i == 1:
            print("{}, you are now the {}".format(self.username, newRole.name))
            self.role = newRole

class Insomniac(RoleBase):
    name = "Insomniac"
    turnOrder = 8
    win = WinConditions.villager

    def __init__(self, username, playerIndex):
        super().__init__(username, playerIndex)
        self.role = Insomniac

    def actions(self, numPlayers):
        yield Action(Action.playerPeek, [self.playerIndex])

    def respond(self, newRole, i):
        if newRole.name == "Insomniac":
            print("Your role hasn't changed, you are still the insomniac.")
        else:
            print("You are now the", newRole.name)
        self.role = newRole

class Werewolf(RoleBase):
    name = "Werewolf"
    turnOrder = 1
    win = WinConditions.werewolf

    def __init__(self, username, playerIndex):
        super().__init__(username, playerIndex)
        self.role = Werewolf
        self.alone = False

    def actions(self, numPlayers):
        yield Action(Action.listClass, ["Werewolf"])

        if self.alone:
            choice = int(input("Which card would you like to peek at?"))
            yield Action(Action.middlePeek, [choice])

    def respond(self, resp, i):
        if i == 0:
            print("Hello, {}".format(self.username))

            if len(resp) > 1:
                print("These players are the werewolves:")
                print(", ".join(player.username for player in resp))
                print("")
            else:
                self.alone = True
                print("Unfortunately, you are the lone wolf")
                print("")

        elif i == 1:
            print("The card you viewed was the {}".format(resp.name))

        
class Villager(RoleBase):
    name = "Villager"
    turnOrder = 8
    win = WinConditions.villager

    def __init__(self, username, playerIndex):
        super().__init__(username, playerIndex)
        self.role = Villager
