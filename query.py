"""
Program to invoke Google Places API and return results

@author: Suresh
"""
from __future__ import absolute_import

from decimal import Decimal
import warnings
import os

#from googleplaces import GooglePlaces, types, lang
from . import googleplaces, types, lang

__all__ = ['GooglePlaces', 'GooglePlacesError', 'GooglePlacesAttributeError', 'geocode_location']

if (os.name == "posix"):
    os.system("clear")
else:
    os.system("cls")

geoLocation = ""

def getInput():
	""" Gets City/State or Zip option from user"""

	print "\n\n\n\t\tWelcome to 7-Eleven\n\n\n"
	print "\n\tTo view the nearest stores, please provide one of following"
	print "\n1. City, State"
	print "\n2. Zip"
	inputOption = raw_input('\nYour Choice (1/2): ')
	validateInput(inputOption)

def validateInput(inputOption):
	""" Fetches & Validates the passed input and gets City/Zip details"""
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

getInput()
print "\n\nGeo Location: " + geoLocation


YOUR_API_KEY = 'AIzaSyAG2gC75WBWAtPsJ9dFtzum9yts0xlZ3Qo'

#google_places = GooglePlaces(YOUR_API_KEY)
google_places = googleplaces.GooglePlaces(YOUR_API_KEY)

query_result = google_places.nearby_search( location=geoLocation, keyword='7 Eleven', radius=20000, types=[types.TYPE_GAS_STATION])

if query_result.has_attributions:
    print query_result.html_attributions

count = 0
for place in query_result.places:
    # The following method has to make a further API call, before getting reviews.
    place.get_details()
    address = place.details.get('formatted_address')
    ratings = place.rating
    reviews = place.details.get('reviews')
    #reviews = place.details.get('reviews').get('text')
    reviewText = []  
    for i, _ in enumerate(reviews):
	stringBuffer = reviews[i]['text']
	stringBuffer = stringBuffer.encode('utf-8')
	reviewText.append(stringBuffer)

    #detail_res[id]['ratings'] = ratings

    print "%s @ %s, Google Place ID: %s" % (place.name, address, place.place_id)
    print "Ratings : %s " % str(ratings)
    print "Reviews : %s " % str(reviewText)
    print "Phone # : %s " % str(place.local_phone_number)
    print "Website : %s " % str(place.website)
    print "MapsURL : %s \n\n" % str(place.url)
    #print place.international_phone_number
    count =  count + 1
    pass
print "Total Count : %s " % count
