movesString="""
A NTH-Bel 2
A Pic-Bel 2
"""
# A Pic-Bur 2
# Bel H
# A NWG S NTH - EDI 1
# A NWG S NTH H 50
# A NWG S NTH 50

# A Hol S NTH-Bel 2
# A Mar S Pic-Bel 2
# A Ber S Pic-Bel 2
# A Mun S Pic-Bel 2

import random
import re

movePattern = re.compile("([A|F] )?\s*(\w+)\s*-\s*(\w+)\s*(\d+)?")
holdPattern = re.compile("([A|F] )?\s*(\w+)\s*[H ]?\s*(\d+)?")
supportMovePattern = re.compile("([A|F] )?\s*(\w+)\s+S\s+(\w+)\s*-\s*(\w+)\s*(\d+)?")
supportHoldPattern = re.compile("([A|F] )?\s*(\w+)\s+S\s+(\w+)\s*H?\s*(\d+)?")

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
    self.moveFailed = None
    self.numSupports = 0

  def p(self):
    print self.s()
  def s(self):
    if self.origin == self.province == self.dest:
      return self.province + ' holds '
    if self.origin == self.province != self.dest:
      return self.province + '-' + self.dest
    if self.origin != self.province != self.dest:
      return self.province + ' S ' + self.origin + '-' + self.dest


allMoveList = list()
for l in movesString.split('\n'):
  if len(l) <= 2: continue
  prob, province, origin, dest, isSupporting = 1.0, None, None, None, False

  if supportMovePattern.match(l):
    province, origin, dest = supportMovePattern.search(l).group(2),  supportMovePattern.search(l).group(3), supportMovePattern.search(l).group(4)
    prob = supportMovePattern.search(l).group(5)
    isSupporting = True
  elif supportHoldPattern.match(l):
    province, origin = supportHoldPattern.search(l).group(2),  supportHoldPattern.search(l).group(3)
    dest = origin
    prob = supportHoldPattern.search(l).group(4)
    isSupporting = True
  elif movePattern.match(l):
    origin, dest = movePattern.search(l).group(2),  movePattern.search(l).group(3)
    prob = movePattern.search(l).group(4)
    province = origin
  elif holdPattern.match(l):
    origin, prob = holdPattern.search(l).group(2),  holdPattern.search(l).group(3)
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
        # choose this move
        if m.isSupporting:
          moves.append(Move(m.province, m.province, m.province, m.prob, False))
        moves.append(m)
        break
  print [(x.province, x.origin, x.dest) for x in moves]

  # get destination map
  destToMovesMap = dict()
  for dest, m in [(m.dest, m) for m in moves]:
    if dest not in destToMovesMap:
      destToMovesMap[dest] = []
    destToMovesMap[dest].append(m)

  # cut supports first
  for dest in destToMovesMap.keys():
    supports = [m for m in destToMovesMap[dest] if m.isSupporting and not m.moveFailed]
    actualMoves = [m for m in destToMovesMap[dest] if not m.isSupporting]
    maxPower = 0
    for m in actualMoves:
      movesSupportingThisOne = [x for x in supports if x.origin == m.origin]
      m.numSupports = len(movesSupportingThisOne)
      if m.numSupports > maxPower:
        maxPower = m.numSupports

    tiedMoves = [m for m in actualMoves if m.numSupports == maxPower]
    print tiedMoves[0].s()


# print [(x.origin, x.dest) for x in allMoveList]
# playGame()
for i in range(1):
  playGame()
