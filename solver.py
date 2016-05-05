movesString="""A NTH-Bel 2
A Pic-Bel 2
A Pic-Bur 2
Bel H
A NWG S NTH - EDI 100
"""
import random
import re

movePattern = re.compile("([A|F] )?\s*(\w+)\s*-\s*(\w+)\s*(\d+)?")
holdPattern = re.compile("([A|F] )?\s*(\w+)\s*[H ]?\s*(\d+)?")
supportPattern = re.compile("([A|F] )?\s*(\w+)\s+S\s+(\w+)\s*-\s*(\w+)\s*(\d+)?")

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def chance(p):
  return p >= random.random()

class Move(object):
  """docstring for Move"""
  def __init__(self, province, origin, dest, prob, isSupporting):
    super(Move, self).__init__()
    self.origin = origin
    self.province = province
    self.dest = dest
    self.prob = prob
    self.isSupporting = isSupporting

allMoveList = list()
for l in movesString.split('\n'):
  if len(l) <= 2: continue
  prob, province, origin, dest, isSupporting = 1.0, None, None, None, False

  if supportPattern.match(l):
    province, origin, dest = supportPattern.search(l).group(2),  supportPattern.search(l).group(3), supportPattern.search(l).group(4)
    prob = supportPattern.search(l).group(5)
    isSupporting = True
  elif movePattern.match(l):
    origin, dest = movePattern.search(l).group(2),  movePattern.search(l).group(3)
    prob = movePattern.search(l).group(4)
    province = origin
  elif holdPattern.match(l):
    origin = holdPattern.search(l).group(2)
    prob = holdPattern.search(l).group(3)
    province = origin
    dest = origin

  if not prob:
    prob = 1.0
  else:
    prob = float(prob)

  allMoveList.append(Move(province, origin, dest, prob, isSupporting))

provinces = list(set([m.province for m in allMoveList]))
provinceToMovesMap = dict()

for prov in provinces:
  provinceToMovesMap[prov] = [m for m in allMoveList if m.province == prov]

from collections import Counter
def playGame():
  moves = []

  # get this game's moves
  for prov in provinceToMovesMap.keys():
    movesForProvince = provinceToMovesMap[prov]
    probSum = sum([m.prob for m in movesForProvince])
    if prov == 'NWG':
      print probSum

    randomFloat = random.random()
    runningP = 0.0
    for m in movesForProvince:
      p = m.prob / probSum
      runningP += p
      if prov == 'NWG':
        print randomFloat, '<=', runningP

      if randomFloat <= runningP:
        moves.append(m)
        break
  print [(x.province, x.origin, x.dest) for x in moves]

  # get destination map
  destToMovesMap = dict()
  for dest in [m.dest for m in moves]:
    if dest not in destToMovesMap:
      destToMovesMap[dest] = []
    destToMovesMap[dest].append(m)

  print destToMovesMap


# print [(x.origin, x.dest) for x in allMoveList]
# playGame()
for i in range(1):
  playGame()
