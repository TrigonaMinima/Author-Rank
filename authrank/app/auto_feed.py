import requests
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup

from app import sys_update


def collect_papers(id_list):
    data = {}
    datum = {}
    count = 0
    for ar_id in id_list:

        r = requests.get('http://arxiv.org/e-print/' + ar_id)
        count += 1

        f_name = os.getcwd() + "/uploads/" + ar_id

        with open(f_name, "wb") as code:
            code.write(r.content)

        datum = sys_update.graph_update(ar_id)
        if datum:
            data[count - 1] = datum
    return data


def auto_feed(url):
    response = urlopen(url).read()
    soup = BeautifulSoup(response, 'html.parser')

    id_list = []
    for week in soup.find_all("a", {"title": "Other formats"}):

        id_list.append(week.get("href").split("/")[2])

    return collect_papers(id_list)
