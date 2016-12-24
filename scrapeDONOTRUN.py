import requests
from bs4 import BeautifulSoup
import time
import re
import random
import sys

baseurl = "http://www.succeedsocially.com/"

startTime = time.clock()

pattern = re.compile("^[a-z]+$")

def ScrapePage(pagename, level, pagelisting):
    global baseurl
    global startTime
    global pattern

    if not pattern.match(pagename):
        print("##!! NOTICE: " + str(pagename) + " is not a valid article on this site, skipping...")
        return pagelisting
    
    time.sleep(random.uniform(1,10))
    print("Scraping " + str(pagename) + "... [level " + str(level) + "]")

    page = requests.get(baseurl + str(pagename))
    soup = BeautifulSoup(page.text, 'html.parser')

    # get the important stuff
    content = soup.find("div", id="content")

    # remove the nonimportant stuff
    try: content.find("div", id="searchbox").decompose()
    except: pass 
    try: content.find("div", id="medfooterspaces").decompose()
    except: pass 
    try: content.find("div", id="largefooterspaces").decompose()
    except: pass 
    try: content.find_all("script").decompose()
    except: pass
    try: content.find_all("iframe").decompose()
    except: pass
    
    print(" - Saving " + str(pagename) + " content... [level " + str(level) + "]")

    saveit = open("SucceedSocially/" + pagename + ".html", 'wb')
    saveit.write(content.prettify().encode(sys.stdout.encoding, errors='replace'))
    saveit.close()

    pagelisting.append(pagename)

    # get all the links
    print(" - Following " + str(pagename) + "'s links... [level " + str(level) + "]")
    for link in content.find_all("a"):
        
        try:
            newpagename = link["href"]
            if (newpagename in pagelisting): # don't get caught in an endless loop if we already have a page and the site wasn't structured well!
                print("##!! NOTICE: article " + str(pagename) + " was already scraped, skipping...")
                continue 
            pagelisting = ScrapePage(newpagename, level + 1, pagelisting)
        except:
            print("##!! ERROR: something went wrong with a link in " + str(pagename) + " - " + str(link))
            errorfile = open("errors.dat", 'a')
            errorfile.write("something happened with a link in " + str(pagename) + " - " + str(link))
            errorfile.close()

    timeSoFar = time.clock() - startTime
    print("Completed " + str(pagename) + "! [level " + str(level) + "] .. time - " + str(timeSoFar))
    return pagelisting

print("Beginning scrape...\n")

pages = []
mainpageurl = "articlecategories"      
pages = ScrapePage(mainpageurl, 0, pages)
totalTime = time.clock() - startTime

print("Scrape successfully completed in " + str(totalTime))

print("Saving page list...")

finalpages = open("pages.dat", 'w')
for thing in pages:
    finalpages.write(thing + "\n")
finalpages.close()

print("Save complete!")
