import datetime

def totimestamp(dt, epoch=datetime.datetime(1970,1,1)):
    #timestamp in milliseconds
    td = dt - epoch
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6)/1000

if __name__ == "__main__":
    startDate = datetime.datetime(2014,03,18,07,00,0)
    startEpoch = totimestamp(startDate)
    print (startEpoch)

