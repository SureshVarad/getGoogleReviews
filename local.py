#!/usr/local/bin/python
#===============
def validateResponse(url, response):
    """Validates that the response from Google was successful."""
    if response['status'] not in [GooglePlaces.RESPONSE_STATUS_OK,
                                  GooglePlaces.RESPONSE_STATUS_ZERO_RESULTS]:
        errorDetail = ('Request to URL %s failed with response code: %s' %
                        (url, response['status']))
        raise GooglePlacesError(errorDetail)


def fetchRemote(serviceUrl, params=None, useHttpPost=False):
    if not params:
        params = {}

    encodedData = {}
    for k, v in params.items():
        if isinstance(v, six.string_types):
            v = v.encode('utf-8')
        encodedData[k] = v
    encodedData = urllib.parse.urlencode(encodedData)

    if not useHttpPost:
        queryUrl = (serviceUrl if serviceUrl.endswith('?') else
                     '%s?' % serviceUrl)
        requestUrl = queryUrl + encodedData
        request = urllib.request.Request(requestUrl)
    else:
        requestUrl = serviceUrl
        request = urllib.request.Request(serviceUrl, data=encodedData)
    return (requestUrl, urllib.request.urlopen(request))


def fetchPlacesJson(serviceUrl, params=None, useHttpPost=False):
    """Retrieves a JSON object from a URL."""
    if not params:
        params = {}

    requestUrl, response = fetchRemote(serviceUrl, params, useHttpPost)
    if six.PY3:
        strResponse = response.read().decode('utf-8')
        return (requestUrl, json.loads(strResponse, parseFloat=Decimal))
    return (requestUrl, json.load(response, parseFloat=Decimal))

def geoCodeLocation(location, sensor=False, apiKey=None):
    """Converts a location to lat-lng.
    Returns a dict with lat and lng keys.
    keyword arguments:
    location -- A human-readable location, e.g 'Dallas, Tx'
    sensor   -- Boolean flag: if the location came from a device true, else false
    apiKey  -- A valid Google Places API key. 
    raises:
    GooglePlacesError -- if the geocoder fails to find a location.
    """
    params = {'address': location, 'sensor': str(sensor).lower()}
    if apiKey is not None:
        params['key'] = apiKey
    url, geoResponse = fetchPlacesJson(
            GooglePlaces.GEOCODE_API_URL, params)
    validateResponse(url, geoResponse)
    if geoResponse['status'] == GooglePlaces.RESPONSE_STATUS_ZERO_RESULTS:
        error_detail = ('Location \'%s\' can\'t be determined.' % location)
        raise GooglePlacesError(error_detail)
    return geoResponse['results'][0]['geometry']['location']

def getPlaceDetails(place_id, apiKey, sensor=False, language=langEnglish):
    """Gets a detailed place response.
    keyword arguments:
    place_id -- The unique identifier for the required place.
    sesnor -- Boolean flag: if the location came from a device true, else false
    language -- Defaults to English
    """
    url, detailResponse = fetchPlacesJson(GooglePlaces.DETAIL_API_URL,
                                              {'placeid': place_id,
                                               'sensor': str(sensor).lower(),
                                               'key': apiKey,
                                               'language': language})
    validateResponse(url, detail_response)
    return detailResponse['result']
#===============

