import keyboard, socket, json
from time import sleep
from os import system

currentGameArray = [
    ["   ", "   ", "   "], 
    ["   ", "   ", "   "], 
    ["   ", "   ", "   "], 
]
currentGame = """
_________________________
|       |       |       |
|   1   |   2   |   3   |
|_______|_______|_______|
|       |       |       |
|   4   |   5   |   6   |
|_______|_______|_______|
|       |       |       |
|   7   |   8   |   9   |
|_______|_______|_______|
"""

playerInfo = {
    1: {
        "playerModel": "X",
        "nickname": "gamz"
    },
    2: {
        "playerModel": "O",
        "nickname": "sopa"
    }
}
winner = -1
currentSlot = {
    "x": 0, # vönster höger
    "y": 0, # upp ner
    "recentX": 0,
    "recentY": 0,
    "recentModel": False
}

def isSlotEmpty():
    if not currentSlot["recentModel"]:
        return True
    return False

def updateBoard(playerModel):
    global currentSlot, currentGameArray
    if (currentSlot["y"] >= 0 and currentSlot["y"] <= 2) and (currentSlot["x"] >= 0 and currentSlot["x"] <= 2):
        if currentSlot["recentModel"]:
            finalString = ""
            if len(currentSlot["recentModel"]) == 3:
                finalString = currentSlot["recentModel"]
            else:
                finalString = " " + currentSlot["recentModel"] + " "
            currentGameArray[currentSlot["recentY"]][currentSlot["recentX"]] = finalString
            currentSlot["recentModel"] = False
        else:
            currentGameArray[currentSlot["recentY"]][currentSlot["recentX"]] = "   "

        if currentGameArray[currentSlot["y"]][currentSlot["x"]] != "   ":
            currentSlot["recentModel"] = currentGameArray[currentSlot["y"]][currentSlot["x"]]
        currentGameArray[currentSlot["y"]][currentSlot["x"]] = "[" + playerModel + "]"

        currentSlot["recentY"] = currentSlot["y"]
        currentSlot["recentX"] = currentSlot["x"]

    system("cls")
    displayBoard()
    print("[LEFT-ARROW] To Move Left\n[RIGHT-ARROW] To Move Right\n[UP-ARROW] To Move Up\n[DOWN-ARROW] To Move Down\n")
    # print("currentslotY:", currentSlot["y"], " | currentslotX: ", currentSlot["x"])
    if isSlotEmpty():
        print("DU KAN LÄGGA HÄR")
    else:
        print("DU KAN INTE LÄGGA HÄR")
    sleep(0.3)

def displayBoard():
    global currentGame
    tempString = currentGame
    player1, player2 = playerInfo[1]["nickname"], playerInfo[2]["nickname"]
    x, z = 0, 0
    for i in range(1, 10):
        currentIndex = str(i)
        currentSlot = currentGameArray[z][x]
        x += 1
        if x >= 3:
            z += 1
            x = 0
        tempString = tempString.replace(" " + currentIndex + " ", currentSlot)
    system("cls")
    print(f"CURRENT GAME | {player1} vs {player2}\n",tempString, flush=True)

    # print(currentGameArray[0])
    # print(currentGameArray[1])
    # print(currentGameArray[2])

def hasPlayerWon(playerId):
    playerModel = " " + playerInfo[playerId]["playerModel"] + " "
    for i in range(3):
        if (currentGameArray[i][0] == playerModel) and (currentGameArray[i][1] == playerModel) and (currentGameArray[i][2] == playerModel):
            return True
        if (currentGameArray[0][i] == playerModel) and (currentGameArray[1][i] == playerModel) and (currentGameArray[2][i] == playerModel):
            return True
    if (currentGameArray[0][0] == playerModel) and (currentGameArray[1][1] == playerModel) and (currentGameArray[2][2] == playerModel):
        return True
    if (currentGameArray[0][2] == playerModel) and (currentGameArray[1][1] == playerModel) and (currentGameArray[2][0] == playerModel):
        return True
    return False
    
