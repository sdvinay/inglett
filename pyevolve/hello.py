#!/usr/bin/python

from pyevolve import G1DList
from pyevolve import Mutators
from pyevolve import Crossovers
from pyevolve import GSimpleGA
import csv
import code
import pyevolve

positions = ['C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF']

playerPT = {}
playerScores = {}
playerNames = {}

for pos in positions:
	playerPT[pos] = []
	playerScores[pos] = []
	playerNames[pos] = []

f = open ("../stats_03.csv", 'r')
statReader = csv.reader(f)
for row in statReader:
	pos = row[1]
	playerScores[pos].append(int(row[3]))
	playerPT[pos].append(int(row[2]))
	playerNames[pos].append(row[4])
	
#print playerNames

def eval_func(chromosome):
   score = 0.0
   PT = 0.0
   # iterate over the chromosome
   for i in range(len(chromosome)):
      pos = positions[i]
      playerNum = int(chromosome[i])
      score += (playerScores[pos][playerNum] * playerPT[pos][playerNum])
      PT += playerPT[pos][playerNum]
   return score/PT

# For interactive mode
	  # The generation that Pyevolve will enter on
# the interactive mode
INTERACTIVE_STOP = 100
 
def evolve_callback(ga_engine):
   """ The callback function to enter on interactive mode"""
   generation = ga_engine.getCurrentGeneration()
 
   if generation == INTERACTIVE_STOP:
      from pyevolve import Interaction
      interact_banner = "## Pyevolve v.%s - Interactive Mode ##" \
                        % (pyevolve.__version__,)
      session_locals = { "ga_engine"  : ga_engine,
                         "population" : ga_engine.getPopulation(),
                         "pyevolve"   : pyevolve,
                         "it"         : Interaction}
      print
      code.interact(interact_banner, local=session_locals)
   return False
 

genome = G1DList.G1DList(len(positions))
genome.setParams(rangemin=0, rangemax=99)
genome.evaluator.set(eval_func)
genome.mutator.set(Mutators.G1DListMutatorIntegerRange)
genome.crossover.set(Crossovers.G1DListCrossoverUniform)
ga = GSimpleGA.GSimpleGA(genome, interactiveMode=True)
#ga.setPopulationSize(1024)
ga.setGenerations(200)
ga.setMutationRate(.1)
#ga.stepCallback.set(evolve_callback)
ga.evolve(freq_stats=10)
#print ga.bestIndividual().genomeList

for i in range(0, len(positions)):
	pos = positions[i]
	print playerNames[pos][ga.bestIndividual().genomeList[i]]
