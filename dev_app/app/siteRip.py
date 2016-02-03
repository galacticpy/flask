import os
import urllib2

def scrape(url):
    pdp = urllib2.urlopen(url).read()
    variation = {
        "pr_page_id='":"'",
        'pr_page_id="':'"',
        'pr_page_id=':'"',
        "pr_page_id : '":"'",
        'pr_page_id : "':'"',
        'pr_page_id: "':'"',
        "pr_page_id: '":"'",
        'pr_page_id : ':'"',
        "pr_page_id : ":"'"
        }

    for var in variation:               
        pageid = pdp.split(var, 1)[-1].split(variation[var])[0]
        if len(pageid) < 12:
            return pageid
    
               
def full(url):
    pdp = urllib2.urlopen(url).read()
    fulljs = pdp.split('src="', 1)[-1].split('"')[0]
    match = False
    while match == False:
        if 'full.js' not in fulljs:
            nofull = fulljs
            fulljs = pdp.split(nofull, 1)[-1]
            fulljs = fulljs.split('src="', 1)[-1].split('"')[0]
        else:
            match = True
    if len(fulljs) < 100:
        return fulljs

