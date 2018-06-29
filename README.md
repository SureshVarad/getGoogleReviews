# getGoogleReviews
#This application README package is tuned for Linux, 
#Please use Git-Bash or similar tool on windows, to circumvent this.


### PRE-REQUISITES
#Make sure Python 2.7 is installed along with Python Package installer pip.
#create a new virtual environment, if you wish so (Optional)
#Start using the virtual environment, so your installations won't affect global python
#CAUTION: This code may not work with Python 3+, so please use python 2.7+ only
```
virtualenv env
source env/bin/activate
```
#Once finished, use 'deactivate' to exit from virtual environment

#If you do not have pip installed, but only python installed, follow below steps.
```
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py --prefix=/usr/local/
```

#Once pip is installed, run following to installed the required packages.
```
(env)$ pip install -r requirements.txt
```
### Export GOOGLE_APPLICATION_CREDENTIALS
#In Linux/Mac export the following
```
export GOOGLE_APPLICATION_CREDENTIALS="<CompletePath>/getGoogleReviews/<Google_Application_Credential>.json"
```
#In Windows set the environment variable instead
```
set GOOGLE_APPLICATION_CREDENTIALS="<CompletePath>\getGoogleReviews\<Google_Application_Credential>.json"
```

### Update the YOUR_API_KEY
#create the Google API key and provide it permissions to use GeoCoding, Places & Cloud Natural Language API's.
#In Linux/GitBash run the following command to do that automatically.
```
sed -i 's/YOUR_API_KEY = ""/YOUR_API_KEY = "<your_actual_api_key_here>"/g' query.py
```

### RUN THE CODE
#To Run the program use below command, before the root directory.
```
python -m getGoogleReviews.query
```

### Unit Tests
#Due to time constraints, was just able to add 2 unit tests more to come, when time permits, TO execute them follow below steps
```
cd getGoogleReviews
python -m unittest query_test
```
