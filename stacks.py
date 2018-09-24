import collections
from enum import IntEnum

#various useful constants
JACK, QUEEN, KING, ACE = 11, 12, 13, 14
PREFLOP_HANDS = 2118760 #50 choose 5
FLOP_HANDS = 1081 #47 choose 2
TURN_HANDS = 46
UNIQUE_POCKETS = 169

class Hand(IntEnum):
	HIGH_CARD = 0
	ONE_PAIR = 1
	TWO_PAIR = 2
	TRIPLES = 3
	STRAIGHT = 4
	FLUSH = 5
	FULL_HOUSE = 6
	QUADS = 7
	STRAIGHT_FLUSH = 8
	ROYAL_FLUSH = 9

def sort(buckets, card_list): #chooses the best 5-card hand from a set of 7
	a, b, c, d, e, f, g = card_list[0:7]
	v = len({a[0], b[0], c[0], d[0], e[0], f[0], g[0]})
	s = len({a[1], b[1], c[1], d[1], e[1], f[1], g[1]})

	if s <= 3: #potential flush
		suit_counter = collections.Counter([i[1] for i in card_list]) #number of each suit there is
		if not {5, 6, 7}.isdisjoint(suit_counter.values()): #at least 5 of one suit - definitely a flush
			flush_list = [card[0] for card in card_list if suit_counter[card[1]] >= 5]
			if flush_list[-1] == ACE:
				if flush_list[-5] == 10: #royal flush
					buckets[Hand.ROYAL_FLUSH] += 1
					return
				if flush_list[3] == 5: #A-5 straight flush
					buckets[Hand.STRAIGHT_FLUSH] += 1
					return
				#if we have an ace and a separate straight flush of the same suit, we drop to the next if statement

			if (flush_list[4] - flush_list[0] == 4
					or (len(flush_list) > 5 and flush_list[5] - flush_list[1] == 4)
					or (len(flush_list) > 6 and flush_list[6] - flush_list[2] == 4)): #straight flush (not containing ace)
				buckets[Hand.STRAIGHT_FLUSH] += 1
				return

			else: #4card and full house are impossible since both require 3 cards of another suit
				buckets[Hand.FLUSH] += 1
				return 

	if v <= 4: #must be true for four of a kind and full house
		value_counter = collections.Counter([i[0] for i in card_list]) #number of each value there is
		values = list(value_counter.values())
		if 4 in values: #four of a kind
			buckets[Hand.QUADS] += 1
			return
		if 3 in values:
			values.remove(3)
			if 3 in values or 2 in values: #full house (we can have 3 triples in a 7-card hand)
				buckets[Hand.FULL_HOUSE] += 1
				return

	if v >= 5: #potential straight
		values_list = list(sorted({a[0], b[0], c[0], d[0], e[0], f[0], g[0]})) #list of values, ignoring suits and pairs/triples
		if (values_list[4] - values_list[0] == 4
					or (len(values_list) > 5 and values_list[5] - values_list[1] == 4)
					or (len(values_list) > 6 and values_list[6] - values_list[2] == 4)): #straight
			buckets[Hand.STRAIGHT] += 1
			return

		if values_list[-1] == ACE: #check for A-5 straight
			if values_list[3] == 5 and values_list[3] - values_list[0] == 3:
				buckets[Hand.STRAIGHT] += 1
				return

	if v <= 6: ##check for pairs and triples
		value_counter = collections.Counter([i[0] for i in card_list]) #same as quad check
		values = list(value_counter.values())
		if 3 in values:
			buckets[Hand.TRIPLES] += 1
			return
		if 2 in values:
			values.remove(2)
			if 2 in values: #two pairs, all higher possibilities removed by this point
				buckets[Hand.TWO_PAIR] += 1
				return 
			buckets[Hand.ONE_PAIR] += 1
			return

	buckets[Hand.HIGH_CARD] += 1
	return

