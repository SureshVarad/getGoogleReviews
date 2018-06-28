"""
Program to invoke Google Places API and return results

@author: Suresh
"""
# Imports
from __future__ import absolute_import
import os
import sys
import warnings
import logging
#import pdb
from decimal import Decimal
from collections import defaultdict
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types as google_types
from googleplaces import GooglePlaces, types, lang

__all__ = ['GooglePlaces', 'GooglePlacesError', 'GooglePlacesAttributeError', 'geocode_location']

#Set the Logs for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# create a file handler
fileHandler = logging.FileHandler('googleReviews.log')
fileHandler.setLevel(logging.INFO)
# create a logging format
formatter = logging.Formatter('%(asctime)s %(filename)s:%(lineno)d [%(levelname)s] -> %(message)s')
fileHandler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fileHandler)

geoLocation = "" 

# [START def_getInput]
def getInput():
	'''Gets City/State or Zip option from user'''

	#clear the screen
	if (os.name == "posix"): #Mac/Linux
	    os.system("clear")
	else:
	    os.system("cls")

	print "\n\n\n\t\tWelcome to 7-Eleven\n\n\n"
	print "\n\tTo view the nearest stores, please provide one of following"
	print "\n1. City, State"
	print "\n2. Zip"
	inputOption = raw_input('\nYour Choice (1 or 2): ')
	validateInput(inputOption)
# [END def_getInput]

# [START def_validateInput]
def validateInput(inputOption):
	'''Fetches & Validates the passed input and gets City/Zip details'''
	global geoLocation
  	cityState = ""
	zipCode = ""
	if (inputOption.isdigit() == False or ( int(inputOption) != 1 and int(inputOption) !=2) ):
	    inputOption = raw_input("Plese input only options 1 or 2 : ")
	    validateInput(inputOption)
	else:
	    if int(inputOption) == 1:
		 cityState = raw_input("Please enter City, State (eg: Dallas,Tx) : ")
		 #TODO: Validate City/zip details format
	         geoLocation = cityState
	    else:
		 zipCode = raw_input("Please enter Zip Code (5-Digits): ")
		 #TODO: Validate Zip code format
	         geoLocation = zipCode
	print "\n\nGeoLocation from User Input : " + geoLocation
# [END def_validateInput]

# [START Of def_print_results]
def print_results(place, detail_res, id):
    print "%s @ %s, Google Place ID: %s" % (place.name, address, id)
    print "Ratings : %s <--> %s \n" % (str(ratings), str(reviewRatings))
    print "Positive Reviews : %s \n" % str(positiveReviews)
    print "Negative Reviews : %s \n" % str(negativeReviews)
    #print "Phone # : %s " % str(place.local_phone_number)
    #print "Website : %s " % str(place.website)
    #print "MapsURL : %s \n\n" % str(place.url)
    #print('Detailed Results {}'.format(detail_res[id]))
    logger.info('Detailed Results {}'.format(detail_res[id]))
# [END of def_print_results]

# [START MAIN BLOCK]
if __name__ == '__main__':
	getInput()
	print "\n\nGeo Location: " + geoLocation


	YOUR_API_KEY = ""

	google_places = GooglePlaces(YOUR_API_KEY)

	#Get All 7 Eleven Stores of type "Gas Station" in the radius of 25miles. Google Returns only 20 top results in one page.
	query_result = google_places.nearby_search( location=geoLocation, keyword='7 Eleven', radius=25000, types=[types.TYPE_GAS_STATION])

	if query_result.has_attributions:
	    print query_result.html_attributions

	detail_res = defaultdict(dict)
	count = 0
	#Initialize Google Cloud Sentiment Analysis
	client = language.LanguageServiceClient()

	#pdb.set_trace()
	try:
		for place in query_result.places:
		    # The following method has to make a further API call, before getting reviews.
		    place.get_details()
		    id = place.place_id
		    address = place.details.get('formatted_address')
		    ratings = place.rating
		    reviews = place.details.get('reviews')
		    #reviews = place.details.get('reviews').get('text')
		    reviewText = []  
		    reviewRatings = []
		    positiveReviews = []
		    negativeReviews = []
		    try:
		    	for i, _ in enumerate(reviews):
			   reviewTextBuffer = reviews[i]['text']
			   rate = reviews[i]['rating']
			   reviewTextBuffer = reviewTextBuffer.encode('utf-8')
			   reviewText.append(reviewTextBuffer)
			   reviewRatings.append(rate)
			
			   #Get Google Sentiment Analysis for each review
			   document = google_types.Document(content=reviewTextBuffer, type=enums.Document.Type.PLAIN_TEXT)
			   annotations = client.analyze_sentiment(document=document)
			   score = annotations.document_sentiment.score
			   #magnitude = annotations.document_sentiment.magnitude
			   logger.info("Google Sentiment Score = {}".format(score))

			   # If score is above 0.3 it's a positive review, we can display this to customers
			   # We are going to skip over the mixed reviews for now.
			   # but can easily add an else condition, to capture them if required.
			   if score > 0.3:
				positiveReviews.append(reviewTextBuffer)	
			   elif score < -0.3:
				negativeReviews.append(reviewTextBuffer)	
			#End of For loop, for fetching reviews
		    except:
			#eprint("Exception inside fetching reviews & sentiment, ", id, place.url, score, sep="---") 
			print("Exception inside fetching reviews & sentiment ID:{}, Maps URL: {}, Score {}".format(id, place.url, score) )
			pass
		    detail_res[id]['overallRatings'] = ratings
		    detail_res[id]['reviewRatings'] = reviewRatings
		    detail_res[id]['AllReviewText'] = reviewText
		    detail_res[id]['positiveReviews'] = positiveReviews
		    detail_res[id]['negativeReviews'] = negativeReviews
		    print_results(place, detail_res, id)
		    count =  count + 1
		    pass
		#End of For loop for all query results on first page
	except:
		#eprint("Exception inside main for loop to fetch results from query", sep="---") 
		print("Exception inside main for loop to fetch results from query")
		pass
	print "Total Count : %s " % count

#[ END OF MAIN BLOCK AND PROGRRAM]
