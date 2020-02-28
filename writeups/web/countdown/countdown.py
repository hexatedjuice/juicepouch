#!/usr/bin/env python2

import requests

pages = ['https://assess.girlsgocyberstart.org/challenge-files/clock-pt1?verify=ieM9d9shIdgsmZ%2B7tnLIjg%3D%3D',
'https://assess.girlsgocyberstart.org/challenge-files/clock-pt2?verify=ieM9d9shIdgsmZ%2B7tnLIjg%3D%3D',
'https://assess.girlsgocyberstart.org/challenge-files/clock-pt3?verify=ieM9d9shIdgsmZ%2B7tnLIjg%3D%3D',
'https://assess.girlsgocyberstart.org/challenge-files/clock-pt4?verify=ieM9d9shIdgsmZ%2B7tnLIjg%3D%3D',
'https://assess.girlsgocyberstart.org/challenge-files/clock-pt5?verify=ieM9d9shIdgsmZ%2B7tnLIjg%3D%3D']

final = []

for i in range(0,5):
	page = requests.get(pages[i])
	piece = page.text
	final.append(piece)

flag = requests.get("https://assess.girlsgocyberstart.org/challenge-files/get-flag?verify=ieM9d9shIdgsmZ%2B7tnLIjg%3D%3D&string=" + ''.join(final))

print(flag.text)
