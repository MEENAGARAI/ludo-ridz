import socket
from tkinter import *
from  threading import Thread
import random
from PIL import ImageTk, Image

screen_width = None
screen_height = None

SERVER = None
PORT = None
IP_ADDRESS = None

canvas1 = None
canvas2 = None

playerName = None
nameEntry = None
nameWindow = None
gameWindow = None

left_boxes = []
right_boxes = []

finish_box = None
player_type = None
turn = None
dice = None
r_button = None
reset_button = None

player1Name = 'joining'
player2Name = 'joining'
player1Label = None
player2Label = None
player1Score = 0
player2Score = 0
player2ScoreLabel = None
player2ScoreLabel = None

winning_msg = None
winning_func_call = 0


def checkColorPosition(boxes, color):
    for box in boxes:
        boxColor = box.cget("bg")
        if(boxColor == color):
            return boxes.index(box)
    return False


def movePlayer1(steps):
    global left_boxes

    boxPosition = checkColorPosition(left_boxes[1:],"red")

    if(boxPosition):
        diceValue = steps
        coloredBoxIndex = boxPosition
        totalSteps = 10
        remainingSteps = totalSteps - coloredBoxIndex

        if(steps == remainingSteps):
            for box in left_boxes[1:]:
                box.configure(bg='white')

            global finish_box

            finish_box.configure(bg='red')

            global SERVER
            global playerName

            greetMessage = f'Red wins the game.'
            SERVER.send(greetMessage.encode())

        elif(steps < remainingSteps):
            for box in left_boxes[1:]:
                box.configure(bg='white')

            nextStep = (coloredBoxIndex + 1 ) + diceValue
            left_boxes[nextStep].configure(bg='red')
        else:
            print("Move False")
    else:
        left_boxes[steps].configure(bg='red')



def movePlayer2(steps):
    global right_boxes

    tempBoxes = right_boxes[-2::-1]

    boxPosition = checkColorPosition(tempBoxes,"yellow")

    if(boxPosition):
        diceValue = steps
        coloredBoxIndex = boxPosition
        totalSteps = 10
        remainingSteps = totalSteps - coloredBoxIndex

        if(diceValue == remainingSteps):
            for box in right_boxes[-2::-1]:
                box.configure(bg='white')

            global finish_box

            finish_box.configure(bg='yellow', fg="black")

            global SERVER
            global playerName

            greetMessage = f'Yellow wins the game.'
            SERVER.send(greetMessage.encode())

        elif(diceValue < remainingSteps):
            for box in right_boxes[-2::-1]:
                box.configure(bg='white')

            nextStep = (coloredBoxIndex + 1 ) + diceValue
            right_boxes[::-1][nextStep].configure(bg='yellow')
        else:
            print("Move False")
    else:
        right_boxes[len(right_boxes) - (steps+1)].configure(bg='yellow')



def rollDice():
    global SERVER
    diceChoices=['\u2680','\u2681','\u2682','\u2683','\u2684','\u2685']

    value = random.choice(diceChoices)

    global player_type
    global r_button
    global turn

    r_button.destroy()
    turn = False

    if(player_type == 'player1'):
        SERVER.send(f'{value}player2Turn'.encode())

    if(player_type == 'player2'):
        SERVER.send(f'{value}player1Turn'.encode())





def leftBoard():
    global gameWindow
    global left_boxes
    global screen_height

    xPos = 85
    for box in range(0,11):
        if(box == 0):
            boxLabel = Label(gameWindow, font=("Helvetica",30), width=1, height=1, relief='ridge', borderwidth=0, bg="red")
            boxLabel.place(x=xPos, y=screen_height/2 - 88)
            left_boxes.append(boxLabel)
            xPos +=50
        else:
            boxLabel = Label(gameWindow, font=("Helvetica",30), width=1, height=1, relief='ridge', borderwidth=0, bg="white")
            boxLabel.place(x=xPos, y=screen_height/2- 100)
            left_boxes.append(boxLabel)
            xPos +=75


def rightBoard():
    global gameWindow
    global right_boxes
    global screen_height

    xPos = 1043
    for box in range(0,11):
        if(box == 10):
            boxLabel = Label(gameWindow, font=("Helvetica",30), width=1, height=1, relief='ridge', borderwidth=0, bg="yellow")
            boxLabel.place(x=xPos, y=screen_height/2-88)
            right_boxes.append(boxLabel)
            xPos +=50
        else:
            boxLabel = Label(gameWindow, font=("Helvetica",30), width=1, height=1, relief='ridge', borderwidth=0, bg="white")
            boxLabel.place(x=xPos, y=screen_height/2 - 100)
            right_boxes.append(boxLabel)
            xPos +=75

