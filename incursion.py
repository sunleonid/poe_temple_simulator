import random

'''
     Apex
     0   1
   2   3   4
 5   6   7   8
   9  Ent  10
'''
# Indices of adjacent rooms for Nexus bonus
adj = {
  0: {1, 2, 3},
  1: {0, 3, 4},
  2: {0, 3, 5, 6},
  3: {0, 1, 2, 4, 6, 7},
  4: {1, 3, 7, 8},
  5: {2, 6, 9},
  6: {2, 3, 5, 7, 9},
  7: {3, 4, 6, 8, 10},
  8: {4, 7, 10},
  9: {5, 6},
  10: {7, 8}
}

# (Room, Tier)
rooms = {
  ('Antechamber', 0),
  ('Banquet Hall', 0),
  ('Cellar', 0),
  ('Chasm', 0),
  ('Cloister', 0),
  ('Halls', 0),
  ('Passageways', 0),
  ('Pits', 0),
  ('Tombs', 0),
  ('Tunnels', 0),
  
  ("Armourer's Workshop", 1),
  ('Corruption Chamber', 1),
  ('Explosives Room', 1),
  ('Flame Workshop', 1),
  ("Gemcutter's Workshop", 1),
  ('Guardhouse', 1),
  ('Hatchery', 1),
  ("Jeweller's Workshop", 1),
  ('Lightning Workshop', 1),
  ('Poison Garden', 1),
  ('Pools of Restoration', 1),
  ('Sacrificial Chamber', 1),
  ('Shrine of Empowerment', 1),
  ('Sparring Room', 1),
  ('Splinter Research Lab', 1),
  ('Strongbox Chamber', 1),
  ('Storage Room', 1),
  ('Tempest Generator', 1),
  ('Torment Cells', 1),
  ('Trap Workshop', 1),
  ('Vault', 1),
  ('Workshop', 1)
}

# lv68+ rooms. Uncomment if these need to be included
# rooms |= {("Surveyor's Study", 1), ('Royal Meeting Room', 1)}

# Return tier of the target room. 0 if temple does not contain target
# Strategy: Always upgrade unless the other option has a higher priority.
def generatetemple(target):
  # Initial setup
  priorities = {room: 0 for (room, tier) in rooms if tier == 1}
  priorities['Shrine of Empowerment'] = 1
  priorities[target] = 2

  temple = random.sample(rooms, 11)
  architects = {room for (room, tier) in rooms if tier == 1 and (room, tier) not in temple}

  # 11 Incursions
  for _ in range(11):
    # Pick a room that is not Tier 3
    nont3indices = [i for i in range(11) if temple[i][1] != 3]
    incursionindex = random.choice(nont3indices)
    incursion = temple[incursionindex]
    
    if incursion[1] == 0: # Current incursion is Tier 0
      # Pick two architects, assign room to one, and kill another
      rivals = random.sample(architects, 2)
      architects -= set(rivals)
      chosenarchitect = max(rivals, key = lambda room: priorities[room])
      temple[incursionindex] = (chosenarchitect, 1)
    else: # Current incursion is occupied by an architect
      # Pick one architect and either kill them or have them take over the current room
      rival = random.choice(list(architects))
      architects -= {rival}
      currentarchitect = incursion[0]
      if priorities[currentarchitect] >= priorities[rival]:
        temple[incursionindex] = (currentarchitect, incursion[1] + 1)
      else:
        temple[incursionindex] = (rival, 1)

  # Upgrade rooms adjacent to Temple Nexus
  nexus = ('Shrine of Empowerment', 3)
  if nexus in temple:
    nexusindex = temple.index(nexus)
    for adjindex in adj[nexusindex]:
      room, tier = temple[adjindex]
      if 0 < tier < 3:
        temple[adjindex] = (room, tier + 1)
  
  for (room, tier) in temple:
    if room == target:
      return tier
  
  return 0

total = 1000000
targetcnt = [0, 0, 0, 0]
target = 'Sacrificial Chamber'

for _ in range(total):
  targetcnt[generatetemple(target)] += 1

print('Total number of temples generated: %d' % total)
for tier in (1, 2, 3):
  print('Number of Tier %d %ss: %d (%.2f%%)' % (tier, target, targetcnt[tier], 100. * targetcnt[tier] / total))
