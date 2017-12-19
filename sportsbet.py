from bs4 import BeautifulSoup
import requests
import re



def createSportsBetNBAMatchups():
    #Open up the page and parse it using beautifulsoup
    r = requests.get("https://www.sportsbet.com.au/betting/basketball-us?QuickLinks")
    data = r.text
    soup = BeautifulSoup(data, "html5lib")
    completedMatchup = True
    matchups = []
    currMatchup = ()

    #Find all divs that match the regex ending in Match
    #Doesn't work if there is currently a live game.
    teamDivs = soup.findAll('div', {'title': re.compile(r'(.*)Match')})
    for team in teamDivs:

        #Since the info we need is inside spans, get all the spans
        teams = team.findAll('span')
        print(teams)
        #And then add the team name + their odds into the matchup array
        teamName = teams[0].text
        teamOdds = float(teams[1].text.replace('\n', ''))
        nameAndOdds = (teamName, teamOdds)
        #If it's the first team, we add the team into the currMatchup tuple
        if(completedMatchup):
            nameAndOdds1 = nameAndOdds
            #and then change compeletedMatchup to false so the other one runs next
            completedMatchup = False
        else:
            #If the matchup is completed, add the team into the
            #currMatchup tuple, and then add that tuple into the matchups tuple.
            #then reset.
            currMatchup = (nameAndOdds1, nameAndOdds)
            matchups.append(currMatchup)
            currMatchup = ()
            completedMatchup = True



    return matchups

print(createSportsBetNBAMatchups())
