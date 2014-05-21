pyker ![python logo](https://www.python.org/static/community_logos/python-powered-h-50x65.png)
=====

##### What and Why?

**pyker** is a small video poker implementation written in Python (v3).

I was both bored and interesting in implementing a simple, small game.

![example gif](http://i.imgur.com/cUe5lsi.gif)

##### Arguments
`-c###` Changes the default cash the player got upon start to ###. (ex.: `python3 pyker.py -c500` for 500$)

##### Default settings hacking
The variables which control the game appearance are round the lines 19 to 28:

`cash` contains the default cash, may be overwritten with `-c`

`minBet` the minimum to bet. :P

`unit` the unit. May be "$" or "€", for example

`winset` the names ("JACKS", for example), and

`payset` the corresponding factors (1,2,5,...) for the possible wins

`betset` betset * minBet = Possibilities to bet. ("100, 200, 500, ..." for example)

`charset` the possible cards ("A","B","5","10",...)

`cardtypes` the possible cardtypes ("♠","♣","♥","♦")

`version` the version.


##### Function reference

`def initCards():` builds up the deck.

`def gameLoop():` is called upon start and enters an eternal loop. Drops out if player got no cash left.

`def winType(wT):` prints out the thing the player has won.

`def analyseCards(randomCards):` analyses the cards the player got.

`def cards():` shuffles & presents cards to user.

`def choice(question,options,selection = 0):` general selection prompt.

`def end():` stops the game.
