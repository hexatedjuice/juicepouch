#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import argparse
import time
import pandas as pd


p = argparse.ArgumentParser('timeline information')
p.add_argument('--usr', type=str, required=True)
p.add_argument('--pwd', type=str, required=True)
p.add_argument('--url', type=str, required=True)
p.add_argument('--file', type=str, required=True)

args = p.parse_args()
URL = args.url
USR = args.usr
PWD = args.pwd
FILE = args.file

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

#login
driver.get("https://www.tiki-toki.com/#login")

time.sleep(1)

user = driver.find_element_by_name("username")
user.send_keys(USR)
password = driver.find_element_by_name("tikitokipassword")
password.send_keys(PWD + Keys.RETURN)

#go to timeline
time.sleep(1)

tl = driver.find_element_by_class_name("tlsp-ali-title")
tl.click()

time.sleep(1)

# #automation
df = pd.read_csv(FILE)
df.set_index("number")
contentAreas = {0:1,1:2,2:4,3:5,4:6,5:7,6:8,7:9,8:10,9:11,10:3}
for index, row in df.iterrows():
	if (index > -1):
		#initiate creation
		create = driver.find_element_by_xpath("//*[contains(text(), 'Create New Story')]")
		create.click()

		#add information
		title = driver.find_element_by_id("tl-ah-field-id-title")
		title.clear()
		title.send_keys(row["number"], " ", row["name"])

		a, b = row["time"].strip().split(" ")
		sdate = driver.find_element_by_id("tl-ah-field-id-startDate")
		sdate.clear()
		sdate.send_keys("01 Jan ", format(int(a), '04d')," ", b.replace("BCE", "BC").replace("CE",""), " 00:00:00")

		edate = driver.find_element_by_id("tl-ah-field-id-endDate")
		edate.clear()
		edate.send_keys("01 Jan ", format(int(a), '04d')," ", b.replace("BCE", "BC").replace("CE",""), " 00:00:00")

		info = driver.find_element_by_id("tl-ah-field-id-text")
		info.clear()
		info.send_keys("\n".join([str(row["material"]),str(row["location"]),str(row["culture"])]))

		content = Select(driver.find_element_by_id("tl-ah-story-category-select"))
		content.select_by_index(contentAreas[int(row["ca"])])

		add = driver.find_element_by_xpath("//*[contains(text(), 'Save')]")
		add.click()
		
		# media = driver.find_element_by_xpath("//*[contains(text(), 'Media')]")
		media = driver.find_element_by_id("tl-extra-media-tab-menu-item")
		media.click()
		media = driver.find_element_by_xpath("//*[contains(text(), 'Add New Media')]")
		media.click()

		# sep = driver.find_element_by_class_name("tl-ah-search-button")
		# sep.click()

		li = driver.find_element_by_xpath("(//input)[9]")
		li.send_keys(str(row["img"]))

		li = driver.find_element_by_name("caption")
		li.send_keys(str(row["img"]))
		# print(len(li))

		add = driver.find_element_by_xpath("(//a[contains(@class, 'rt-button-4') and contains(@class, 'ajk-verifier-submit')])[2]")
		add.click()

		print("done", row["number"], " ", row["name"])

	




