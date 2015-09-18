import time
import datetime
import csv
import trueskill



class TPlayer(object):
    skill = (25.0, 25.0/3.0)
    rank = 1
    gamesPlayed = 0


    def __init__(self,player_id, firstname,lastname,hand,datebirth,nationality):
        self.player_id = player_id
        self.firstname = firstname
        self.lastname = lastname
        self.hand = hand
        self.datebirth = datebirth
        self.nationality = nationality

    def getSummaryStats(self):
        return "skill= {:.1f} stdev= {:.1f} games= {} name= {} {}".format(self.skill[0],
                                                                          self.skill[1],
                                                                          self.gamesPlayed,
                                                                          self.firstname,
                                                                          self.lastname)



def getKey(item):
    return item.skill[0]



if __name__ == "__main__":

    ######################
    # initial variables
    ######################
    startTime = time.clock()
    playerDict = {}



    #########################
    # import all players IDs
    #########################
    csvfilename = './data/atp_players.csv'
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
    countTotGames = 0
    csvfilename = './data/atp_matches_2015.csv'
    with open(csvfilename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            winner = playerDict[row['winner_id']]
            looser = playerDict[row['loser_id']]
            winner.rank = 1
            looser.rank = 2

            trueskill.AdjustPlayers([winner, looser])
            winner.gamesPlayed += 1
            looser.gamesPlayed += 1

            countTotGames += 1

    ##################
    # print results
    ##################
    playerList = playerDict.values()
    playerList = sorted(playerList, key=getKey, reverse=True)

    i = 0
    while i < 50:
        print playerList[i].getSummaryStats()
        i += 1

    print ""
    print "time taken(s): {:.2f} for total of {} games".format(time.clock() - startTime, countTotGames)