def finish_box():
    global gameWindow
    global finish_box
    global screen_width
    global screen_height

    finish_box = Label(gameWindow, text="Home", font=("Chalkboard SE", 32), width=7, height=3, borderwidth=0, bg="green", fg="white")
    finish_box.place(x=screen_width/2 - 100, y=screen_height/2 -160)




def gameWindow():
    global gameWindow
    global canvas2
    global screen_width
    global screen_height
    global dice
    global winning_msg
    global reset_button


    gameWindow = Tk()
    gameWindow.title("Ludo Ladder")
    gameWindow.attributes('-fullscreen',False)

    screen_width = gameWindow.winfo_screenwidth()
    screen_height = gameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas2 = Canvas( gameWindow, width = 1000,height = 1000)
    canvas2.pack(fill = "both", expand = True)

    canvas2.create_image( 0, 0, image = bg, anchor = "nw")

    canvas2.create_text( screen_width/2, screen_height/5, text = "Ludo Ladder", font=("Chalkboard SE",100), fill="white")

    winning_msg = canvas2.create_text(screen_width/2 + 10, screen_height/2 + 250, text = "", font=("Chalkboard SE",100), fill='#fff176')

    reset_button =  Button(gameWindow,text="Reset Game", fg='black', font=("Chalkboard SE", 15), bg="grey",command=restGame, width=20, height=5)

    leftBoard()
    rightBoard()
    finish_box()

    global r_button

    r_button = Button(gameWindow,text="Roll Dice", fg='black', font=("Chalkboard SE", 15), bg="grey",command=rollDice, width=16, height=5)

    global turn
    global player_type
    global playerName
    global player1Name
    global player2Name
    global player1Label
    global player2Label
    global player1Score
    global player2Score
    global player1ScoreLabel
    global player2ScoreLabel



    if(player_type == 'player1' and turn):
        r_button.place(x=screen_width / 2 - 80, y=screen_height/2  + 250)
    else:
        r_button.pack_forget()

    dice = canvas2.create_text(screen_width/2 -10, screen_height/2 + 100, text = "\u2680", font=("Chalkboard SE",250), fill="white")

    player1Label = canvas2.create_text(400,  screen_height/2 + 65, text = player1Name, font=("Chalkboard SE",60), fill='#fff176' )
    player2Label = canvas2.create_text(screen_width - 300, screen_height/2 + 65, text = player2Name, font=("Chalkboard SE",60), fill='#fff176' )

    player1ScoreLabel = canvas2.create_text(400,  screen_height/2 - 160, text = player1Score, font=("Chalkboard SE",80), fill='#fff176' )
    player2ScoreLabel = canvas2.create_text(screen_width - 300, screen_height/2 - 160, text = player2Score, font=("Chalkboard SE",80), fill='#fff176' )


    gameWindow.resizable(True, True)
    gameWindow.mainloop()



def saveName():
    global SERVER
    global playerName
    global nameWindow
    global nameEntry

    playerName = nameEntry.get()
    nameEntry.delete(0, END)
    nameWindow.destroy()

    SERVER.send(playerName.encode())

    gameWindow()


def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1

    nameWindow  = Tk()
    nameWindow.title("Ludo Ladder")
    nameWindow.attributes('-fullscreen',True)


    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas1 = Canvas( nameWindow, width = 500,height = 500)
    canvas1.pack(fill = "both", expand = True)

    canvas1.create_image( 0, 0, image = bg, anchor = "nw")
    canvas1.create_text( screen_width/2, screen_height/5, text = "Enter Name", font=("Chalkboard SE",100), fill="white")

    nameEntry = Entry(nameWindow, width=15, justify='center', font=('Chalkboard SE', 50), bd=5, bg='white')
    nameEntry.place(x = screen_width/2 - 220, y=screen_height/4 + 100)


    button = Button(nameWindow, text="Save", font=("Chalkboard SE", 30),width=15, command=saveName, height=2, bg="#80deea", bd=3)
    button.place(x = screen_width/2 - 130, y=screen_height/2 - 30)

    nameWindow.resizable(True, True)
    nameWindow.mainloop()

def restGame():
    global SERVER
    SERVER.send("reset game".encode())


def handleWin(message):
    global player_type
    global r_button
    global canvas2
    global winning_msg
    global screen_width
    global screen_height
    global reset_button

    if('Red' in message):
        if(player_type == 'player2'):
            r_button.destroy()

    if('Yellow' in message):
        if(player_type == 'player1'):
            r_button.destroy()

    message = message.split(".")[0] + "."
    canvas2.itemconfigure(winning_msg, text = message)

    reset_button.place(x=screen_width / 2 - 80, y=screen_height - 220)

