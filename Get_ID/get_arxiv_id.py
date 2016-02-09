import urllib
import feedparser
import time

ids_arxiv = open("ids_arxiv.txt","a")

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
        ID = entry.id.split('/abs/')[-1]
        ids_arxiv.write(ID+'\n')
    return True
    
def call_api(cat):
    time.sleep(3)
    start_time = 0
    max_result = 1000
    cont = True
    while(cont):
        url = form_url(cat,start_time,max_result)
        response = urllib.urlopen(url).read()
        cont = parse_response(response)
        start_time += max_result
    
    

if __name__ == '__main__':
    categories = get_list_categories('categories.txt')
    for category in categories:
        call_api(category)
    ids_arxiv.close();
