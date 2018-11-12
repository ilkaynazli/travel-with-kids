Summary
Road Trips with Kids is an app that helps parents to plan their journey by showing kid-friendly places along the route they have selected.  After selecting their route, parents can select several food and play options to display them on the map. Furthermore, parents can examine each business page and look at pictures to decide if they like the place. They can later add this place as a stopover for that specific route. In the user page, parents can see their last saved route, now with stopovers.

About the Developer
Road Trips with Kids was created by Ilkay Gulsoy, a software engineer in San Francisco Bay Area, CA. Learn more about the developer on www.linkedin.com/in/ilkay-celik-gulsoy.

Technologies used:

Python
Flask
Javascript
React
JQuery
AJAX
JSON
PostgreSQL
SQLAlchemy
cachetools-ttl
Jinja2
HTML
CSS
Bootstrap
Python unittest module
Google Maps API
Google Places API
Yelp API


Road Trips with Kids is an app built on a Flask server with a PostgreSQL database, with SQLAlchemy as the ORM. 
The Javascript uses JQuery and AJAX to interact with the backend. The Login and Sign Up buttons and routes use React to connect to the Flask backend.
The front end templating uses Jinja2. Bootstrap and CSS were used to make the site user friendly.
The map is built using the Google Maps API, which sends coordinates to Yelp API and then displays the results of Yelp API requests. Detailed information on businesses were collected from both Yelp API and Google Places API.
The Yelp API requests were cached for 24 hours via cachetools-ttl API.
Server routes are tested using the Python unittest module.

Setup/Installation

Requirements:
PostgreSQL
Python 3.6
Google Maps and Yelp API keys

Please follow the below steps to run this app on your local device:

Clone repository:
    $ git clone https://github.com/ilkaynazli/travel-with-kids.git

Get your own secret keys for Google Maps and Yelp and create a secret key that will be used as a session key. Save them to a file secret.sh. Your file should look something like this:
    export GOOGLE_MAPS_API='xyz'
    export YELP_API='xyz'
    export SECRET='xyz'    

Create a virtual environment:
    $ virtualenv env

Activate the virtual environment:
    $ source env/bin/activate

Source your keys from secret.sh to your environment
    $ source secret.sh

Install dependencies:
    $ pip install -r requirements.txt

Create database 'travels'.
    $ createdb travels

Create your database tables and seed questions data.
    $ python model.py
    $ python seed.py

Run the app from the command line.
    $ python server.py

You can now navigate to 'localhost:5000/' to access Road Trips with Kids

