'''
Tapu Ahmed
Carlyn Thomsen
Andrew Schlein

4/22/2021
CSCE 4210 / 5210 Artificial Intelligence - Final Project

Please run this code using Python3.

For this project, we created a MiniMax implementation to play dots-and-squares.
The input for the game is manual.  The dots are labeled from 1 - 25.
You will need to input two numbers each time.  Conditions are built in to prevent
incorrect input.

When the AI makes a decision, the AB Minimax tree is printed.  The maximum depth
of search is set to 5.

The graphics will also show score and winner.  Finally, the results of the match
is stored in a file called dataFile.txt.  This file will be in the same directory
as the Python file.  It is designed to keep adding data to it.

'''

import turtle
import time
import random
import sys
import copy

# coordinates to hold location of circles  (Dictionary structure)
coordinates = {1: [-300, 300], 2: [-200, 300], 3: [-100, 300], 4: [0, 300], 5: [100, 300],
               6: [-300, 200], 7: [-200, 200], 8: [-100, 200], 9: [0, 200], 10: [100, 200],
               11: [-300, 100], 12: [-200, 100], 13: [-100, 100], 14: [0, 100], 15: [100, 100],
               16: [-300, 0], 17: [-200, 0], 18: [-100, 0], 19: [0, 0], 20: [100, 0],
               21: [-300, -100], 22: [-200, -100], 23: [-100, -100], 24: [0, -100], 25: [100, -100]}

# Lines that are available for drawing
lines = [(1, 2), (2, 3), (3, 4), (4, 5),
         (6, 7), (7, 8), (8, 9), (9, 10),
         (11, 12), (12, 13), (13, 14), (14, 15),
         (16, 17), (17, 18), (18, 19), (19, 20),
         (21, 22), (22, 23), (23, 24), (24, 25),
         (1, 6), (2, 7), (3, 8), (4, 9), (5, 10),
         (6, 11), (7, 12), (8, 13), (9, 14), (10, 15),
         (11, 16), (12, 17), (13, 18), (14, 19), (15, 20),
         (16, 21), (17, 22), (18, 23), (19, 24), (20, 25)]

# boxes available for drawing and the coordinates of where they begin
# As lines are chose, coordinates are removed from their respective boxes.
# When a box no longer has coordinates available, that means that box has been captured.
boxes = {
    'box1': [[(1, 2), (1, 6), (6, 7), (2, 7)], (-300, 300)],
    'box2': [[(2, 3), (2, 7), (3, 8), (7, 8)], (-200, 300)],
    'box3': [[(3, 4), (3, 8), (8, 9), (4, 9)], (-100, 300)],
    'box4': [[(4, 9), (4, 5), (9, 10), (5, 10)], (0, 300)],
    'box5': [[(6, 7), (6, 11), (11, 12), (7, 12)], (-300, 200)],
    'box6': [[(7, 12), (7, 8), (12, 13), (8, 13)], (-200, 200)],
    'box7': [[(8, 13), (8, 9), (13, 14), (9, 14)], (-100, 200)],
    'box8': [[(9, 14), (9, 10), (14, 15), (10, 15)], (0, 200)],
    'box9': [[(11, 12), (11, 16), (16, 17), (12, 17)], (-300, 100)],
    'box10': [[(12, 17), (12, 13), (17, 18), (13, 18)], (-200, 100)],
    'box11': [[(13, 18), (13, 14), (14, 19), (18, 19)], (-100, 100)],
    'box12': [[(14, 19), (14, 15), (19, 20), (15, 20)], (0, 100)],
    'box13': [[(16, 17), (16, 21), (21, 22), (17, 22)], (-300, 0)],
    'box14': [[(17, 22), (17, 18), (22, 23), (18, 23)], (-200, 0)],
    'box15': [[(18, 23), (18, 19), (23, 24), (19, 24)], (-100, 0)],
    'box16': [[(19, 24), (19, 20), (24, 25), (20, 25)], (0, 0)]
}

########################################################################################################################
########################################################################################################################
########################################################################################################################
###                                         DONT TOUCH THE CODE BELOW                                                ###
########################################################################################################################
########################################################################################################################
########################################################################################################################

