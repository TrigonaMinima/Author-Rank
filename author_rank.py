from py2neo import authenticate, Graph, Node, Relationship
from pprint import pprint

graph = Graph("http://localhost:7474/db/data")

'''

query = """
match (n)-[:Published]->(m)-[:BelongsTo]->(c)
where c.name = {cat} return n.name, sum(m.q_score) as Score
order by Score DESC LIMIT 5;
"""
'''

# Current state : Finds the top author in each category

for a in graph.cypher.execute("match (c:Category) return c.name"):
	print(a[0])
	for b in  graph.cypher.execute(query, cat=a[0]):
		print(b[0],b[1])


