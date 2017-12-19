from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver


def importCrownBetPage():
    #Opens the page and returns the html inside
    browser = webdriver.Chrome()
    url = "https://crownbet.com.au/sports-betting/basketball/nba/"
    browser.get(url)
    innerHTML = browser.execute_script("return document.body.innerHTML")
    return innerHTML

def createCrownBetNBAMatchups():
    matchups = []
    currMatchup = ()
    pageHTML = importCrownBetPage()
    soup = BeautifulSoup(pageHTML, 'html5lib')
#Crownbet organises their page in divs, so we find each div with the info we need
    matchupList = soup.findAll('div', {"class" : "event-summary-table container-fluid visible-xs"})
    for matchup in matchupList:
        #the info is contained in div "rows" so we retrieve them,
        matchupRows = matchup.findAll('div', {"class":"row"})
        #find the rows we need - the odds are in the 2nd and 5th rows,
        #and the name of the team is in the row before them.

        #for each team, get the name and odds and throw it into a tuple
        teamName1 = matchupRows[0]
        teamName1 = teamName1.find("span", {"class":"outcome-anchor-text"}).text
        teamOdds1 = matchupRows[1]
        teamOdds1 = teamOdds1.find("span", {"class":"bet-amount"}).text.strip()

        nameAndOdds1 = (teamName1, teamOdds1)

        teamName2 = matchupRows[3]
        teamName2 = teamName2.find("span", {"class":"outcome-anchor-text"}).text
        teamOdds2 = matchupRows[4]
        teamOdds2 = teamOdds2.find("span", {"class":"bet-amount"}).text.strip()
        nameAndOdds2 = (teamName2, teamOdds2)

        #then, create the currMatchup tuple and append it to the matchups list
        currMatchup = (nameAndOdds1, nameAndOdds2)
        matchups.append(currMatchup)



    print(matchups)

createCrownBetNBAMatchups()