# Board initialization code
x = -300
y = 300
tim = turtle.Turtle()
tim.color('black')
tim.pensize(5)
tim.shape('circle')
tim.speed(0)
counter = 1
# Board initialization code

playerScore = 0
aiScore = 0
squaresLeft = 16


# draw the board with the initial circles and labels
tim.penup()
for j in range(5):
    for i in range(5):
        tim.goto(x, y)
        tim.pendown()
        tim.begin_fill()
        tim.circle(10)
        tim.end_fill()
        tim.penup()
        tim.goto(x - 30, y + 30)
        tim.write(counter)
        counter += 1
        tim.goto(x - 30, y - 30)
        x += 100
    y -= 100
    x = -300
    tim.penup()
    tim.goto(1000, 1000)
tim.goto(-600, 400)
tim.pendown()
tim.color('Navy')
tim.write("Welcome to Dots and Boxes ", font=("Verdana", 50, "bold"))
tim.penup()
tim.goto(-600, -200)
tim.color('lightblue')
tim.setheading(0)
tim.pendown()
tim.begin_fill()
tim.forward(1050)
tim.right(90)
tim.forward(300)
tim.right(90)
tim.forward(1050)
tim.right(90)
tim.forward(300)
tim.setheading(0)
tim.end_fill()

tim.penup()
tim.goto(-500, -300)
tim.pendown()
tim.color('red')
tim.write("Player ", font=("Courier", 40, "bold"))
tim.penup()

tim.penup()
tim.goto(-200, -300)
tim.pendown()
tim.color('BLACK')
tim.write("SCORE ", font=("Courier", 60, "bold"))
tim.penup()

tim.penup()
tim.goto(200, -300)
tim.pendown()
tim.color('BLUE')
tim.write("AI ", font=("Courier", 40, "bold"))
tim.penup()

# Player Score
tim.penup()
tim.goto(-440, -450)
tim.pendown()
tim.color('RED')
tim.write("0", font=("Courier", 80, "bold"))
tim.penup()

# AI Score Score
tim.penup()
tim.goto(200, -450)
tim.pendown()
tim.color('BLUE')
tim.write("0", font=("Courier", 80, "bold"))
tim.penup()

tim.goto(1000, 1000)  # makes the turtle disappear off-screen

########################################################################################################################
########################################################################################################################
########################################################################################################################
###                                         DONT TOUCH THE CODE ABOVE                                                ###
########################################################################################################################
########################################################################################################################
########################################################################################################################

# Displays the current score to the console
def displayScore():
    print('\nPlayer Score: ', playerScore)
    print('AI Score: ', aiScore)
    print('\n')

# The start of CPU's decision.  It goes through the boxes remaining and determines
# which one is the bet opening move.  Any box with only 1 line remaining is weighted
# as the best since it allows the AI to gain points.  Then, it's boxes with 4, 3, and
# 2 respectively.  2 is the worst since that grants the other person points.
def determineBestOpener():
    returnType = 2
    for key in boxes:
        myList = boxes[key]
        if len(myList[0]) == 1:
            return 1
    for key in boxes:
        myList = boxes[key]
        if len(myList[0]) == 3:
            returnType = 3
    for key in boxes:
        myList = boxes[key]
        if len(myList[0]) == 4:
            returnType = 4
    return returnType

def determineBestOpenerSim(boxes2):
    returnType = 2
    for key in boxes2:
        myList = boxes2[key]
        if len(myList[0]) == 1:
            return 1
    for key in boxes2:
        myList = boxes2[key]
        if len(myList[0]) == 3:
            returnType = 3
    for key in boxes2:
        myList = boxes2[key]
        if len(myList[0]) == 4:
            returnType = 4
    return returnType

