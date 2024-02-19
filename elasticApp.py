from flask import Flask, render_template, request, session, jsonify
import shodan
import re
import requests as r
from os import system
from timeit import default_timer as timer
import sqlite3
from dotenv import load_dotenv
from os import getenv
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# Load .env variables
load_dotenv()

# Shodan API key (replace 'YOUR_SHODAN_API_KEY' with your actual API key)
SHODAN_API_KEY = getenv('SHODAN_API_KEY')
api = shodan.Shodan(SHODAN_API_KEY)
app.secret_key = 'b332ac5ec3f95e6913e3a76eb5d38891'
#json_results = 'json_results'

# IPv4 pattern recognition
ipv4_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]+\b')


@app.route('/', methods=['GET', 'POST'])
def index():
	countries = [{"name": "Afghanistan","code": "AF"},{"name": "Åland Islands","code": "AX"},{"name": "Albania","code": "AL"},{"name": "Algeria","code": "DZ"},{"name": "American Samoa","code": "AS"},{"name": "AndorrA","code": "AD"},{"name": "Angola","code": "AO"},{"name": "Anguilla","code": "AI"},{"name": "Antarctica","code": "AQ"},{"name": "Antigua and Barbuda","code": "AG"},{"name": "Argentina","code": "AR"},{"name": "Armenia","code": "AM"},{"name": "Aruba","code": "AW"},{"name": "Australia","code": "AU"},{"name": "Austria","code": "AT"},{"name": "Azerbaijan","code": "AZ"},{"name": "Bahamas","code": "BS"},{"name": "Bahrain","code": "BH"},{"name": "Bangladesh","code": "BD"},{"name": "Barbados","code": "BB"},{"name": "Belarus","code": "BY"},{"name": "Belgium","code": "BE"},{"name": "Belize","code": "BZ"},{"name": "Benin","code": "BJ"},{"name": "Bermuda","code": "BM"},{"name": "Bhutan","code": "BT"},{"name": "Bolivia","code": "BO"},{"name": "Bosnia and Herzegovina","code": "BA"},{"name": "Botswana","code": "BW"},{"name": "Bouvet Island","code": "BV"},{"name": "Brazil","code": "BR"},{"name": "British Indian Ocean Territory","code": "IO"},{"name": "Brunei Darussalam","code": "BN"},{"name": "Bulgaria","code": "BG"},{"name": "Burkina Faso","code": "BF"},{"name": "Burundi","code": "BI"},{"name": "Cambodia","code": "KH"},{"name": "Cameroon","code": "CM"},{"name": "Canada","code": "CA"},{"name": "Cape Verde","code": "CV"},{"name": "Cayman Islands","code": "KY"},{"name": "Central African Republic","code": "CF"},{"name": "Chad","code": "TD"},{"name": "Chile","code": "CL"},{"name": "China","code": "CN"},{"name": "Christmas Island","code": "CX"},{"name": "Cocos (Keeling) Islands","code": "CC"},{"name": "Colombia","code": "CO"},{"name": "Comoros","code": "KM"},{"name": "Congo","code": "CG"},{"name": "Congo, The Democratic Republic of the","code": "CD"},{"name": "Cook Islands","code": "CK"},{"name": "Costa Rica","code": "CR"},{"name": "Cote D\"Ivoire","code": "CI"},{"name": "Croatia","code": "HR"},{"name": "Cuba","code": "CU"},{"name": "Cyprus","code": "CY"},{"name": "Czech Republic","code": "CZ"},{"name": "Denmark","code": "DK"},{"name": "Djibouti","code": "DJ"},{"name": "Dominica","code": "DM"},{"name": "Dominican Republic","code": "DO"},{"name": "Ecuador","code": "EC"},{"name": "Egypt","code": "EG"},{"name": "El Salvador","code": "SV"},{"name": "Equatorial Guinea","code": "GQ"},{"name": "Eritrea","code": "ER"},{"name": "Estonia","code": "EE"},{"name": "Ethiopia","code": "ET"},{"name": "Falkland Islands (Malvinas)","code": "FK"},{"name": "Faroe Islands","code": "FO"},{"name": "Fiji","code": "FJ"},{"name": "Finland","code": "FI"},{"name": "France","code": "FR"},{"name": "French Guiana","code": "GF"},{"name": "French Polynesia","code": "PF"},{"name": "French Southern Territories","code": "TF"},{"name": "Gabon","code": "GA"},{"name": "Gambia","code": "GM"},{"name": "Georgia","code": "GE"},{"name": "Germany","code": "DE"},{"name": "Ghana","code": "GH"},{"name": "Gibraltar","code": "GI"},{"name": "Greece","code": "GR"},{"name": "Greenland","code": "GL"},{"name": "Grenada","code": "GD"},{"name": "Guadeloupe","code": "GP"},{"name": "Guam","code": "GU"},{"name": "Guatemala","code": "GT"},{"name": "Guernsey","code": "GG"},{"name": "Guinea","code": "GN"},{"name": "Guinea-Bissau","code": "GW"},{"name": "Guyana","code": "GY"},{"name": "Haiti","code": "HT"},{"name": "Heard Island and Mcdonald Islands","code": "HM"},{"name": "Holy See (Vatican City State)","code": "VA"},{"name": "Honduras","code": "HN"},{"name": "Hong Kong","code": "HK"},{"name": "Hungary","code": "HU"},{"name": "Iceland","code": "IS"},{"name": "India","code": "IN"},{"name": "Indonesia","code": "ID"},{"name": "Iran, Islamic Republic Of","code": "IR"},{"name": "Iraq","code": "IQ"},{"name": "Ireland","code": "IE"},{"name": "Isle of Man","code": "IM"},{"name": "Israel","code": "IL"},{"name": "Italy","code": "IT"},{"name": "Jamaica","code": "JM"},{"name": "Japan","code": "JP"},{"name": "Jersey","code": "JE"},{"name": "Jordan","code": "JO"},{"name": "Kazakhstan","code": "KZ"},{"name": "Kenya","code": "KE"},{"name": "Kiribati","code": "KI"},{"name": "Korea, Democratic People\"S Republic of","code": "KP"},{"name": "Korea, Republic of","code": "KR"},{"name": "Kuwait","code": "KW"},{"name": "Kyrgyzstan","code": "KG"},{"name": "Lao People\"S Democratic Republic","code": "LA"},{"name": "Latvia","code": "LV"},{"name": "Lebanon","code": "LB"},{"name": "Lesotho","code": "LS"},{"name": "Liberia","code": "LR"},{"name": "Libyan Arab Jamahiriya","code": "LY"},{"name": "Liechtenstein","code": "LI"},{"name": "Lithuania","code": "LT"},{"name": "Luxembourg","code": "LU"},{"name": "Macao","code": "MO"},{"name": "Macedonia, The Former Yugoslav Republic of","code": "MK"},{"name": "Madagascar","code": "MG"},{"name": "Malawi","code": "MW"},{"name": "Malaysia","code": "MY"},{"name": "Maldives","code": "MV"},{"name": "Mali","code": "ML"},{"name": "Malta","code": "MT"},{"name": "Marshall Islands","code": "MH"},{"name": "Martinique","code": "MQ"},{"name": "Mauritania","code": "MR"},{"name": "Mauritius","code": "MU"},{"name": "Mayotte","code": "YT"},{"name": "Mexico","code": "MX"},{"name": "Micronesia, Federated States of","code": "FM"},{"name": "Moldova, Republic of","code": "MD"},{"name": "Monaco","code": "MC"},{"name": "Mongolia","code": "MN"},{"name": "Montserrat","code": "MS"},{"name": "Morocco","code": "MA"},{"name": "Mozambique","code": "MZ"},{"name": "Myanmar","code": "MM"},{"name": "Namibia","code": "NA"},{"name": "Nauru","code": "NR"},{"name": "Nepal","code": "NP"},{"name": "Netherlands","code": "NL"},{"name": "Netherlands Antilles","code": "AN"},{"name": "New Caledonia","code": "NC"},{"name": "New Zealand","code": "NZ"},{"name": "Nicaragua","code": "NI"},{"name": "Niger","code": "NE"},{"name": "Nigeria","code": "NG"},{"name": "Niue","code": "NU"},{"name": "Norfolk Island","code": "NF"},{"name": "Northern Mariana Islands","code": "MP"},{"name": "Norway","code": "NO"},{"name": "Oman","code": "OM"},{"name": "Pakistan","code": "PK"},{"name": "Palau","code": "PW"},{"name": "Palestinian Territory, Occupied","code": "PS"},{"name": "Panama","code": "PA"},{"name": "Papua New Guinea","code": "PG"},{"name": "Paraguay","code": "PY"},{"name": "Peru","code": "PE"},{"name": "Philippines","code": "PH"},{"name": "Pitcairn","code": "PN"},{"name": "Poland","code": "PL"},{"name": "Portugal","code": "PT"},{"name": "Puerto Rico","code": "PR"},{"name": "Qatar","code": "QA"},{"name": "Reunion","code": "RE"},{"name": "Romania","code": "RO"},{"name": "Russian Federation","code": "RU"},{"name": "RWANDA","code": "RW"},{"name": "Saint Helena","code": "SH"},{"name": "Saint Kitts and Nevis","code": "KN"},{"name": "Saint Lucia","code": "LC"},{"name": "Saint Pierre and Miquelon","code": "PM"},{"name": "Saint Vincent and the Grenadines","code": "VC"},{"name": "Samoa","code": "WS"},{"name": "San Marino","code": "SM"},{"name": "Sao Tome and Principe","code": "ST"},{"name": "Saudi Arabia","code": "SA"},{"name": "Senegal","code": "SN"},{"name": "Serbia and Montenegro","code": "CS"},{"name": "Seychelles","code": "SC"},{"name": "Sierra Leone","code": "SL"},{"name": "Singapore","code": "SG"},{"name": "Slovakia","code": "SK"},{"name": "Slovenia","code": "SI"},{"name": "Solomon Islands","code": "SB"},{"name": "Somalia","code": "SO"},{"name": "South Africa","code": "ZA"},{"name": "South Georgia and the South Sandwich Islands","code": "GS"},{"name": "Spain","code": "ES"},{"name": "Sri Lanka","code": "LK"},{"name": "Sudan","code": "SD"},{"name": "Suriname","code": "SR"},{"name": "Svalbard and Jan Mayen","code": "SJ"},{"name": "Swaziland","code": "SZ"},{"name": "Sweden","code": "SE"},{"name": "Switzerland","code": "CH"},{"name": "Syrian Arab Republic","code": "SY"},{"name": "Taiwan","code": "TW"},{"name": "Tajikistan","code": "TJ"},{"name": "Tanzania, United Republic of","code": "TZ"},{"name": "Thailand","code": "TH"},{"name": "Timor-Leste","code": "TL"},{"name": "Togo","code": "TG"},{"name": "Tokelau","code": "TK"},{"name": "Tonga","code": "TO"},{"name": "Trinidad and Tobago","code": "TT"},{"name": "Tunisia","code": "TN"},{"name": "Turkey","code": "TR"},{"name": "Turkmenistan","code": "TM"},{"name": "Turks and Caicos Islands","code": "TC"},{"name": "Tuvalu","code": "TV"},{"name": "Uganda","code": "UG"},{"name": "Ukraine","code": "UA"},{"name": "United Arab Emirates","code": "AE"},{"name": "United Kingdom","code": "GB"},{"name": "United States","code": "US"},{"name": "United States Minor Outlying Islands","code": "UM"},{"name": "Uruguay","code": "UY"},{"name": "Uzbekistan","code": "UZ"},{"name": "Vanuatu","code": "VU"},{"name": "Venezuela","code": "VE"},{"name": "Viet Nam","code": "VN"},{"name": "Virgin Islands, British","code": "VG"},{"name": "Virgin Islands, U.S.","code": "VI"},{"name": "Wallis and Futuna","code": "WF"},{"name": "Western Sahara","code": "EH"},{"name": "Yemen","code": "YE"},{"name": "Zambia","code": "ZM"},{"name": "Zimbabwe","code": "ZW"},]
	num_results = 0
	error = False
	results = []
	error_msg = 'Try again!'
	keywords = {"user":0, "password":0, "admin":0, "invoice":0, "order":0, "receipt":0, "resumes":0, "citizen":0, "credential":0}

	if request.method == 'POST':
		
		selected_country = request.form.get('country')

		time_before = timer()
		
		try:
			results = get_shodan_results(selected_country)
		except Exception as e:
			return render_template('index.html', countries=countries, selected_country=selected_country, results=results, error=error, error_msg=e)
		
		if results:
			session['json_data'] = dict(results)
			num_results = len(results)
			for keyword in keywords:
				for body in results:
					if keyword in body[1]:
						keywords[keyword] += 1


		
			print("Time for the whole thing: " + str(timer() - time_before))
			return render_template('index.html', countries=countries, num_results=num_results, keywords=keywords, selected_country=selected_country, results=results, error=error)

	return render_template('index.html', countries=countries, num_results=num_results, error=error)

