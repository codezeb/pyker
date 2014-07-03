'''
DATE CREATED:  14-05-2014
DATE FINISHED: 21-05-2014
CREATOR:       Martin Dessauer
CONTACT:       martin.dessauer@me.com, @codezeb (Github)
COPYRIGHT:     2014 Martin Dessauer
LICENSE:       GPLv3
'''

import sys # for sys.argv
import getch # reading input (arrow keys)
from binascii import hexlify # l158
from time import sleep # ... guess.
from random import randint,shuffle # should be obvious aswell



''' SETTINGS '''

cash      = 200
minBet    = 100
unit      = "$"
winset    = ["JACKS OR BETTER","TWO PAIRS","PAIR O' THREE","STRAIGHT","FLUSH","FULL HOUSE","PAIR O' FOUR","STRAIGHT FLUSH","ROYAL FLUSH"]
payset    = [1,2,3,4,6,9,25,50,250] # multiplies with bet/minBet 
betset    = [1,2,5,10,50,100,250] # factor
charset   = ["A","K","D","B","10","9","8","7","6","5","4","3","2"]
cardtypes = ["♠","♣","♥","♦"] # 2x black, 2x red
version   = "1.0b"

# DO NOT TOUCH THIS.
bet       = 0

''' PARAMETER SETUP '''

for i in range(1,len(sys.argv)):
	if(sys.argv[i][:2] == "-c"):
		cash = int(sys.argv[i][2:])


''' FUNCTIONS '''

def initCards(): # builds up the deck
	global charset,cardtypes
	cardset = []
	for i in range(0,len(charset)):
		for j in range(0,len(cardtypes)):
			if(len(charset[i]) == 1):
				cardset.append(charset[i] + "  " + cardtypes[j])
			else:
				cardset.append(charset[i] + " " + cardtypes[j])
	return cardset

def gameLoop(): # is called upon start and enters an eternal loop (runs alas person got enough cash ;) )
	firstRun = True
	global cash,bet

	print("Pyker v" + version)
	sleep(1)

	if(len(winset) != len(payset)):
		print("Configuration error! (|winSet| != |paySet|)")
	if(cash < minBet):
		print("Configuration error! (cash < minBet)")
		Quit()

	print("\033[2A")

	while(not cash<minBet):
		print("You've got \033[92m" + str(cash) + unit + "\033[0m.")
		if(not firstRun):
			if(choice("Continue with bets?",["Yes","No"]) == "No"):
				end()
		else:
			firstRun = False
			bet = 0
		betPossibilities = []
		for i in range(0,len(betset)-1):
			if(cash>=betset[i]*minBet):
				betPossibilities.append(str(betset[i]*minBet)+unit)
		bet  = int(choice("Place your bet:",betPossibilities,0)[:-1])
		cash = cash - bet
		cards()
	# We just arrive here if cash<minBet.
	choice("\n\033[31mYou ran out of money!\033[0m",["Exit"])

def winType(wT): # prints out the thing we've won.
	global cash
	print("You've got a \033[32m" + winset[wT-1] + "\033[0m! \033[32m+" + str(payset[wT-1]*bet) + unit + "\033[0m")
	cash = cash + payset[wT-1]*bet


