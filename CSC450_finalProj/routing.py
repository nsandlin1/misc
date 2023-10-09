import csv
import sys
from time import sleep

# for use in Dijkstra's Algorithm
class PriorityQueue:
	def __init__(self):
		self.queue = []
	def insert(self, value, priority):
		self.queue.append((value, priority))
	def pop(self):
		curr_index = -1
		curr_priority = float('inf')
		for i in range(len(self.queue)):
			if self.queue[i][1] < curr_priority:
				curr_index = i
				curr_priority = self.queue[i][1]
		if curr_index == -1:
			return None
		return self.queue.pop(curr_index)
	def __str__(self):
		return str(self.queue)
	def empty(self):
		return len(self.queue) == 0

# For creation of the shortest path tree
class Node:
	def __init__(self, X):
		self.value = X
		self.children = []
	# __repr__ for testing not my code
	def __repr__(self, level=0):
		s = "\t"*level+str(self.value)+"\n"
		for child in self.children:
			s += child.__repr__(level+1)
		return s

# Rather than construct the shortest path tree inside dijkstra, pass the 
# previous array and the names array into previous_to_spt which converts them into the tree.
def previous_to_spt(previous,names):
	nodes = []

	for node in range(len(previous)):
		nodes.append(Node(names[node]))
	for i in range(len(previous)):
		if previous[i] == None:
			head = i
		else:
			nodes[previous[i]].children.append(nodes[i])

	return nodes[head]

# find all paths from given shortest path tree
def tree_to_listh(head):
	if head.children == []:
		return [[head.value]]

	res = [[head.value]]
	for child in head.children:
		cl = tree_to_listh(child)
		for item in cl:
			res.append([head.value]+item)

	return res

def tree_to_list(head):
	res_temp = tree_to_listh(head)
	d = {}
	for item in res_temp:
		d[''.join(item)] = len(item)

	return [x[0] for x in sorted(d.items(), key=lambda x: x[1])]

# takes a node and a matrix and returns the following:
# 	distance: minimum distance between starting_node and each other node
# 	previous: previous node for each node in the traversal
def dijkstra(matrix, starting_node):
	# initialize distance array
	distance = []
	previous = [None]*len(matrix)
	for i in range(len(matrix)):
		if i == starting_node:
			distance.append(0)
		else:
			distance.append(9999)

	# which nodes have been visited
	visited = [False]*len(matrix)

	# initialize priority queue
	pqueue = PriorityQueue()
	# push starting node to queue
	pqueue.insert(starting_node, 0)

	# find paths
	# protects from disconnected graphs
	while not pqueue.empty():
		curr_node = pqueue.pop()
		visited[curr_node[0]] = True
		for node in range(len(matrix)):
			if visited[node]:
				continue
			newdist = distance[curr_node[0]] + matrix[curr_node[0]][node]
			if newdist < distance[node]:
				distance[node] = newdist
				previous[node] = curr_node[0]
				pqueue.insert(node, newdist)
	
	# return the distance and previous node of traversal
	return distance, previous

def bellman_ford(matrix, starting_node):
	# initialize distance matrix
	dist = [9999] * len(matrix)
	dist[starting_node] = 0

	# visit edges v - 1 times. This is because with v vertices, the longest
	# path is at most of length v - 1
	for _ in range(len(matrix) - 1):
		# traverse and compare the distance to each node
		# through each other node
		for row in range(len(matrix)):
			for column in range(len(matrix)):
				if dist[row] + matrix[row][column] < dist[column]:
					dist[column] = dist[row] + matrix[row][column]
	
	return dist


if __name__ == '__main__':
	# define correct number of arguments
	if len(sys.argv) != 2:
		print("invalid arguments")
		exit(1)
	
	# open csv file and reader
	csv_file = open(sys.argv[1])
	csvreader = csv.reader(csv_file)
	
	# list of nodes in the csv matrix
	nodes = next(csvreader)[1:]
	
	# get csv distance matrix
	dmatrix = []
	for row in csvreader:
		crow = []
		for item in row[1:]:
			crow.append(int(item))
		dmatrix.append(crow)
	
	# get shortest path tree and least cost paths array
	source_node = input("Please, provide the source node: ")
	least_cost_paths, previous = dijkstra(dmatrix, nodes.index(source_node))
	shortest_path_tree = previous_to_spt(previous,nodes)

	# print formatted outputs
	print(f"Shortest path tree for node {source_node}:")
	paths = tree_to_list(shortest_path_tree)
	for i in range(1,len(paths)):
		if i == len(paths)-1:
			print(f"{paths[i]}")
		else:
			print(f"{paths[i]}, ", end="")

	print(f"Costs of the least-cost paths for node {source_node}:")
	for i in range(len(nodes)):
		if i == len(nodes)-1:
			print(f"{nodes[i]}:{least_cost_paths[i]}\n")
		else:
			print(f"{nodes[i]}:{least_cost_paths[i]}, ", end="")

	for node in range(len(nodes)):
		print(f"Distance vector for node {nodes[node]}: ", end="")
		distances = bellman_ford(dmatrix, node)
		for d in distances:
			print(f"{d} ", end="")
		print()

	csv_file.close()
	
	
