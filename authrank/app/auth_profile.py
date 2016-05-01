
from py2neo import authenticate, Graph, Node, Relationship

graph = Graph("http://localhost:7474/db/data")


def form_query(name):
    query_auth_papers = "match (n)-[:Published]->(m) where n.name = '"+ name +"' return m.title order by m.q_score DESC "
    return query_auth_papers


def  author_profile(name):
    resp = graph.cypher.execute(form_query(name))
    list_papers = []

    for i in range(0,len(resp)):
        list_papers.append(resp[i][0])

    return list_papers