# Once a box has been chosen, which line is the best fit for the box?
# This portion weights the lines that aren't in common as better choices.
def bestChoice(theChoice):
    if len(theChoice) == 4:
        counter1 = 0
        counter2 = 0
        counter3 = 0
        counter4 = 0
        for key in boxes:
            myList = boxes[key]
            if myList[0].__contains__(theChoice[0]):
                counter1 += 1
            elif myList[0].__contains__(theChoice[1]):
                counter2 += 1
            elif myList[0].__contains__(theChoice[2]):
                counter3 += 1
            elif myList[0].__contains__(theChoice[3]):
                counter4 += 1
        theBest = min(counter1, counter2, counter3, counter4)
        if theBest == counter1:
            return theChoice[0]
        elif theBest == counter2:
            return theChoice[1]
        elif theBest == counter3:
            return theChoice[2]
        else:
            return theChoice[3]
    elif len(theChoice) == 3:
        counter1 = 0
        counter2 = 0
        counter3 = 0
        for key in boxes:
            myList = boxes[key]
            if myList[0].__contains__(theChoice[0]):
                counter1 += 1
            elif myList[0].__contains__(theChoice[1]):
                counter2 += 1
            elif myList[0].__contains__(theChoice[2]):
                counter3 += 1
        theBest = min(counter1, counter2, counter3)
        if theBest == counter1:
            return theChoice[0]
        elif theBest == counter2:
            return theChoice[1]
        else:
            return theChoice[2]
    else:
        counter1 = 0
        counter2 = 0
        for key in boxes:
            myList = boxes[key]
            if myList[0].__contains__(theChoice[0]):
                counter1 += 1
            elif myList[0].__contains__(theChoice[1]):
                counter2 += 1
        theBest = min(counter1, counter2)
        if theBest == counter1:
            return theChoice[0]
        else:
            return theChoice[1]

def bestChoiceSim(theChoice, boxes2):
    if len(theChoice) == 4:
        counter1 = 0
        counter2 = 0
        counter3 = 0
        counter4 = 0
        for key in boxes2:
            myList = boxes2[key]
            if myList[0].__contains__(theChoice[0]):
                counter1 += 1
            elif myList[0].__contains__(theChoice[1]):
                counter2 += 1
            elif myList[0].__contains__(theChoice[2]):
                counter3 += 1
            elif myList[0].__contains__(theChoice[3]):
                counter4 += 1
        theBest = min(counter1, counter2, counter3, counter4)
        if theBest == counter1:
            return theChoice[0]
        elif theBest == counter2:
            return theChoice[1]
        elif theBest == counter3:
            return theChoice[2]
        else:
            return theChoice[3]
    elif len(theChoice) == 3:
        counter1 = 0
        counter2 = 0
        counter3 = 0
        for key in boxes2:
            myList = boxes2[key]
            if myList[0].__contains__(theChoice[0]):
                counter1 += 1
            elif myList[0].__contains__(theChoice[1]):
                counter2 += 1
            elif myList[0].__contains__(theChoice[2]):
                counter3 += 1
        theBest = min(counter1, counter2, counter3)
        if theBest == counter1:
            return theChoice[0]
        elif theBest == counter2:
            return theChoice[1]
        else:
            return theChoice[2]
    else:
        counter1 = 0
        counter2 = 0
        for key in boxes2:
            myList = boxes2[key]
            if myList[0].__contains__(theChoice[0]):
                counter1 += 1
            elif myList[0].__contains__(theChoice[1]):
                counter2 += 1
        theBest = min(counter1, counter2)
        if theBest == counter1:
            return theChoice[0]
        else:
            return theChoice[1]



# Determines the best line for a particular move
def chooseBestLine(bestRating):
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    if bestRating == 1:
        for key in boxes:
            myList = boxes[key]
            if len(myList[0]) == 1:
                list1.append(key)
    elif bestRating == 2:
        for key in boxes:
            myList = boxes[key]
            if len(myList[0]) == 2:
                list2.append(key)
    elif bestRating == 3:
        for key in boxes:
            myList = boxes[key]
            if len(myList[0]) == 3:
                list3.append(key)
    else:
        for key in boxes:
            myList = boxes[key]
            if len(myList[0]) == 4:
                list4.append(key)

    if len(list1) > 0:
        bestPick = random.choice(list1)
        myList = boxes[bestPick]
        return random.choice(myList[0])
    elif len(list4) > 0:
        bestPick = random.choice(list4)
        myList = boxes[bestPick]
        theChoice = bestChoice(myList[0])
        return theChoice
    elif len(list3) > 0:
        bestPick = random.choice(list3)
        myList = boxes[bestPick]
        theChoice = bestChoice(myList[0])
        return theChoice
    else:
        bestPick = random.choice(list2)
        myList = boxes[bestPick]
        theChoice = bestChoice(myList[0])
        return theChoice

