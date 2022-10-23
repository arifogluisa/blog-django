import requests
import json


def get_current_temperature():
	"""
	This function returns current temperature of the Baku city.
	API allows us to send request 25 times per a day.
	We will use this function to schedule a task,
	which get current temperature and save to database in every hour,
	and later we can use last temperature to show in navbar.
	"""
	url = "https://weatherbit-v1-mashape.p.rapidapi.com/current"
	querystring = {"lon": "49.86", "lat": "40.4"}
	headers = {
		"X-RapidAPI-Key": "a135d51756msh8def5004263b704p1476eajsn0c347e3f06b5",
		"X-RapidAPI-Host": "weatherbit-v1-mashape.p.rapidapi.com"
	}
	response = requests.request("GET", url, headers=headers, params=querystring)
	response_dict = json.loads(response.text)
	temp = response_dict['data'][0]['temp']
	if temp > 0:
		temp = f'+{temp}'
	return temp
