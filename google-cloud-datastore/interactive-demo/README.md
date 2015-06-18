This is a sample to demonstrate Google Cloud Datastore with the python gcloud library.

Usage Video: https://youtu.be/bMC_k0NBjKs?t=1508

#Prerequisites:

	1) Java 7 Runtime (or later version) http://java.com/
	2) gcd tool https://cloud.google.com/datastore/docs/downloads#tools
	3) Python 2.7
	4) pip
	5) Account on Google Cloud Platform https://cloud.google.com/

	
#Steps:

	1) Log in to Google Cloud Platform https://console.developers.google.com/
	2) Create a project
	3) Enable Google Cloud Datastore API
	4) Create a new client key (Credentials > Create new Client ID > Service Account)
	5) Never share your private key!
	6) Rename the JSON key you downloaded to key.json and move it to the project directory
	7) Replace YOUR_RPOEJCT_ID_HERE in code.py to your Google Cloud Project ID
	8) Replace YOUR_RPOEJCT_ID_HERE in appengine-web.xml to your Google Cloud Project ID
	9) Run the gcd tool to create the indexes (this will take some time, you can check progress in the developers console)
		Linux/OSX/Unix:	path/to/gcd.sh updateindexes --auth_mode=oauth2 .
		Windows: 		path/to/gcd.cmd updateindexes --auth_mode=oauth2 .
	10) Install python libraies: pip install -r requirements.txt
	11) Run:
		python demo.py 
		to start the program!
	
Notes:
This is not an official Google product.