def analyseCards(randomCards): # analyses the cards the player got
	cleanCards = [] # stores pure int values w/o card type
	sameType = False
	print("\r                                           \r",end="")
	for i in range(0,5):
		cleanCards.append(int(randomCards[i][:2].replace(" ","").replace("B","11").replace("D","12").replace("K","13").replace("A","14")))

	cleanCards.sort()

	if(randomCards[0][-1] == randomCards[1][-1] == randomCards[2][-1] == randomCards[3][-1] == randomCards[4][-1]):
		sameType = True
		if(sum(cleanCards) == 60):
			winType(9) # royal flush
		elif(cleanCards[0]+4 == cleanCards[1]+3 == cleanCards[2]+2 == cleanCards[3]+1 == cleanCards[4]):
			winType(8) # straight flush
		else:
			winType(5) # flush
	elif(cleanCards[0] == cleanCards[1] == cleanCards[2] == cleanCards[3]) or (cleanCards[1] == cleanCards[2] == cleanCards[3] == cleanCards[4]):
		winType(7) # pairo 4
	elif(cleanCards[0] == cleanCards[1] == cleanCards[2] and cleanCards[3] == cleanCards[4]) or (cleanCards[0] == cleanCards[1] and cleanCards[2] == cleanCards[3] == cleanCards[4]):
		winType(6) # full house
	elif(cleanCards[0]+4 == cleanCards[1]+3 == cleanCards[2]+2 == cleanCards[3]+1 == cleanCards[4]):
		winType(4) # straight
	elif(cleanCards[0] == cleanCards[1] == cleanCards[2]) or (cleanCards[1] == cleanCards[2] == cleanCards[3]) or (cleanCards[2] == cleanCards[3] == cleanCards[4]):
		winType(3)  #  pairo 3
	elif(((cleanCards[0] == cleanCards[1]) and (cleanCards[2] == cleanCards[3])) or ((cleanCards[1] == cleanCards[2]) and (cleanCards[3] == cleanCards[4])) or ((cleanCards[0] == cleanCards[1]) and (cleanCards[3] == cleanCards[4]))):
		winType(2)  #  2pairs
	elif((cleanCards[0] + cleanCards[1] >= 22) and (cleanCards[0] == cleanCards[1])) or ((cleanCards[1] + cleanCards[2] >= 22) and (cleanCards[1] == cleanCards[2])) or ((cleanCards[2] + cleanCards[3] >= 22) and (cleanCards[2] == cleanCards[3])) or ((cleanCards[3] + cleanCards[4] >= 22) and (cleanCards[3] == cleanCards[4])):
		winType(1)  #  jack o better
	else:
		print("\033[31mNothing\033[0m. \033[31m-" + str(bet) + unit + "\033[0m")

def cards(): # shuffles & presents cards to user
	tmpCardset = initCards()
	randomCards = []
	selection = 0
	keep = [False,False,False,False,False]
	dropout = False

	for i in range(0,5):
		shuffle(tmpCardset)
		index = randint(0,len(tmpCardset)-1)
		randomCards.append(tmpCardset[index])
		print(" " + randomCards[i] + "  ",end="")
		tmpCardset.remove(tmpCardset[index])
	
	print("\n")
	######################
	while(not dropout):
		print("\033[1A",end="")
		for i in range(0,5):
			if(i==selection):
				if(keep[i]):
					print("\033[7m[KEEP]\033[0m ",end="")
				else:
					print("\033[7m[    ]\033[0m ",end="")
			else:
				if(keep[i]):
					print("[KEEP] ",end="")
				else:
					print("[    ] ",end="")
		if(5==selection):
			print("\033[7m[ACCEPT]\033[0m ")
		else:
			print("[ACCEPT]")

		key = getch.getch()
		if(hexlify(bytes(key,"UTF-8")) != bytes("1b","UTF-8")):
			if(selection==5):
				dropout = True
			else:
				keep[selection] = not keep[selection]
		else:
			getch.getch()      # \_ SIC!
			key = getch.getch()# /
			if(key == "D"):
				if(selection>0):
					selection = selection - 1
			elif(key == "C"):
				if(selection<5):
					selection = selection + 1
	print("\033[3A")
	for i in range(0,5):
		shuffle(tmpCardset)
		if(keep[i]):
			print(" " + randomCards[i] + "  ",end="")
		else:
			index = randint(0,len(tmpCardset)-1)
			randomCards[i] = tmpCardset[index]
			print(" " + randomCards[i] + "  ",end="")
			tmpCardset.remove(tmpCardset[index])
	print("")
	sleep(1)
	analyseCards(randomCards)

def choice(question,options,selection = 0): # selection prompt
	print("") # so that \033[1A gets a fresh new line on *first* cycle
	while(True):
		print("\033[1A" + question,end="")
		for i in range(0,len(options)):
			if(i==selection):
				print(" \033[7m[" + str(options[i]) + "]\033[0m ",end="")
			else:
				print("  " + str(options[i]) + "  ",end="")
		print("")

		key = getch.getch()
		if(key == "\n"):
			return options[selection]
		else:
			getch.getch()      # \_ SIC!
			key = getch.getch()# /
			if(key == "D"):
				if(selection>0):
					selection = selection - 1
			elif(key == "C"):
				if(selection<len(options)-1):
					selection = selection + 1

def end():
	print("Thanks for playing! :)")
	exit()

''' GAME LOOP '''

gameLoop()