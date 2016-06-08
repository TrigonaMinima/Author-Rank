
import requests, zipfile, tarfile
import os

import io



from urllib.request import urlopen
from bs4 import BeautifulSoup

from app import sys_update


def collect_papers(id_list):
	count = 0
	for ar_id in id_list:
		r = requests.get('http://arxiv.org/e-print/'+ar_id)
		count+=1

		f_name = os.getcwd() + "/uploads/"+ar_id

		with open(f_name,"wb") as code:
			code.write(r.content)

		print("Update called for", f_name)
		sys_update.graph_update(ar_id)

def auto_feed(url):
	response = urlopen(url).read()
	soup = BeautifulSoup(response, 'html.parser')

	count = 0
	id_list = []
	for week in soup.find_all("a",{"title":"Other formats"}):

		id_list.append(week.get("href").split("/")[2])
		count+=1

	print("Count is",count)
	collect_papers(id_list)
	#print(soup.prettify())





