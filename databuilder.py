from stacks import card_sort
import sys

f = open("hands.txt", "w")
count = 0
buckets = [0]*10
li = [(x+2, y) for x in range(13) for y in range(4)]
for lefthand in range(13):
	for second in range(lefthand*2+1, 26):
		righthand = (second/2)*4 + (second%2)
		buckets = [0 for elt in buckets]
		count += 1
		print("Calculating odds for starting hand " + str(count) + "/169...")
		print("Hand " + str(li[lefthand]) + ", " + str(li[righthand]) + ":")

		h1 = li[lefthand*4]
		h2 = li[righthand]
		li.remove(li[righthand])
		li.remove(li[lefthand*4])

		un = "un"*(second%2)
		id_str = str(h1[0]) + " " + str(h2[0]) + " " + un + "suited "
		print(id_str)

		for a in range(len(li)):
			for b in range(a+1, len(li)):
				for c in range(b+1, len(li)):
					for d in range(c+1, len(li)):
						for e in range(d+1, len(li)):
							sl = [h1, h2, li[a], li[b], li[c], li[d], li[e]]
							sl.sort(key=lambda x: x[0])					
							sort(buckets, sl)

		print(buckets)
		
		f.write(id_str + " ".join([str(i) for i in buckets]) + "\n")
		li = [(x+2, y) for x in range(13) for y in range(4)]
f.close()