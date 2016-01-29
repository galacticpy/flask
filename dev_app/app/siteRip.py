import os
import urllib2
url = 'http://localhost:5000/super-wedge.html'
pdp = urllib2.urlopen(url).read()

def scrape(pdp):
    variation = {
        'pr_page_id=':'"',
        "pr_page_id : '":"'",
        'pr_page_id : "':'"',
        'pr_page_id: "':'"',
        "pr_page_id: '":"'",
        'pr_page_id : ':'"',
        "pr_page_id : ":"'"
        }
    
    def getid():
        for var in variation:               
            pageid = pdp.split(var, 1)[-1].split(variation[var])[0]
            if len(pageid) < 12:
                print pageid
                return pageid
    getid()
               

def full(pdp):
    fulljs = pdp.split('src="', 1)[-1].split('"')[0]
    match = False
    while match == False:
        if 'full.js' not in fulljs:
            nofull = fulljs
            fulljs = pdp.split(nofull, 1)[-1]
            fulljs = fulljs.split('src="', 1)[-1].split('"')[0]
            print nofull
        else:
            match = True
    if len(fulljs) < 100:
        print fulljs
        return fulljs
      
scrape(pdp)
full(pdp)