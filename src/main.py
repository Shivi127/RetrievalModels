from TermAtaTimeR import TRetrival
from Compressed import CompressedIndex
from parse import Parse

p = Parse()
t = TRetrival()

Qarray=["the king queen royalty","servant guard soldier","hope dream sleep","ghost spirit","fool jester player",
        "to be or not to be","alas", "alas poor", "alas poor yorick","antony strumpet"]

trecrun = "shivangising-vectorspace"


file = open("vecctorspace.trecrun", "w")



rank = 1
for i,q in enumerate(Qarray,1):
    Q = q.split(" ")
    print("Doing the BM25 Retrival for ",q)
    print()
    x = t.TermAtATime(Q, 1000, "BM25")


    for element in x:
        QueryNumber = "Q" + str(i)
        scene = p.getScene(element[0])
        score = element[1]
        file.write(QueryNumber + " " + "skip" + " "+ scene +" "+ str(rank) + " " + str(score) + " " + trecrun + "\n")
        rank+=1

file.close()