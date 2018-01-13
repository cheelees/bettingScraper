from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver

def importNedsNBAPage():
    #Opens the page and returns the html inside
    browser = webdriver.Chrome()
    url = "https://neds.com.au/sports/basketball/8476024b-5c61-4769-bc50-7c0a5abc97a2/3c34d075-dc14-436d-bfc4-9272a49c2b39"
    browser.get(url)
    # innerHTML = browser.execute_script("return document.body.innerHTML")

    innerHTML = browser.page_source

    return innerHTML

def createNedsNBAMatchup():
    matchups = []
    currMatchup = ()
    # pageHTML = importNedsNBAPage()
    # # ###################################
    #
    # output = open('nedsoutput.html','w')
    # output.write(pageHTML)
    pageHTML = open('nedsoutput-kenny.html', 'r')
    # ###################################
    soup = BeautifulSoup(pageHTML, 'lxml')
    groupsByTime = soup.findAll('div', {"class":"event-group-by-time"})
    teamDivs = soup.findAll('div', {"class":"price-row"})

    for group in groupsByTime:
        teamDivs = group.findAll('div', {"class":"live-event-detail-entrants"})
        for row in teamDivs:
            #both the team names are in classes called "entrant-name-cell"
            names = row.findAll('span', {'class':"entrant-name"})
            #and the odds are in divs called 'entrant-odds'
            odds = row.findAll('button', {'class':'odds entrant-odds'})
            teamName1 = names[0].text.strip()
            oddsSpan1 = odds[0].find('span')
            teamOdds1 = oddsSpan1.text.strip()
            teamName2 = names[1].text.strip()
            oddsSpan2 = odds[1].find('span')
            teamOdds2 = oddsSpan2.text.strip()

            nameAndOdds1 = (teamName1, teamOdds1)
            nameAndOdds2 = (teamName2, teamOdds2)
            currMatchup = (nameAndOdds1, nameAndOdds2)
            sortedMatchup = sorted(currMatchup, key=lambda odds: odds[1], reverse=True)
            matchups.append(sortedMatchup)
    print(matchups)
    return matchups

createNedsNBAMatchup()
