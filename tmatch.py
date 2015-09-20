

###############
# Match Class
###############
class TMatch(object):
    def __init__(self,nSets):
        self.sets = []
        self.nSets = nSets
        self.playerWon = 0
        self.scoreSets = [0,0]
        self.addSet()
        self.__pserving = 0

    def addSet(self):
        tSetObj = TSet()
        self.sets.append(tSetObj)

    def addPoint(self,char):
        #only accept S,R,A,D
        if char in ('S','R','A','D') and self.playerWon == 0:

            ####################################
            # Keep track of who is serving next
            ####################################
            lset = self.sets[-1]
            lgame = lset.games[-1]


            if lgame.playerServing == 0:
                if self.__pserving == 0:
                    lgame.playerServing = 1
                    self.__pserving = 1
                else:
                    self.__pserving = self.__pserving*-1
                    lgame.playerServing = self.__pserving


            #########################
            # ADD point
            #########################
            self.sets[-1].games[-1].addPoint(char)


            #########################
            # POST point check score
            #########################


            #check if game has finished
            if lgame.playerWon != 0:
                if lgame.playerWon == 1:
                    lset.scoreGames[0] += 1
                elif lgame.playerWon == -1:
                    lset.scoreGames[1] += 1

                lset.isSetWon()

                if lset.playerWon == 0:
                    lset.addGame()



            # check if set has finished
            if lset.playerWon != 0:
                if lset.playerWon == 1:
                    self.scoreSets[0] += 1
                elif lset.playerWon == -1:
                    self.scoreSets[1] += 1

                # check if the match has finished
                if sum(self.scoreSets) == self.nSets:
                    if self.scoreSets[0] > self.scoreSets[1]:
                        self.playerWon = 1
                    else:
                        self.playerWon = -1
                else:
                    self.addSet()



#############
# Set Class
############
class TSet(object):
    def __init__(self):
        self.games = []
        self.playerWon = 0
        self.scoreGames = [0,0]
        self.addGame()

    def addGame(self):
        tGameObj = TGame()
        if sum(self.scoreGames) == 12: #check if next game is tiebreak
            tGameObj.isTB = True

        self.games.append(tGameObj)


    def isSetWon(self):
        maxscore = max(self.scoreGames)
        scorediff = self.scoreGames[0] - self.scoreGames[1]
        if maxscore > 5:
            if (abs(scorediff) > 1 and self.games[-1].isTB == False) or (abs(scorediff) == 1 and self.games[-1].isTB == True):
                if scorediff > 0:
                    self.playerWon = 1
                else:
                    self.playerWon = -1




#############
# Game Class
############
class TGame(object):
    def __init__(self):
        self.points = []
        self.playerServing = 0
        self.playerWon = 0
        self.scorePoints = [0,0]
        self.isTB = False

    def addPoint(self,char):
        tObj = TPoint()

        #interchange serving on odd points in tiebreaks
        tmpServ = self.playerServing
        if self.isTB:
            if sum(self.scorePoints)%4 in (1,2):
                tmpServ = self.playerServing*-1

        tObj.playerServing = tmpServ

        if char == 'S':
            tObj.playerWon = tmpServ

        elif char == 'A':
            tObj.playerWon = tmpServ
            tObj.isAce = True

        elif char == 'R':
            tObj.playerWon = tmpServ*-1

        elif char == 'D':
            tObj.playerWon = tmpServ*-1
            tObj.isDFault = True


        self.points.append(tObj)
        self.updateGameScores()

        #check if the game has been won
        self.isGameWon()

    def updateGameScores(self):
        winner = self.points[-1].playerWon
        y = int((winner-1)*-0.5) #trick to convert (1,-1) to (0,1)
        self.scorePoints[y] += 1



    def isGameWon(self):
        maxscore = max(self.scorePoints)
        score = self.scorePoints[0] - self.scorePoints[1]

        if abs(score) > 1 and maxscore > 3:
            if (self.isTB == False) or (self.isTB == True and maxscore > 6):
                if score > 1:
                    self.playerWon = 1
                else:
                    self.playerWon = -1



###############
# Point Class
###############
class TPoint(object):
    def __init__(self):
        self.playerServing = 0
        self.playerWon = 0
        self.isAce = False
        self.isDFault = False
        self.isBP = False


def getCurrentScore(tMatchObj):
    print "pl | sets | games | points"
    print "p1 |   {}       {}      {}".format(tMatchObj.scoreSets[0], tMatchObj.sets[-1].scoreGames[0], tMatchObj.sets[-1].games[-1].scorePoints[0])
    print "p2 |   {}       {}      {}".format(tMatchObj.scoreSets[1], tMatchObj.sets[-1].scoreGames[1], tMatchObj.sets[-1].games[-1].scorePoints[1])





if __name__ == "__main__":
    import random
    import time

    x = 0
    startTime = time.clock()

    tmpStr = 'RDRSASSS;SRSSRS;RSSSS;RRSRR;SSSRRS;SSRRSS;RSARRD;SRSSS;RSSSA;RSDRR.SRSSS;SRARRSSRSRSS;RSRRR;SRRSDD;SSSRS;SSSS;RSSSRS;SSSDRRSRRSSRSRSS;SRRRSR;SDSSS.RRSSSS;DRSSSA;SSSS;SRRSSRRSSRRSSS;SSRSS;RRDR;SSSS;SSSA;SSSS'
    tMatchObj = TMatch(3) #number of sets

    for i in xrange(0,len(tmpStr)):
        char = tmpStr[i]
        tMatchObj.addPoint(char)

    getCurrentScore(tMatchObj)

    print "time taken(s): {:.2f}".format(time.clock() - startTime)


    ############ some monte carlo #################
    # for m in range(1,100):
    #     tmpStr = "".join(random.choice('SR') for x in range(1,1000))
    #     tMatchObj = TMatch(3) #number of sets
    #
    #     for i in xrange(0,len(tmpStr)):
    #         char = tmpStr[i]
    #         tMatchObj.addPoint(char)
    #
    #
    #     if tMatchObj.playerWon == 1: x += 1
    #
    # getCurrentScore(tMatchObj)
    # print "{:.4f}".format(float(x)/float(m))
