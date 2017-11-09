from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver


def importCrownBetPage():
    browser = webdriver.Chrome()
    url = "https://crownbet.com.au/sports-betting/basketball/nba/"
    browser.get(url)
    innerHTML = browser.execute_script("return document.body.innerHTML")
    return innerHTML

def createCrownBetNBAMatchups():
    # pageHTML = importCrownBetPage()
    # output = open("output.html", 'w')
    # output.write(pageHTML)

    # soup = BeautifulSoup(pageHTML, 'lxml')
    output = open('output.html', 'r')
    soup = BeautifulSoup(output.read(), 'lxml')
#Crownbet organises their page in tables, so we find all the divs containing the table
    # teamTable = soup.findAll('div', {'class': 'event-summary-table sport-block sport-event hidden-xs'})
    teamTable = soup.findAll('table')

    for team in teamTable:
        betType = soup.findAll('tr')
        # print(betType)
        print(team)
        print("\n\n\n\n\n\n\n")

createCrownBetNBAMatchups()
