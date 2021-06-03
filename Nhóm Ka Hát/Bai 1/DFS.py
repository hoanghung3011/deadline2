
def DFS(graph, start):
    #check what the current vertex connected with
    visited = set()


    #mark the starting vertex as visited
	visited.add(start)
	print(start)


    #dfs traversal starting from all vertex one by one
	for next in graph[start] - visited:
		DFS(graph, next, visited)




#example: setting egde for each vertex.
graph = {'0': set(['1', '2']),
         '1': set(['0', '3', '4']),
         '2': set(['0']),
         '3': set(['1']),
         '4': set(['2', '3'])}

DFS(graph, '0')

