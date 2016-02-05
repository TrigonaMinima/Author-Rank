# Calcualting Paper Citation Score(PCS)

# Example Graph : Representing Paper and their respective reference section
graph={'paper1':['paper2','paper4'],
	   'paper2':['paper3'],
	   'paper3':['paper4','paper5'],
	   'paper4':['paper5']
	  }

# Iterations to improve result at every stage(and avoid recursion).
no_of_iterations = 5

# Print paper and their PQS
def print_score(graph):
	for node in graph:
		print "PCS of",node,"is",graph[node]

# Main function to calculate PCS
def paper_citation_score(graph_of_papers, iterations):
	cur_paper_score={}

	no_of_papers = len(graph_of_papers)

	# Initial assumed rank
	for paper in graph_of_papers:
		cur_paper_score[paper]= (1.0/no_of_papers)

	for i in range(0,iterations):
		next_paper_score = {}
		for paper in graph_of_papers:
			new_score = (1.0/no_of_papers) # Minimum score (Incase no other RP has cited RP paper)	
			for node in graph_of_papers:
				# If RP node has referenced RP paper
				if paper in graph_of_papers[node]:
					new_score += cur_paper_score[node]
				
			next_paper_score[paper] = new_score	
	 	cur_paper_score = next_paper_score		

	return cur_paper_score


if __name__=="__main__":
	paper_score = paper_citation_score(graph,no_of_iterations)
	print_score(paper_score)