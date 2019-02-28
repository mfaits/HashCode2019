# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 14:21:38 2019

@author: faitsmc
"""

from __future__ import print_function
from ortools.graph import pywrapgraph
import time
import numpy as np

input_file = open('parseData/example_dont_delete.txt','r')

def score(tags_1, tags_2):
 inner_score = sum([1 for element in list(set(tags_1) & set(tags_2))])
 left_outer_score = sum([1 for element in list(set(tags_1) - set(tags_2))])
 right_outer_score = sum([1 for element in list(set(tags_2) - set(tags_1))])
 return min([inner_score, left_outer_score, right_outer_score])


def optimize(input_file):
 """Solving an Assignment Problem with MinCostFlow"""

 # Instantiate a SimpleMinCostFlow solver.
 min_cost_flow = pywrapgraph.SimpleMinCostFlow()
 # Define the directed graph for the flow.



 nodes = [line for line in input_file]

 start_nodes = [0] * len(nodes)
 end_nodes = [i for i in range(1, len(nodes) + 1)]
 costs = [0] * len(nodes)

 for index, node_1 in enumerate(nodes):
   node_1_line = node_1.split(',')
   node_1_id_num = index+1
   node_1_num_tags = node_1_line[1]
   node_1_tags = node_1_line[2].split(' ')
   for index2, node_2 in enumerate(nodes):
     if node_1 != node_2:
       node_2_line = node_2.split(',')
       node_2_id_num = index2+1+len(nodes)
       node_2_num_tags = node_2_line[1]
       node_2_tags = node_2_line[2].split(' ')
       start_nodes += [int(node_1_id_num)]
       end_nodes += [int(node_2_id_num)]
       costs += [10000000 - (score(node_1_tags, node_2_tags))]



 start_nodes += range(len(nodes) + 1,2*len(nodes)+1)
 end_nodes += [2*len(nodes) + 1] * len(nodes)
 capacities =  [1] * len(start_nodes)
 costs  += [0] * len(nodes)
 
 print(len(start_nodes))
 print(len(end_nodes))
 print(len(capacities))
 print(len(costs))

 # Define an array of supplies at each node.
 supplies = [len(nodes)] + ([0] * len(nodes)) + [-1 * len(nodes)]
 source = 0
 sink = 2*len(nodes) + 1

 # Add each arc.
 for i in range(len(start_nodes)):
   min_cost_flow.AddArcWithCapacityAndUnitCost(start_nodes[i], end_nodes[i],
                                               capacities[i], costs[i])

 # Add node supplies.

 for i in range(len(supplies)):
   min_cost_flow.SetNodeSupply(i, supplies[i])
 # Find the minimum cost flow between node 0 and node 10.
 if min_cost_flow.Solve() == min_cost_flow.OPTIMAL:
   print('Total cost = ', min_cost_flow.OptimalCost())
   print()
   for arc in range(min_cost_flow.NumArcs()):

     # Can ignore arcs leading out of source or into sink.
     if min_cost_flow.Tail(arc)!=source and min_cost_flow.Head(arc)!=sink:
       #print(arc)

       # Arcs in the solution have a flow value of 1. Their start and end nodes
       # give an assignment of worker to task.

       if min_cost_flow.Flow(arc) > 0:
         print(arc)
         print('Worker %d assigned to task %d.  Cost = %d' % (
               min_cost_flow.Tail(arc),
               min_cost_flow.Head(arc),
               min_cost_flow.UnitCost(arc)))
 else:
   print('There was an issue with the min cost flow input.')
   
optimize(input_file)
