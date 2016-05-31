
from py2neo import authenticate, Graph, Node, Relationship
from urllib.request import urlopen
import feedparser
import time
import json
import re

from app import sub_mapping

graph = Graph("http://localhost:7474/db/data")


def form_query(te, typ, cat):
    url = "http://export.arxiv.org/api/query?search_query="+typ+":'"+te+"'"
    if cat != 'all':
    	url = url + "+AND+cat:"+cat
    url = url + "&start=0&max_results=50&sortBy=relevance&sortOrder=ascending"
    return url

def parse_response(response):
    feed = feedparser.parse(response)
    if not feed.entries:
        return []
    RP={}
    ind = 0
    for entry in feed.entries:
        rp={}
        ind +=1
        ID = entry.id.split('/abs/')[-1]
        Publish = entry.published.strip()
        Title = entry.title.strip()
        Summary = entry.summary.strip()
        Author = []
        for author in entry.authors:
            Author.append(author.name.strip().encode("utf-8"))
        Cat = []
        for category in entry.tags:
            subject_name = sub_mapping.map_id_to_name(category['term'].strip())
            if subject_name:
            		Cat.append(subject_name)

        rp['id']=ID
        rp['pub']=Publish
        rp['tit']=Title
        rp['sum']=Summary
        rp['aut']=Author
        rp['cat']=Cat
        RP[ind] = rp
    return RP

def  search_arxiv(term, typ, cat):
    url = form_query(term, typ, cat)
    response = urlopen(url).read()
    cont = parse_response(response)
    return cont

