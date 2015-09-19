import os
from fnmatch import fnmatch
import re
from operator import itemgetter

def getMatchesFileNames(strDir):
    fileList = []
    for fn in os.listdir(strDir):
        if fn.endswith('.csv'):
            if fnmatch(fn,'atp_matches*'):
                m = re.match(r".*(\d{4})\.csv",fn) #match 4 consecutive numbers
                fileList.append([fn,int(m.group(1))])

    fileList = sorted(fileList, key=itemgetter(1), reverse=False)
    return [x[0] for x in fileList]



if __name__ == "__main__":
    #test
    getMatchesFileNames('./data/matches/')