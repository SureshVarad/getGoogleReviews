# getGoogleReviews
#------------------
#This application README package is tuned for Linux, 
#Please use Git-Bash or similar tool on windows, to circumvent this.


### PRE-REQUISITES
#-----------------
#Make sure Python 2.7 or greater is installed along with Python Package installer pip.
#create a new virtual environment, if you wish so (Optional)
#Start using the virtual environment, so your installations won't affect global python
virtualenv env
source env/bin/activate
#Once finished, use 'deactivate' to exit from virtual environment

#If you do not have pip installed, but only python installed, follow below steps.
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py --prefix=/usr/local/

#Once pip is installed, run following to installed the required packages.
(env)$ pip install -r requirements.txt

#In Linux/Mac export the following
export GOOGLE_APPLICATION_CREDENTIALS="~/getGoogleReviews/<Google_Application_Credential>.json"
#In Windows set the environment variable instead
set GOOGLE_APPLICATION_CREDENTIALS="<CompletePath>\getGoogleReviews\<Google_Application_Credential>.json"

### RUN THE CODE
#---------------
#To Run the program use below command, before the root directory.
python -m getGoogleReviews.query