#take an inputted number and convert it to the right value
def string_to_card(card):
	val, suit = 0, ' '
	if card[0].isdigit():
		if len(card) == 3:
			val = 10
			suit = card[2]
			return (val, char_to_suit(suit))

		val = int(card[0])
	else:
		if card[0] == 'J':
			val = JACK
		elif card[0] == 'Q':
			val = QUEEN
		elif card[0] == 'K':
			val = KING
		elif card[0] == 'A':
			val = ACE
	suit = card[1]
	return (val, char_to_suit(suit))

def char_to_suit(chr):
	if chr == 'C':
		return 0
	if chr == 'D':
		return 1
	if chr == 'H':
		return 2
	if chr == 'S':
		return 3
	return -1

def enum_to_lowercase(enum_str):
	return enum_str.lower().replace("_", " ")

def print_probs(p_list, total_hands):
	for i in range(10):
		print("Chance of getting a",  enum_to_lowercase(Hand(i).name), "is", \
				str(round(p_list[i]*100, 4)) + "% (" + str(int(p_list[i]*total_hands)) + "/" + str(total_hands) + ")")

def preflop():
	global p_list, h1, h2
	val1, suit1 = string_to_card(h1)
	val2, suit2 = string_to_card(h2)
	CARD_INDEX_1, CARD_INDEX_2, SUITED = 0, 1, 2

	print("Computing preflop percentages...")

	f = open("hands.txt", "r")
	arr = [None]*UNIQUE_POCKETS
	for pair in range(UNIQUE_POCKETS):
		arr[pair] = f.readline().split()
		assert(len(arr[pair]) == 13) #check data is intact
		
	target_condition = "suited"
	if suit1 != suit2:
		target_condition = "unsuited"

	target_hand = [x for x in arr if (int(x[0]) == val1 and int(x[1]) == val2 
		or int(x[1]) == val1 and int(x[0]) == val2) and x[2] == target_condition]
	assert(len(target_hand) == 1) #check target data for chosen pair exists and is unique
	p_list = [float(prob)/PREFLOP_HANDS for prob in target_hand[0][3:13]]
	print_probs(p_list, PREFLOP_HANDS)	

def flop():
	global li, h1, h2, c1, c2, c3
	a = string_to_card(h1)
	b = string_to_card(h2)
	c = string_to_card(c1)
	d = string_to_card(c2)
	e = string_to_card(c3)
	buckets = [0]*10
	print("Computing flop percentages...")

	li = [elt for elt in li if elt not in [a, b, c, d, e]]
	for f in range(len(li)):
		for g in range(f + 1, len(li)):
			sl = [a, b, c, d, e, li[f], li[g]]
			sl.sort(key=lambda x: x[0])					
			sort(buckets, sl)

	p_list = [float(bucket)/FLOP_HANDS for bucket in buckets]
	print_probs(p_list, FLOP_HANDS)


def turn():
	global li, h1, h2, c1, c2, c3, c4
	a = string_to_card(h1)
	b = string_to_card(h2)
	c = string_to_card(c1)
	d = string_to_card(c2)
	e = string_to_card(c3)
	f = string_to_card(c4)
	buckets = [0]*10
	print("Computing turn percentages...")

	li = [elt for elt in li if elt not in [a, b, c, d, e, f]]
	for g in range(len(li)):
		sl = [a, b, c, d, e, f, li[g]]
		sl.sort(key=lambda x: x[0])					
		sort(buckets, sl)

	p_list = [float(bucket)/TURN_HANDS for bucket in buckets]
	print_probs(p_list, TURN_HANDS)

li = [(x+2, y) for x in range(13) for y in range(4)]



p_list = [0.0]*10
h1, h2 = input("Enter hole cards: ").split()
preflop()
c1, c2, c3 = input("Enter flop cards: ").split()
flop()
c4 = input("Enter turn card: ")
turn()