def updateScore(message):
    global canvas2
    global player1Score
    global player2Score
    global player1ScoreLabel
    global player2ScoreLabel


    if('Red' in message):
        player1Score +=1

    if('Yellow' in message):
        player2Score +=1

    canvas2.itemconfigure(player1ScoreLabel, text = player1Score)
    canvas2.itemconfigure(player2ScoreLabel, text = player2Score)



def handleResetGame():
    global canvas2
    global player_type
    global gameWindow
    global r_button
    global dice
    global screen_width
    global screen_height
    global turn
    global right_boxes
    global left_boxes
    global finish_box
    global reset_button
    global winning_msg
    global winning_func_call

    canvas2.itemconfigure(dice, text='\u2680')

    if(player_type == 'player1'):

        r_button = Button(gameWindow,text="Roll Dice", fg='black', font=("Chalkboard SE", 15), bg="grey",command=rollDice, width=16, height=5)
        r_button.place(x=screen_width / 2 - 80, y=screen_height/2  + 250)
        turn = True

    if(player_type == 'player2'):
        turn = False

    for rBox in right_boxes[-2::-1]:
        rBox.configure(bg='white')

    for lBox  in left_boxes[1:]:
        lBox.configure(bg='white')


    finish_box.configure(bg='green')
    canvas2.itemconfigure(winning_msg, text="")
    reset_button.destroy()

    reset_button =  Button(gameWindow,text="Reset Game", fg='black', font=("Chalkboard SE", 15), bg="grey",command=restGame, width=20, height=5)
    winning_func_call = 0


def recivedMsg():
    global SERVER
    global player_type
    global turn
    global r_button
    global screen_width
    global screen_height
    global canvas2
    global dice
    global gameWindow
    global player1Name
    global player2Name
    global player1Label
    global player2Label
    global winning_func_call



    while True:
        message = SERVER.recv(2048).decode()

        if('player_type' in message):
            recvMsg = eval(message)
            player_type = recvMsg['player_type']
            turn = recvMsg['turn']
        elif('player_names' in message):

            players = eval(message)
            players = players["player_names"]
            for p in players:
                if(p["type"] == 'player1'):
                    player1Name = p['name']
                if(p['type'] == 'player2'):
                    player2Name = p['name']

        elif('⚀' in message):

            canvas2.itemconfigure(dice, text='\u2680')
        elif('⚁' in message):

            canvas2.itemconfigure(dice, text='\u2681')
        elif('⚂' in message):

            canvas2.itemconfigure(dice, text='\u2682')
        elif('⚃' in message):

            canvas2.itemconfigure(dice, text='\u2683')
        elif('⚄' in message):

            canvas2.itemconfigure(dice, text='\u2684')
        elif('⚅' in message):

            canvas2.itemconfigure(dice, text='\u2685')

        elif('wins the game.' in message and winning_func_call == 0):
            winning_func_call +=1
            handleWin(message)

            updateScore(message)
        elif(message == 'reset game'):
            handleResetGame()

        if('player1Turn' in message and player_type == 'player1'):
            turn = True
            r_button = Button(gameWindow,text="Roll Dice", fg='black', font=("Chalkboard SE", 15), bg="grey",command=rollDice, width=16, height=5)
            r_button.place(x=screen_width / 2 - 80, y=screen_height/2  + 250)

        elif('player2Turn' in message and player_type == 'player2'):
            turn = True
            r_button = Button(gameWindow,text="Roll Dice", fg='black', font=("Chalkboard SE", 15), bg="grey",command=rollDice, width=16, height=5)
            r_button.place(x=screen_width / 2 - 80, y=screen_height/2  + 260)

        if('player1Turn' in message or 'player2Turn' in message):
            diceChoices=['⚀','⚁','⚂','⚃','⚄','⚅']
            diceValue = diceChoices.index(message[0]) + 1

            if('player2Turn' in message):
                movePlayer1(diceValue)


            if('player1Turn' in message):
                movePlayer2(diceValue)

        if(player1Name != 'joining' and canvas2):
            canvas2.itemconfigure(player1Label, text=player1Name)

        if(player2Name != 'joining' and canvas2):
            canvas2.itemconfigure(player2Label, text=player2Name)





def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    PORT  = 8000
    IP_ADDRESS = '127.0.0.1'

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    thread = Thread(target=recivedMsg)
    thread.start()

    askPlayerName()




setup()
