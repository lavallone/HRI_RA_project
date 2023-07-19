from unified_planning.shortcuts import *

Cell = UserType('Cell')
Bin = UserType('Bin')
Agent = UserType('Agent')

## FLUENTS definition
agent_at = unified_planning.model.Fluent('agent_at', BoolType(), robot=Agent, position=Cell)
is_agent = unified_planning.model.Fluent('is_agent', BoolType(), robot=Agent)
bin_at = unified_planning.model.Fluent('bin_at', BoolType(), bin=Bin, position=Cell)
is_bin = unified_planning.model.Fluent('is_bin', BoolType(), bin=Bin)
adj = unified_planning.model.Fluent('adj', BoolType(), from_position=Cell, to_position=Cell)
throw = unified_planning.model.Fluent('throw', BoolType(), bin=Bin)
# numerical fluents for the level of the bins
level = unified_planning.model.Fluent("level", IntType(0,3), bin=Bin)

## ACTIONS definition
# move
move = unified_planning.model.InstantaneousAction('move', robot=Agent, from_position=Cell, to_position=Cell)
robot = move.parameter('robot')
from_position = move.parameter('from_position')
to_position = move.parameter('to_position')
move.add_precondition(adj(from_position, to_position))
move.add_precondition(is_agent(robot))
move.add_precondition(agent_at(robot, from_position))
move.add_effect(agent_at(robot, from_position), False)
move.add_effect(agent_at(robot, to_position), True)

# throw
throw_bin = unified_planning.model.InstantaneousAction('throw', robot=Agent, bin=Bin, position=Cell)
robot = move.parameter('robot')
bin_ = move.parameter('bin')
position = move.parameter('position')
throw_bin.add_precondition(is_agent(robot))
throw_bin.add_precondition(agent_at(robot, position))
throw_bin.add_precondition(is_agent(bin_))
throw_bin.add_precondition(agent_at(bin_, position))
# how to define the inequality of the level?
throw_bin.add_precondition(LT(level(bin_), 3))
throw_bin.add_effect(throw(bin_), True)

## PROBLEM definition
problem = unified_planning.model.Problem('school')
problem.add_fluent(agent_at)
problem.add_fluent(is_agent)
problem.add_fluent(bin_at)
problem.add_fluent(is_bin)
problem.add_fluent(adj)
problem.add_fluent(throw)
problem.add_fluent(level)
problem.add_action(move)
problem.add_action(throw_bin)


# define OBJECTS
list_letter = [('A', 30),('B', 36),('C', 20),('D', 25),('E', 40),('F', 24),('G', 18),('H', 24),('I', 108)]
cells = []
for elem in list_letter:
  for i in range(elem[1]):
    cells.append(unified_planning.model.Object(f'{elem[0]}{i+1}', Cell))

robot = unified_planning.model.Object('robot', Agent)
bin1 = unified_planning.model.Object('bin1', Bin)
bin2 = unified_planning.model.Object('bin2', Bin)
bin3 = unified_planning.model.Object('bin3', Bin)


problem.add_objects(cells)

problem.add_object(robot)
problem.add_object(bin1)
problem.add_object(bin2)
problem.add_object(bin3)