@app.route("/export/json", methods=['GET'])
def summary():
	results = session['json_data']
	dict_results = {}
	counter = 0
	for key in results:
		dict_results[str(counter)] = {"url":str(key),"body":str(results[key])}
		counter += 1
	return jsonify(dict_results)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    return c

def fetch_host_id(host):
	hostid = ''
	cursor = get_db_connection()
	url = "http://{}/_cat/indices?v".format(host)
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'}
	try:
		response = r.get(url, headers=headers, timeout=5)
		status = response.status_code

		if status != 200:
			hostid = cursor.execute('select id from elastic where host = "{}"'.format(host)).fetchall()[0]
			print(hostid)
			return hostid
	except Exception as e:
		hostid = cursor.execute('select id from elastic where host = "{}"'.format(host)).fetchall()[0]
		print(hostid)
		return hostid

def delete_from_database(id):
    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Insert data into the table
    cursor.execute('DELETE FROM elastic WHERE id = ?', (id,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

@app.route("/cleanup", methods=['GET'])
def cleanup():
	cursor = get_db_connection()
	hosts_in_database = cursor.execute("select host from elastic").fetchall()
	to_delete = []
	num_threads = min(10, len(hosts_in_database))
	with ThreadPoolExecutor(max_workers=num_threads) as executor:
		to_delete = executor.map(fetch_host_id, hosts_in_database)
	
	for id in to_delete:
		if id is not None:
			print("Deleting {}".format(id))
			try:
				delete_from_database(id)
			except Exception as e:
				print(f"Error deleting row with id {id}: {e}")

	return render_template('cleanup.html')

def insert_into_database(host, country):
    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Insert data into the table
    cursor.execute("INSERT INTO elastic (host, country) VALUES (?, ?);",
                   (host, country))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def fetch_url(host):
	url = "http://{}/_cat/indices?v".format(host)
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'}
	status = ''
	try:
		response = r.get(url, headers=headers, timeout=5)
		status, body = response.status_code, response.text
		
		# If they are alive and reachable
		if status == 200:
			
			# add to results
			return (url,body), host
	except Exception as e:
		if status:
			print("{} - {}".format(url,status))
		else:
			print("{} - {}".format(url,e))

def get_shodan_results(country_code):
	print('Hi!')
	country_code = country_code.lower()
	cursor = get_db_connection()
	results = api.search('product:elastic "200 OK" country:{} "GB"'.format(country_code))
	
	# Results of the shodan query
	hosts = []

	# Temp hosts list to get content from
	new_hosts = []

	# End results
	end_results = []
	
	# for anew
	hosts_in_database = cursor.execute("select host from elastic where country is '{}'".format(country_code)).fetchall()


	# grab all IPv4 from the query results
	for result in results['matches']:
		host = result['ip_str'] + ':' + str(result['port'])
		if ipv4_pattern.search(host):
			hosts.append(host)

	hosts_not_in_database = list(set(hosts) - set(hosts_in_database))
	
	# DEBUG
	print("hosts_not_in_database")
	print(hosts_not_in_database)

	#thread_results = []
	num_threads = min(10, len(hosts_not_in_database))
	with ThreadPoolExecutor(max_workers=num_threads) as executor:
		thread_results = executor.map(fetch_url, hosts_not_in_database)

	for result in thread_results:
		if result is not None:
			end_results.append(result[0])
			insert_into_database(result[1],country_code)

	return end_results

if __name__ == '__main__':
	app.run(debug=True)