def makeMove(player):
    global currentSlot, currentGame, currentGameArray
    playerModel = playerInfo[player]["playerModel"]
    updateBoard(playerModel)
    while True:
        if keyboard.is_pressed("right arrow"):
            if currentSlot["x"] < 2:
                currentSlot["x"] += 1
                updateBoard(playerModel)
        elif keyboard.is_pressed("left arrow"):
            if currentSlot["x"] > 0:
                currentSlot["x"] -= 1
                updateBoard(playerModel)
        elif keyboard.is_pressed("down arrow"):
            if currentSlot["y"] < 2:
                currentSlot["y"] += 1
                updateBoard(playerModel)
        elif keyboard.is_pressed("up arrow"):
            if currentSlot["y"] > 0:
                currentSlot["y"] -= 1
                updateBoard(playerModel)
        elif keyboard.is_pressed("enter"):
            if not currentSlot["recentModel"]:
                currentGameArray[currentSlot["y"]][currentSlot["x"]] = " " + playerModel + " "
                currentSlot["recentY"] = currentSlot["y"]
                currentSlot["recentX"] = currentSlot["x"]
                currentSlot["x"] = 0
                currentSlot["y"] = 0
                currentSlot["recentModel"] = " " + playerModel + " "
                displayBoard()
                break
            else:
                print("Det är inte ens ledigt här", currentSlot["recentModel"], flush=True)
            sleep(0.6)
        elif keyboard.is_pressed("-"):
            exit(0)

def a():
    global winner
    while winner == -1:
        for currentPlayer in range(1, 3):
            displayBoard()
            makeMove(currentPlayer)
            if hasPlayerWon(currentPlayer):
                nickname = playerInfo[currentPlayer]["nickname"]
                print("Spelare", currentPlayer, f"({nickname}) vann!", flush=True)
                sleep(5)
                winner = currentPlayer
                quit()
            sleep(0.2)

def playTurn(playerId):
    displayBoard()
    makeMove(playerId)
    if hasPlayerWon(playerId):
        nickname = playerInfo[playerId]["nickname"]
        print("Spelare", playerId, f"({nickname}) vann!", flush=True)
        sleep(5)
        winner = playerId
        quit()
    sleep(0.2)

hostServer = input("HOST Server? ")
yourTurn = False
if hostServer == "y":
    print("[TRE I RAD] Väntar på att någon ska ansluta...")
    playerId = 1
    while True:
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind(("localhost", 8089))
        serversocket.listen(1)
        connections, address = serversocket.accept()
        connection = connections.recv(1024)
        receivedData = json.loads(connection.decode())

        if receivedData:
            print("Received something", receivedData)
            if receivedData["action"] == "join":
                joinedUser = receivedData["username"]
                playerInfo[2]["username"] = joinedUser
                print("[TRE I RAD]", joinedUser, "joined")
                print("[TRE I RAD] Väntar på att", joinedUser, "ska spela")
                encodedGame = json.dumps({
                    "action": "makeMove",
                    "data": currentGameArray,
                    "username": playerInfo[1]["nickname"]
                }).encode()
                connections.send(encodedGame)
                serversocket.close()
            
            if receivedData["action"] == "makeMove":
                currentGameArray = receivedData["data"]
                print("[TRE I RAD] Din tur!")
                encodedGame = json.dumps({
                    "action": "makeMove",
                    "data": currentGameArray,
                    "username": playerInfo[1]["nickname"]
                }).encode()
                connections.send(encodedGame)
                
else:
    firstLaunch = True
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', 8089))
    while True:

        if firstLaunch:
            firstLaunch = False
            print("ANSLUTER")
            encodedGame = json.dumps({
                "action": "join",
                "data": currentGameArray,
                "username": playerInfo[2]["nickname"]
            }).encode()
            print("ANSLUTEN")
            clientsocket.send(encodedGame)
        else:
            connection = clientsocket.recv(1024)
            receivedData = json.loads(connection.decode())
            if receivedData["action"] == "makeMove":
                print("[TRE I RAD] Din tur!")
                playTurn(2)
                encodedGame = json.dumps({
                    "action": "makeMove",
                    "data": currentGameArray,
                    "username": playerInfo[2]["nickname"]
                }).encode()
                sleep(1)
                clientsocket.send(encodedGame)
                print("sent")

        
