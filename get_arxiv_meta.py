import urllib
import feedparser
import time
import json
import re


def form_url(id):
    url = 'http://export.arxiv.org/api/query?search_query=id:'+ id
    return url

def parse_response(response):
    feed = feedparser.parse(response)
    if not feed.entries:
        return "Not Found"
    for entry in feed.entries:
        RP={}
        ID = entry.id.split('/abs/')[-1]
        Publish = entry.published.strip()
        Title = entry.title.strip()
        Summary = entry.summary.strip()
        Author = []
        for author in entry.authors:
            Author.append(author.name.strip().encode("utf-8"))
        Cat = []
        for category in entry.tags:
            Cat.append(category['term'].strip().encode("utf-8"))

        Cat = Cat[:-1]

        RP['id']=ID
        RP['pub']=Publish
        RP['tit']=Title
        RP['sum']=Summary
        RP['aut']=Author
        RP['cat']=Cat

    return RP

def clean(id):
    new_id =id
    if not new_id[:1].isdigit():
        m = re.search("\d", id)
        pos = m.start()
        new_id = id[:pos] + '/' + id[pos:]
    return new_id

# Return metadata by ID

def call_api(id):
    c_id = clean(id)
    url = form_url(c_id)
    response = urllib.urlopen(url).read()
    cont = parse_response(response)
    return cont