# Determines the best line for a particular move
def chooseBestLineSim(bestRating, boxes2):
    list1 = []
    list2 = []
    list3 = []
    list4 = []

    if bestRating == 1:
        for key in boxes2:
            myList = boxes2[key]
            if len(myList[0]) == 1:
                list1.append(key)
    elif bestRating == 2:
        for key in boxes2:
            myList = boxes2[key]
            if len(myList[0]) == 2:
                list2.append(key)
    elif bestRating == 3:
        for key in boxes2:
            myList = boxes2[key]
            if len(myList[0]) == 3:
                list3.append(key)
    else:
        for key in boxes2:
            myList = boxes2[key]
            if len(myList[0]) == 4:
                list4.append(key)
    if len(list1) > 0 or len(list2) > 0 or len(list3) > 0 or len(list4) > 0:
        if len(list1) > 0:
            bestPick = random.choice(list1)
            myList = boxes2[bestPick]
            return random.choice(myList[0])
        elif len(list4) > 0:
            bestPick = random.choice(list4)
            myList = boxes2[bestPick]
            theChoice = bestChoiceSim(myList[0], boxes2)
            return theChoice
        elif len(list3) > 0:
            bestPick = random.choice(list3)
            myList = boxes2[bestPick]
            theChoice = bestChoiceSim(myList[0], boxes2)
            return theChoice
        else:
            bestPick = random.choice(list2)
            myList = boxes2[bestPick]
            theChoice = bestChoiceSim(myList[0], boxes2)
            return theChoice
    else:
        return random.choice(lines)

def minMax(rating, lineValue, turn, testLines, testBoxes, counter, bestValue, valuesoFar):
    if counter > 5 or len(testLines) == 0:  # we reach maximum depth
        print()
        return 0
    else:
        value = 0

        # Determine the point value awarded
        if rating == 2 and turn == 0:
            value = -10
        elif rating == 2 and turn == 1:
            value = 10
        elif rating == 1 and turn == 0:
            value = 15
        elif rating == 1 and turn == 1:
            value = -15
        elif rating == 3 and turn == 0:
            value = 2
        elif rating == 3 and turn == 1:
            value = -2
        print(value, '==>', end = '')

        # Determine who gets to keep playing:  AI or player
        if rating == 1 and turn == 1:
            turn = 1
        elif rating == 1 and turn == 0:
            turn = 0
        else:
            if turn == 1:
                turn = 0
            else:
                turn = 1

        # update the line chosen and the simulation boxes
        testLines.remove(lineValue)
        for key in testBoxes:
            myList = testBoxes[key]
            if myList[0].__contains__(lineValue):
                myList[0].remove(lineValue)

        rating = determineBestOpenerSim(testBoxes)
        theLine = chooseBestLineSim(rating, testBoxes)

        # AB Pruning
        valuesoFar += value
        if counter == 1:
            return value + minMax(rating, theLine, turn, testLines, testBoxes, counter + 1, bestValue, valuesoFar)
        else:
            if valuesoFar < bestValue:
                print('PRUNED')
                return value
            else:
                return value + minMax(rating, theLine, turn, testLines, testBoxes, counter + 1, bestValue, valuesoFar)

def aiMove():  # MiniMax Algorithm:
    bestRating = determineBestOpener()
    boxes2 = copy.deepcopy(boxes)
    listOfBest = []
    for key in boxes2:
        myList = boxes2[key]
        if len(myList[0]) == bestRating:
            for term in myList[0]:
                listOfBest.append(term)
    setofBest = list(set(listOfBest))

    bestValue = 0
    bestTerm = setofBest[0]
    print('MiniMax Search:')
    for term in setofBest:
        lines2 = copy.deepcopy(lines)
        boxes2 = copy.deepcopy(boxes)
        temp = minMax(bestRating, term, 0, lines2, boxes2, 1, bestValue, 0)
        if temp > bestValue:
            bestValue = temp
            bestTerm = term
    print('\nBest Score Found for Current State: ', bestValue, '\n\n')
    dataTemp = str(bestTerm)
    if len(dataTemp) <= 7:
        data = f'AI\t\t{bestTerm}\t\t{bestValue}\n'
    else:
        data = f'AI\t\t{bestTerm}\t{bestValue}\n'
    with open('dataFile.txt', 'a') as myFile:
        myFile.write(data)

    return bestTerm

