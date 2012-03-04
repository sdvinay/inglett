#!/usr/bin/python

from pyevolve import G1DList
from pyevolve import GSimpleGA
import csv

playerPT = []
playerScores = []
playerNames = []

f = open ("stats_02.csv", 'r')
statReader = csv.reader(f)
for row in statReader:
	playerScores.append(int(row[3]))
	playerPT.append(int(row[2]))
	playerNames.append(row[4])
	

def eval_func(chromosome):
   score = 0.0
   PT = 0.0
   # iterate over the chromosome
   for value in chromosome:
#print value, playerScores[value]
      score += (playerScores[value] * playerPT[value])
      PT += playerPT[value]
   return score/PT

genome = G1DList.G1DList(20)
genome.setParams(rangemin=0, rangemax=299)
genome.evaluator.set(eval_func)
ga = GSimpleGA.GSimpleGA(genome)
ga.evolve(freq_stats=10)
print ga.bestIndividual()
