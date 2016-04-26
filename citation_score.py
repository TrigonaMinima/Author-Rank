from py2neo import authenticate, Graph, Node, Relationship
from pprint import pprint

graph = Graph("http://localhost:7474/db/data")

get_ref_query = """
MATCH (p:Paper)-[:Refers]->(r:Paper)
WHERE r.id = {name}
RETURN p
"""

num_ref_query = """
MATCH (p:Paper)-[:Refers]->(r:Paper)
WHERE p.id = {name}
RETURN count(p)
"""

#Calculation of Quality Score (q_score)
'''
for a in  graph.cypher.execute("match (n:Paper) RETURN n"):
	node = a[0]
	node['q_score'] = 0.01   #TBD
	node.push()
'''

for i in range(0,6):    #TBD
	for a in  graph.cypher.execute("match (n:Paper) RETURN n"):
		node = a[0]
		n_q_score = 0.01

		for b in graph.cypher.execute(get_ref_query, name=node['id']):
			num_of_ref = graph.cypher.execute(num_ref_query, name = b[0]['id'])[0][0]
			ref_score = b[0]['q_score']/float(num_of_ref)
			n_q_score += ref_score

		node['q_score'] = n_q_score
		node.push()