# code for CPU play
def cpuPlays():
    time.sleep(1)

    ####################################################################################################################
    ###                                      THIS IS THE CODE YOU MUST ADJUST                                        ###
    ####################################################################################################################

    # Replace with better choosing algorithm
    cpuChoice = aiMove()

    ####################################################################################################################
    ###                                         DON'T TOUCH THE CODE BELOW                                           ###
    ####################################################################################################################

    print('\nAI chooses line : ', cpuChoice)

    circle1 = cpuChoice[0]
    circle2 = cpuChoice[1]
    temp = (min(circle1, circle2), max(circle1, circle2))

    x1 = coordinates.get(circle1)
    tim.goto(x1[0], x1[1] + 10)
    tim.color('black')
    tim.pendown()
    x2 = coordinates.get(circle2)
    tim.goto(x2[0], x2[1] + 10)
    tim.penup()
    tim.goto(1000, 1000)
    lines.remove(temp)
    createBox = isItABox((temp))
    createBox2 = isItABox(temp)
    if createBox != -1:
        global aiScore
        global playerScore
        aiScore += 1
        global squaresLeft
        squaresLeft -= 1
        drawBox(1, createBox[0], createBox[1])
        updateScore(1)
        if squaresLeft == 0:
            if aiScore > playerScore:
                print("AI wins ")
                whoWins(1)
            elif playerScore > aiScore:
                print("Player Wins")
                whoWins(0)
            else:
                print('It is a tie')
                whoWins(2)
            time.sleep(5)
            sys.exit('\nGame Over')
        displayScore()
        if createBox2 != -1:
            aiScore += 1
            squaresLeft -= 1
            drawBox(1, createBox2[0], createBox2[1])
            updateScore(1)
            if squaresLeft == 0:
                if aiScore > playerScore:
                    print("AI wins ")
                    whoWins(1)
                elif playerScore > aiScore:
                    print("Player Wins")
                    whoWins(0)
                else:
                    print('It is a tie')
                    whoWins(2)
                time.sleep(5)
                sys.exit('\nGame Over')
            displayScore()
        cpuPlays()
    else:
        pass


# this method will take in identity and the coordinates of the top left corner of the box
# 0 is player, 1 is AI
def drawBox(whoIsIt, coordX, coordY):
    tim.penup()
    tim.goto(coordX + 5, coordY + 5) # looking nice
    tim.setheading(0)
    if whoIsIt == 0:
        tim.color('red')
    else:
        tim.color('blue')
    tim.pendown()
    tim.begin_fill()
    tim.forward(90)
    tim.right(90)
    tim.forward(90)
    tim.right(90)
    tim.forward(90)
    tim.right(90)
    tim.forward(90)
    tim.end_fill()
    tim.penup()
    tim.goto(1000, 1000)



# given a line, it determines if the line taken creates a full box
def isItABox(line):
    returnType = -1
    for key in boxes:
        myList = boxes[key]
        if myList[0].__contains__(line):
            myList[0].remove(line)
            if len(myList[0]) == 0:
                returnType = myList[1]
                break
    return returnType

def updateScore(whoIsIt):
    if whoIsIt == 0:
        tim.penup()
        tim.goto(-440, -450)
        tim.color('lightblue')
        tim.setheading(90)
        tim.pendown()
        tim.begin_fill()
        tim.forward(150)
        tim.right(90)
        tim.forward(150)
        tim.right(90)
        tim.forward(150)
        tim.right(90)
        tim.forward(150)
        tim.setheading(0)
        tim.end_fill()
        tim.penup()
        tim.goto(-440, -450)
        tim.pendown()
        tim.color('RED')
        tim.write(playerScore, font=("Courier", 80, "bold"))
        tim.penup()
        tim.goto(1000, 1000)
    else:
        tim.penup()
        tim.goto(200, -450)
        tim.color('lightblue')
        tim.setheading(90)
        tim.pendown()
        tim.begin_fill()
        tim.forward(150)
        tim.right(90)
        tim.forward(150)
        tim.right(90)
        tim.forward(150)
        tim.right(90)
        tim.forward(150)
        tim.setheading(0)
        tim.end_fill()
        tim.penup()
        tim.goto(200, -450)
        tim.pendown()
        tim.color('blue')
        tim.write(aiScore, font=("Courier", 80, "bold"))
        tim.penup()
        tim.goto(1000, 1000)

