#!/usr/bin/env python3

from lxml import html
import requests
import bs4
import re
import sys

def main(argv):
	#defining user params
	payload = {
		'Database' : 10,
		'LogOnDetails.UserName' : argv[1],
		'LogOnDetails.Password' : argv[2],
	}
	baseUrl = argv[0]
	r = requests.session()

	try:
		result = login(baseUrl, payload, r)
	except:
		invalidServer(
)
	if "Your attempt to log in was unsuccessful" in result.text:
		invalidLogin()
	elif "Schedule" in result.text:
		getGrades(baseUrl, r)


def login(baseUrl, payload, r):
	url = baseUrl + "/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2f"
	result = r.post(url, data = payload)

	return result


def invalidServer():
	print("Invalid hac server address.")
	quit()

def invalidLogin():
	print("Your login was invalid...")
	quit()

#scraping student grades
def getGrades(baseUrl, r):
	print("One moment please...\n")
	url = baseUrl + "/HomeAccess/Content/Student/Assignments.aspx"
	result = r.get(url)
	soup = bs4.BeautifulSoup(result.text, 'lxml')

	classes = soup.findAll('a', {'class' : "sg-header-heading"})
	averages = soup.findAll('span', id = re.compile("plnMain_rptAssigmnetsByCourse_lblHdrAverage_"))

	# finding assignment tables
	tables = soup.findAll('table', id = re.compile("plnMain_rptAssigmnetsByCourse_dgCourseAssignments_"))

	for table in tables:
		print(classes[tables.index(table)].text.strip() + "        " + averages[tables.index(table)].text)
		rows = table.findAll('tr')
		for tr in rows[1:]:
			td = tr.findAll('td')
			row = [i.text for i in td]
			print("Date Due: " + row[0] + "      " + row[2].strip()[:-1].strip() + "     " + row[5])
		print("\n\n\n")



if __name__ == '__main__':
	main(sys.argv[1:])
