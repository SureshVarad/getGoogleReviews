"""
Program to invoke Google Places API and return results and sort review based 
on review sentiments from Google's Cloud Natural Language API

@author: Suresh
"""
# Imports
from __future__ import absolute_import
import os
import sys
import warnings
import logging
import operator
#import pdb
from decimal import Decimal
from collections import defaultdict
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types as google_types
from googleplaces import GooglePlaces, GooglePlacesError, GooglePlacesAttributeError, types, lang
from operator import itemgetter

#__all__ = ['GooglePlaces', 'GooglePlacesError', 'GooglePlacesAttributeError', 'geocode_location']

geoLocation = "" 
log_dir = "./"
file_name = "googleReviews.log"

# [ START def_initialize_logger]
def initialize_logger(output_dir, file_name):
    	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)

	# create console handler and set level to info
	handler = logging.StreamHandler()
	handler.setLevel(logging.ERROR)
	formatter = logging.Formatter("%(levelname)s - %(message)s")
	handler.setFormatter(formatter)
	logger.addHandler(handler)

	# create debug file handler and set level to debug
	handler = logging.FileHandler(os.path.join(output_dir, file_name),"w")
	handler.setLevel(logging.DEBUG)
	# create a logging format
	formatter = logging.Formatter('%(asctime)s %(filename)s:%(lineno)d [%(levelname)s] -> %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)
# [END of def_initialize_logger]

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

# [START def_validateZipCode]
def validateZipCode(zipCode):
    return(len(zipCode) == 5 and zipCode.isdigit()) 
# [END def_validateZipCode]

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
		 #Validate Zip code format
    		 zipCode = zipCode.replace(" ", "")
		 if validateZipCode(zipCode) is True:
	            geoLocation = zipCode
		 else:
		    print "\n\nInvalid ZipCode Format, should be only 5 digits, retry"
		    validateInput(inputOption)
	logging.debug("\n\nGeoLocation from User Input : {} ".format(geoLocation))
# [END def_validateInput]


# [START Of def_sortAndPrint]]
def sortAndPrint(queryResults):
   logging.debug("UnSorted Results : {}".format(queryResults))
   queryResults.sort(key=itemgetter('score','overAllRatings'), reverse=True)
   logging.debug("Sorted Results : {}".format(queryResults))
   print_results(queryResults)
# [END def_sortAndPrint]]


# [START Of def_print_results]
def print_results(results):
    printCounter = 1
    for item in results:
	print "\n\n\nSorted :%d/%d, %s @ %s, Google Place ID: %s" % (printCounter, len(results), item['placeName'], item['address'], item['placeId'])
	print "Phone # : %s " % str(item['phoneNumber'])
	print "MapsURL : %s " % (item['mapsUrl'])
	print "Combined Sentiment Score : {0:.9f}".format((round(item['score'],9)))
	print "Ratings : %s " % (str(item['overAllRatings']))
	print "Positive Reviews -----> %s " % item['positiveReviews']
	#print "Negative Reviews : %s " % item['negativeReviews']
	#print('Detailed Results {}'.format(details))
	logging.debug('Detailed Printed Results {},{},{},{},{}'.format(item['placeId'], 
			item['address'],item['phoneNumber'],round(item['score'],9),item['overAllRatings']))
	printCounter += 1
	#After 4 results Take a break and let user review them before continuing to next set of results.
	if printCounter % 4 is 0:
	   try:
		input("\n\nPress Enter to continue...")
	   except SyntaxError:
    		pass
    #End of For Loop
    print "\n\n"
# [END of def_print_results]

# [START MAIN BLOCK]
if __name__ == '__main__':
	initialize_logger(log_dir, file_name)
	getInput()
	print("\n\nGeoLocation: {}".format(geoLocation))

	YOUR_API_KEY = ""

	google_places = GooglePlaces(YOUR_API_KEY)

	try:
	    #
	    #Get All 7 Eleven Stores of type "Gas Station" in the radius of 25miles. Google Returns only 20 top results in one page.
	    query_result = google_places.nearby_search( location=geoLocation, keyword='7 Eleven', 
							radius=25000, types=[types.TYPE_GAS_STATION])
	except Exception as err:
		logging.fatal(err, exc_info=False)
		logging.debug("Exception occured when fetching results from Google")
		print("Exception occured when fetching results based on input, Exiting..!!")
		sys.exit(1)
	#End of try & Except

	if query_result.has_attributions:
	    print query_result.html_attributions

	count = 0
	#Initialize Google Cloud Sentiment Analysis
	client = language.LanguageServiceClient()
	#Create a List to store query details below
	queryResults = []

	#pdb.set_trace()
	try:
		for place in query_result.places:
		    # The following method has to make a further API call, before getting reviews.
		    place.get_details()
		    id = place.place_id
		    address = place.details.get('formatted_address')
		    overAllRatings = place.rating
		    reviews = place.details.get('reviews')
		    #reviews = place.details.get('reviews').get('text')
		    reviewText = []  
		    #reviewRatings = []
		    positiveReviews = []
		    negativeReviews = []
		    combinedSentimentScore = 0.0
    		    logging.debug("%s @ %s, Google Place ID: %s" % (place.name, address, id))
		    #If there are no reviews, skip drilling down into details 
		    logging.debug("Id: {}, Address {}, URL {}".format(id,address,place.url))
		    if reviews is not None:
			try:
			   for i, _ in enumerate(reviews):
				#Reset score, just to make sure it's not carrying forward old data.
				score=0.0
				reviewTextBuffer = reviews[i]['text']
				#rate = reviews[i]['rating']
				reviewTextBuffer = reviewTextBuffer.encode('utf-8')
				reviewText.append(reviewTextBuffer)
				#reviewRatings.append(rate)
				
				#Get Google Sentiment Analysis for each review
				document = google_types.Document(content=reviewTextBuffer, type=enums.Document.Type.PLAIN_TEXT)
				annotations = client.analyze_sentiment(document=document)
				#Get the overall score for the review submitted.
				score = annotations.document_sentiment.score 
				#Get the magnitude for the review submitted.
				#magnitude = annotations.document_sentiment.magnitude 
				logging.debug("Google Place Review = {}".format(reviewTextBuffer))
				logging.debug("Google Sentiment Score = {}".format(score))

				# Google's sentiment score ranges between -1.0 to 1.0
				# If score is above 0.3 it's a positive review, we can display this to customers
				# We are going to skip over the mixed reviews for now.
				# but can easily add an else condition, to capture them if required.
				combinedSentimentScore += score
				if score > 0.3:
					positiveReviews.append(reviewTextBuffer)
				elif score < -0.3:
					negativeReviews.append(reviewTextBuffer)
				#End of For loop, for fetching reviews
			except Exception as err:
				# If it failed, Most cases its just mean NO Reviews are present for this store. Log it and continue
				# If Google Sentiments call failed, then it would assign default sentiment score of 0.0 for all stores, 
				# which would cause algorithm to use google ratings for sorting
				logging.fatal(err, exc_info=True)
				logging.debug("Exception inside fetching reviews & sentiment ID:{}, Maps URL: {}, Score {}".format(id, place.url, score) )
				pass
		    #End of -- If Loop for len(reviews) > 0 
		    details = {
			'placeId': id,
			'placeName': place.name,
			'overAllRatings': overAllRatings,
			'score': combinedSentimentScore,
			'address': address,
			'phoneNumber': place.local_phone_number,
			'mapsUrl': place.url,
			'positiveReviews': positiveReviews,
			'negativeReviews': negativeReviews
		    }
		    queryResults.append(details)
		    #print_results(place, details, id)
    		    logging.debug("\n\nAll Details fetched so far ===> %s\n\n\n" % (queryResults))
		    count =  count + 1
		    pass
		#End of For loop for all query results on first page
	except Exception as err:
		#print Exception, err
		logging.fatal(err, exc_info=True)
		logging.debug("Exception occured when fetching results from query")
		print("Exception occured when fetching results from query")
		pass
	print "Total Fetched Stores for this GeoLocation : %s " % count
	
	#Let's Sort based on combinedSentimentScore & overAllRatings
	sortAndPrint(queryResults)

#[ END OF MAIN BLOCK AND PROGRRAM]
