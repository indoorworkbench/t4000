import time
import datetime
import csv
import trueskill
import functions
from scipy.stats.distributions import norm as scipy_norm
from math import sqrt
import matplotlib.pyplot as plt





class TPlayer(object):
    def __init__(self,player_id, firstname,lastname,hand,datebirth,nationality):
        self.player_id = player_id
        self.firstname = firstname
        self.lastname = lastname
        self.hand = hand
        self.datebirth = datebirth
        self.nationality = nationality
        self.skillHistory = []
        self.gamesPlayed = 0
        self.rank = 1
        self.skill = (25.0, 25.0/3.0)

    def getSummaryStats(self):
        return "skill= {:.1f} stdev= {:.1f} games= {} name= {} {}".format(self.skill[0],
                                                                          self.skill[1],
                                                                          self.gamesPlayed,
                                                                          self.firstname,
                                                                          self.lastname)

    def recordHistory(self,dateplayed):
        dateObj = datetime.datetime.strptime(dateplayed, '%Y%m%d')
        self.skillHistory.append((dateObj,self.skill[0],self.skill[1]))
        self.gamesPlayed += 1



def getKey(item):
    return item.skill[0]


def winProb(p1,p2):
    norm = scipy_norm()
    cdf = norm.cdf
    deltaMu = p1.skill[0] - p2.skill[0]
    rsss = sqrt(p1.skill[1]**2 + p2.skill[1]**2)

    print cdf(deltaMu/rsss)

    plt.plot([x[1] for x in p1.skillHistory])
    plt.plot([x[1] for x in p2.skillHistory])
    plt.show()



if __name__ == "__main__":

    ######################
    # initial variables
    ######################
    strDir = './data/matches/'
    startTime = time.clock()
    playerDict = {}



    #########################
    # import all players IDs
    #########################
    csvfilename = strDir + 'atp_players.csv'
    with open(csvfilename) as csvfile:
        fieldnames =['player_id','firstname','lastname','hand','datebirth','nationality']
        reader = csv.DictReader(csvfile, fieldnames)
        for row in reader:
            pObj = TPlayer(row['player_id'],
                        row['firstname'],
                        row['lastname'],
                        row['hand'],
                        row['datebirth'],
                        row['nationality'])
            playerDict[pObj.player_id] = pObj

    ########################
    # loop through game data and
    # update player's skills
    ########################
    fileList = functions.getMatchesFileNames(strDir)
    countTotGames = 0

    trueskill.SetParameters(beta=None,
                            epsilon=None,
                            draw_probability=0,
                            gamma=1)

    for csvfilename in fileList:
        csvfilename = strDir + csvfilename
        with open(csvfilename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:

                winner = playerDict[row['winner_id']]
                looser = playerDict[row['loser_id']]
                winner.rank = 1
                looser.rank = 2

                trueskill.AdjustPlayers([winner, looser])
                winner.recordHistory(row['tourney_date'])
                looser.recordHistory(row['tourney_date'])

                countTotGames += 1

                #print every 1000 games
                if (countTotGames/1000.0).is_integer():
                    print countTotGames

    ##################
    # print results
    ##################
    playerList = playerDict.values()
    playerList = sorted(playerList, key=getKey, reverse=True)


    i = 0
    while i < 100:
        print str(i) + ' ' + str(playerList[i].getSummaryStats())
        i += 1

    winProb(playerList[0],playerList[1])
    print ""
    print "time taken(s): {:.2f} for total of {} games".format(time.clock() - startTime, countTotGames)

