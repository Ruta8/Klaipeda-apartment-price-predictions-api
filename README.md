# Klaipėda apartment price predictor API connected to Heroku Database
This project is an API created using Flask. The API allows to send POST requests to it with some apartment features and uses an ML model to predict prices for apartments in Klaipeda. The model was trained on data collected with Klaiped-apartment-scraper-package, which you may also find between my public git repositories. The API also allows GET requests that show the last ten price predictions and the features and values used for those predictions. Last ten price predictions are stored in 

## Project Structure
This project has four major parts :
1. `model` folder contains code for training the ML model as well as separate pickle files for encoding and scaling input data.
2. `preprocessing` folder contains `cleaning.py` used to clean scraped data, and `preprocessing.py` which scales and encodes cleaned data before feeding it to the model.
3. `database` folder contains `database.py` contains code used to create and populate Heroku database with apartment predictions.

## Running the project
The project is hosted by Heroku and the model and history can be accessed via requests.
1. You can send POST requests to [/predict](https://peaceful-journey-07197.herokuapp.com/predict) FLask API using Python's inbuilt request module or Postman platform. <br>
Below is an example of how to run a command to send the request with some pre-popuated values. <br>
Python code:
```
import requests
import json

BASE = 'https://peaceful-journey-07197.herokuapp.com/predict'

data = [{
		"Room Count": 2,
		"Square Meters": 66,
		"Apartment Floor": 5,
		"Area": "Poilsio",
		"Total Floors": 5,
		"Building Age": 34
	}]

response = requests.post(BASE,  data=json.dumps({"inputs": data}))
print(json.loads(response.text))
```
Result:
```
>> {"Predicted house prices": [62450.53862953569]}
```
2. You can also send GET requests to [/history](https://peaceful-journey-07197.herokuapp.com/history) FLask API using Python's inbuilt request module or Postman platform. <br>
