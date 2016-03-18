import urllib
import feedparser
import time
import json


def form_url(category,start,max_res):
    url = 'http://export.arxiv.org/api/query?search_query=cat:'+\
           category + '&start=' + str(start) + '&max_results=' + str(max_res) 
    return url

def get_list_categories(filename):
    return [line.rstrip('\n') for line in open(filename)]

def parse_response(response):
    feed = feedparser.parse(response)
    if not feed.entries:
        return False
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
        
        RP['id']=ID
        RP['pub']=Publish
        RP['tit']=Title
        RP['sum']=Summary
        RP['aut']=Author
        RP['cat']=Cat
        
        file_name = ID+".json"
        out_file = open(file_name,"w")
        json.dump(RP,out_file)
        
    return True
    
def call_api(cat):
    time.sleep(1)
    start_time = 0
    max_result = 1000
    cont = True
    while(cont):
        url = form_url(cat,start_time,max_result)
        response = urllib.urlopen(url).read()
        cont = parse_response(response)
        start_time += max_result
        break
    

if __name__ == '__main__':
    categories = get_list_categories('categories.txt')
    for category in categories:
        call_api(category)
    ids_arxiv.close();
    