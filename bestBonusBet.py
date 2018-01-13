from sportsbet import createSportsBetNBAMatchups
from crownBet import createCrownBetNBAMatchups
from neds import createNedsNBAMatchup
from ubet import createUBetNBAMatchup
from tabulate import tabulate
import sys
agencyFunctions = {'CrownBet' : createCrownBetNBAMatchups, 'SportsBet': createSportsBetNBAMatchups,
'Neds': createNedsNBAMatchup, 'UBet' : createUBetNBAMatchup}



#Creates the matchup objects so we can compare them against each other.
def createCandidates(bonusBetAgency):
    #First retrieve the odds for the agency with the bonus bet, it will go
    #into agencyCandidates first\
    agencyCandidates = {}
    agencyCandidates[bonusBetAgency] = agencyFunctions[bonusBetAgency]()
    # agencyCandidates.append(agencyFunctions[bonusBetAgency]())

    #then go through the other agencies and create their oddds lists.
    for agency in agencies:
        if agency != bonusBetAgency:
            agencyCandidates[agency] = agencyFunctions[agency]()


    #we return a list of list of tuples, with teams and odds.
    return agencyCandidates

#Goes through the odds in the bonus bet agency
#and initialises a dictionary with the team with the
#highest odds as the key.
def createBonusDict(candidates):
    bonusDict = {}
    for matchup in candidates:
        #Because the matchups are sorted with highest odds first,
        #just need to add the team with the highest odds into the dict.
        bonusDict[matchup[0][0]] = matchup[0][1]
    return bonusDict

#takes as input the bonusTeam tuple, and the dictionary of agencies
def findBestOpponent(bonusTeam, agencies):
    highestPercent = 0
    bestOpponent = ()
    bestAgency = ""
    found = False
    #Loop through each agency
    for agency in agencies.keys():
        if agency != bonusBetAgency:
        #And then loop through each pair of teams
            for teams in agencies[agency]:
                #We changed it to just compare the teamName (e.g. instead of "Philadelphia 76ers",
                #just compare "76ers"), because UBet is shit and they format their names weird
                teamName = teams[0][0].split(' ')[-1]

                ###### if (teams[0][0] == bonusTeam[0] and \
                ####### calculatePercent(bonusTeam[1], teams[1][1]) > highestPercent):

                #If it's the matchup and the  percentage return is the highest,
                if (teamName == bonusTeam[0].split(' ')[-1] and \
                 calculatePercent(bonusTeam[1], teams[1][1]) > highestPercent):
                    #store the data of the best team.
                    found = True
                    highestPercent = calculatePercent(bonusTeam[1], teams[1][1])
                    bestOpponent = teams[1]
                    bestAgency = agency
    if found:
        return (bestAgency, bestOpponent, highestPercent)
    else:
        return None


#calculates the percentage return from the bonus bets.
def calculatePercent(odd1, odd2):
    profit = float(odd1) - 1
    hedge = profit/float(odd2)

    percentReturn = profit - hedge
    return percentReturn

def findBet(bonusBetAgency):
    #So now we have the candidates which we can compare the teams in the
    #dictionary of the bonus Agency against
    agencies = createCandidates(bonusBetAgency)
    bonusDict = createBonusDict(agencies[bonusBetAgency])
    matchupList = []
    #loop through each agency in the bonus agency,
    for bonusTeam in bonusDict.keys():
        bestMatchup = []
        #then find the best opponent
        bestOpponent = findBestOpponent((bonusTeam, float(bonusDict[bonusTeam])), agencies)
        #append all the matchup info into bestMatchup into a format that allows
        #us to print it easily later on
        if bestOpponent is not None:
            bestMatchup = [bonusBetAgency, bonusTeam, bonusDict[bonusTeam],
            bestOpponent[0], bestOpponent[1][0], bestOpponent[1][1], bestOpponent[2]]
        #then put the list into the list of matchups.
            matchupList.append(bestMatchup)

    #then, return matchupList sorted by highest percentage first.
    matchupList = sorted(matchupList, key=lambda percent: percent[6], reverse=True)
    return matchupList

def printBets(betList):
    print(tabulate(betList, headers = ["Bonus Bet Agency", "Team", "Odds", "Opposing Team Agency", "Team", "Odds", "Return"]))

    return 0

def calculateBet(betList):
    print("\n")
    bonusBet = int(input("Enter how much your bonus bet is, or 0 to exit: "))
    if not bonusBet:
        sys.exit()
    else:
        odds1 = float(betList[2])
        odds2 = float(betList[5])
        bet = ((bonusBet*odds1) - bonusBet)/odds2
        print("Place your bonus bet on {}, and put ${:.2f} on {}".format(
        betList[1], bet, betList[4]))
    return 0
#First we choose which agency has the bonus bet
agencies = ["CrownBet", "SportsBet", "Neds", "UBet"]
for agency in range(len(agencies)):
    print(str(agency+1) + ": " + agencies[agency])
bonusBetAgency = agencies[int(input("Which agency has the bonus bet? "))-1]

#Then cal findBet, which figures out the best bonus bets for us
betList = findBet(bonusBetAgency)
#then print it out nicely
printBets(betList)
calculateBet(betList[0])
