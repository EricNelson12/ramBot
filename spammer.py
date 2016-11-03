###############################################################################
#
#                          2015 (C) Kushara Singh
#                         kushagra14056@iiitd.ac.in
#
#                           Licensed under WTFPL#               
#                          http://www.wtfpl.net/
#
#              Author is nor liable for misuse; Use carefully!
#
###############################################################################
#
#	A dumb script to spam a google form.
#
#	What it can spam?	(1)
#
#		- Single page forms
#		- The following controls :
#			- text
#			- textarea
#			- select
#			- radio
#			- checkbox
#
#	What it cannot spam?
#
#		- Multi page forms
#		- Forms that require login (duh!)
#		- A google form which has stuff not mentioned in (1)
#
###############################################################################

import random
import string
import sys
import mechanize
from lxml import html
import requests

REVIEWCOUNTER = 0


def new_browser():

	""" Returns a new mechanize browser instance """

	browser = mechanize.Browser()
	browser.set_handle_robots(False)
	browser.set_handle_refresh(False)

	return browser

def fill_form(form):

	global REVIEWCOUNTER			
			
	form.controls[0].value = 'Ramon Lawrence'
	form.controls[1].value = 'Sciences'
	form.controls[2].value = reviewList[REVIEWCOUNTER]
	
	REVIEWCOUNTER = REVIEWCOUNTER +1		

		
#Spams the form with Ramon reviews
def spam_form(times = 1): 

	browser = new_browser()			
	total = times
	
	while times:
		""" Open form """
		
												#URL OF THE GOOGLE FORM!!!!!!!!!!!!!!! (Change if testing)
		browser.open('https://docs.google.com/forms/d/e/1FAIpQLSdQbEUg5-C9TskmUPMRimoj__OLkY7pP7bR60fe1XMGeJ5efA/viewform')
		browser.form = list(browser.forms())[0]

		""" Mess it up and submit"""
		fill_form(browser.form)
		browser.submit()
		times -= 1

		print "%d. Filled form" % (total - times)

# Returns a list of all reviews from rate my professor page. Replaces the first and last names with Ramon and Lawrence. :)
def getReviews(myProfURL):

	returnList = []

	page = requests.get(myProfURL)
	tree = html.fromstring(page.content)

	# Get First and Last name of stolen reviews
	firstName = tree.xpath('//span[@class="pfname"]/text()')[0].strip() 
	lastName = tree.xpath('//span[@class="plname"]/text()')[0].strip()
	reviews = tree.xpath('//p[@class="commentsParagraph"]/text()')	

	for r in reviews:
		txt = r.strip() #remove /r/l and trailing blank spaces		
		txt = txt.replace(firstName,"Ramon")
		txt = txt.replace(lastName,"Lawrence")
		txt = txt.replace(firstName.upper(),"Ramon")
		txt = txt.replace(lastName.lower(),"Lawrence")
		txt = txt.replace("she","he")
		txt = txt.replace("She","He")
		returnList.append(txt)
	
	return returnList

#Return number of rate my prof reviews (one per line)
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
		
if __name__ == "__main__":

	if len(sys.argv) < 1:
		print "run script as\n'python %s 'url' (in quotes) '\n" %(__file__)
		exit()

	#Rate my prof URL	
	url = sys.argv[1]
	
	#Gets list of reviews to spam form with
	reviewList = getReviews(url)	
	#Number of reviews that we have
	times = len(reviewList)
	#Submits votes for Ramon
	spam_form(times)

