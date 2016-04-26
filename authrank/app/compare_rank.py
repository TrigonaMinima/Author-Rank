from urllib.request import urlopen
import feedparser

from py2neo import authenticate, Graph, Node, Relationship
from pprint import pprint

graph = Graph("http://localhost:7474/db/data")


seed = 'http://export.arxiv.org/api/query?search_query=id:'

query = """
match (n)-[:Published]->(m)-[:BelongsTo]->(c)
where c.name = {cat} return n.name, sum(m.q_score) as Score, c.subject
order by Score DESC;
"""

def parse_response(response):
    resp_dict={}
    feed = feedparser.parse(response)
    if not feed.entries:
        return "Not Found"

    title = feed.entries[0].title.strip()

    author = []
    for aut in feed.entries[0].authors:
    	author.append(aut.name.strip())


    category = []
    for cat in feed.entries[0].tags:
    	category.append(cat['term'].strip())


    resp_dict['aut'] = author
    resp_dict['cat'] = category
    resp_dict['tit'] = title

    return resp_dict

def get_rank(C):
    disp_data={}
    rank_dict={}
    disp_data['T'] = C['tit']

    for c in C['cat']:
        rank_list=[]
        cat_avalbl = graph.cypher.execute(query, cat=c)

        if len(cat_avalbl) == 0:
            continue

        for b in  cat_avalbl:
            rank_list.append(b[0])

        aut_rank={}
        for a in C['aut']:
            try:
                aut_rank[a] = rank_list.index(a) + 1
            except:
                aut_rank[a] = None

        rank_dict[b[2]] = aut_rank


    disp_data['rank'] = rank_dict

    return disp_data




def compare_rank(id):
    url = seed + id
    response = urlopen(url).read()
    content = parse_response(response)
    rank_dict = get_rank(content)
    return rank_dict





