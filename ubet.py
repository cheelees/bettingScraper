from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver


def importUBetNBAPage():
    #Opens the page and returns the html inside
    browser = webdriver.Chrome()
    url = "https://ubet.com/sports/basketball/nba/nba-matches"
    browser.get(url)
    # innerHTML = browser.execute_script("return document.body.innerHTML")

    innerHTML = browser.page_source
    return innerHTML

def createUBetNBAMatchup():
    matchups = []
    currMatchup = ()
    pageHTML = importUBetNBAPage()
    #
    # ###################################
    # # print(pageHTML)
    output = open('ubetoutput.html', 'w', encoding='utf-8')
    output.write(pageHTML)
    # pageHTML = open('ubetoutput.html', 'r')
    ###################################
    soup = BeautifulSoup(pageHTML, 'lxml')
    #This gets the divs for each matchup
    teamDivs = soup.findAll('div', {"ng-multi-transclude":"content"})
    output = open('ubetoutput2.html', 'w', encoding='utf-8')
    output.write(str(teamDivs))
    for row in teamDivs:

        #Then we find the "Head to head" section,
        headToHead = row.find('div', {"class":"ubet-sub-events-summary"})
        #And then we find the name and odds for each team, which are contained in divs
        nameAndOddDivs = headToHead.findAll("div", {"class":"ubet-offer-win-only"})


        #Then we retrieve the name and the odds, which are contained in spans of each divs

        #matchupInfo is a list of lists, with each inner list containing name and Odds
        matchupInfo = []
        for team in nameAndOddDivs:
            spans = team.findAll("span")
            spans = [span.text for span in spans]
            matchupInfo.append(spans)
        # print(matchupInfo)
        teamName1 = matchupInfo[0][0]
        teamOdds1 = matchupInfo[0][1]
        teamName2 = matchupInfo[1][0]
        teamOdds2 = matchupInfo[1][1]

        nameAndOdds1 = (teamName1, teamOdds1)
        nameAndOdds2 = (teamName2, teamOdds2)
        currMatchup = (nameAndOdds1, nameAndOdds2)
        sortedMatchup = sorted(currMatchup, key=lambda odds: odds[1], reverse=True)
        matchups.append(sortedMatchup)

    return matchups
