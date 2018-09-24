Simple poker script that allows you to see the chances of getting each hand.

To use:

1. Run "python stacks.py" (currently, must be done in Python 3)
2. Enter 2 cards for preflop, then 3 for flop, then 1 for turn.

The format of all the cards is [V][S], where:

	V is a card value (integer from 2-10 or J/Q/K/A for jack/queen/king/ace)
	
	S is the first letter of the desired suit (C/D/H/S)

Examples:

10S JC (10 of spades, jack of clubs)

7D KH AH (7 of diamonds, king of hearts, 10 of hearts)

QH (queen of hearts)
