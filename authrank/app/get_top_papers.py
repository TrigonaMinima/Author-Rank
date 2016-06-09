from py2neo import authenticate, Graph, Node, Relationship

from .config import graph_url

graph = Graph(graph_url)


def form_query(cat, limit):
    query_top_authors = "match (m)-[:BelongsTo]->(c) where c.name = '" + cat + \
        "' return m.title, m.q_score as Score order by Score DESC LIMIT " + limit
    return query_top_authors


def get_top_papers(cat, limit):
    limit = str(limit)
    resp = graph.cypher.execute(form_query(cat, limit))
    list_papers = []

    for i in range(0, len(resp)):
        list_papers.append(resp[i][0])

    return list_papers