def whoWins(whoIsIt):
    if whoIsIt == 0:
        tim.penup()
        tim.goto(300, 0)
        tim.pendown()
        tim.color('red')
        tim.write('Player\nWins!!!', font=("Courier", 100, "bold"))

        data = f'\nPlayer Wins\n\n\n'
        with open('dataFile.txt', 'a') as myFile:
            myFile.write(data)

        tim.penup()
        tim.goto(1000, 1000)
    elif whoIsIt == 1:
        tim.penup()
        tim.goto(300, 0)
        tim.pendown()
        tim.color('blue')
        tim.write('AI\nWins!!!', font=("Courier", 100, "bold"))

        data = f'\nAI Wins\n\n\n'
        with open('dataFile.txt', 'a') as myFile:
            myFile.write(data)

        tim.penup()
        tim.goto(1000, 1000)
    else:
        tim.penup()
        tim.goto(300, 0)
        tim.pendown()
        tim.color('black')
        tim.write('It is\na tie', font=("Courier", 100, "bold"))
        tim.penup()
        tim.goto(1000, 1000)

        data = f'\nIt is a tie\n\n\n'
        with open('dataFile.txt', 'a') as myFile:
            myFile.write(data)

def startGame():
    data = f'Identity\tLine\t\tMinMax Value\n\n'
    with open('dataFile.txt', 'a') as myFile:
        myFile.write(data)

    while True:
        tim.color('black')
        circle1 = int(input('\n\nEnter first coordinate: '))
        circle2 = int(input('Enter second coordinate: '))
        temp = (min(circle1, circle2), max(circle1, circle2))

        data = f'Player\t\t{temp}\n'

        with open('dataFile.txt', 'a') as myFile:
            myFile.write(data)

        if circle1 < 1 or circle1 > 25 or circle2 < 1 or circle2 > 25:
            print('That is an invalid input')
        elif lines.__contains__(temp):
            x1 = coordinates.get(circle1)
            tim.goto(x1[0], x1[1] + 10)
            tim.color('black')
            tim.pendown()
            x2 = coordinates.get(circle2)
            tim.goto(x2[0], x2[1] + 10)
            tim.penup()
            tim.goto(1000, 1000)
            lines.remove(temp)
            createBox = isItABox(temp)
            createBox2 = isItABox(temp)
            if createBox != -1:
                global aiScore
                global playerScore
                playerScore += 1
                global squaresLeft
                squaresLeft -= 1
                drawBox(0, createBox[0], createBox[1])
                updateScore(0)
                if squaresLeft == 0:
                    if aiScore > playerScore:
                        print("AI wins ")
                        whoWins(1)
                    elif playerScore > aiScore:
                        print("Player Wins")
                        whoWins(0)
                    else:
                        print('It is a tie')
                        whoWins(2)
                    time.sleep(5)
                    sys.exit('\nGame Over')
                displayScore()
                if createBox2 != -1:
                    playerScore += 1
                    squaresLeft -= 1
                    drawBox(0, createBox2[0], createBox2[1])
                    updateScore(0)
                    if squaresLeft == 0:
                        if aiScore > playerScore:
                            print("AI wins ")
                            whoWins(1)
                        elif playerScore > aiScore:
                            print("Player Wins")
                            whoWins(0)
                        else:
                            print('It is a tie')
                            whoWins(2)
                        time.sleep(5)
                        sys.exit('\nGame Over')
                    displayScore()
            else:
                cpuPlays()
        else:
            print('That is an invalid input\n\n')

startGame()
turtle.done()