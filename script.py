import os

for i in range(15):
    j = 0 
    j+=1
    print "Ronda " + str(i) + "." + str(j)
    os.system("python2 busters.py -p QLearningAgent -l labAA2 -k 2 -t 0.01")
    j+=1
    print "Ronda " + str(i) + "." + str(j)
    os.system("python2 busters.py -p QLearningAgent -l labAA2 -k 2 -t 0.01 -g RandomGhost")
    j+=1
    print "Ronda " + str(i) + "." + str(j)
    os.system("python2 busters.py -p QLearningAgent -l labAA2a -k 2 -t 0.01")
    j+=1
    print "Ronda " + str(i) + "." + str(j)
    os.system("python2 busters.py -p QLearningAgent -l labAA2a -k 2 -t 0.01 -g RandomGhost")
    j+=1
    print "Ronda " + str(i) + "." + str(j)
    os.system("python2 busters.py -p QLearningAgent -l labAA2b -k 2 -t 0.01")
    j+=1
    print "Ronda " + str(i) + "." + str(j)
    os.system("python2 busters.py -p QLearningAgent -l labAA2b -k 2 -t 0.01 -g RandomGhost")
    j+=1
    print "Ronda " + str(i) + "." + str(j)
    os.system("python2 busters.py -p QLearningAgent -l labAA2c -k 2 -t 0.01")
    j+=1
    print "Ronda " + str(i) + "." + str(j)
    os.system("python2 busters.py -p QLearningAgent -l labAA2c -k 2 -t 0.01 -g RandomGhost")
    j+=1
    print "Ronda " + str(i) + "." + str(j)
    os.system("python2 busters.py -p QLearningAgent -l labAA2d -k 2 -t 0.01")
    j+=1
    print "Ronda " + str(i) + "." + str(j)
    os.system("python2 busters.py -p QLearningAgent -l labAA2d -k 2 -t 0.01 -g RandomGhost")
    j+=1
    print "Ronda " + str(i) + "." + str(j)
    os.system("python2 busters.py -p QLearningAgent -l labAA3 -k 3 -t 0.01")
    j+=1
    print "Ronda " + str(i) + "." + str(j)
    os.system("python2 busters.py -p QLearningAgent -l labAA3 -k 3 -t 0.01 -g RandomGhost")

