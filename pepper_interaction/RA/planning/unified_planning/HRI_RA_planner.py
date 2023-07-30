# remember to run: 
# pip install -r requirements.txt
from unified_planning.shortcuts import *

global coords2states_bins, states2coords_bins, coords2states_doors
coords2states_bins = {(16,1) : "C9", (18,27): "E39", (2,28) : "H12", (18,7) : "D22", (18,26) : "E38", (7,28) : "G12", (15,12) : "I85", (1,20) : "I3",  (1,1) : "A1", (11,6) : "B30", (12,28) : "F18"}
states2coords_bins = {'C9': (16, 1), 'E39': (18, 27), 'H12': (2, 28), 'D22': (18, 7), 'E38': (18, 26), 'G12': (7, 28), 'I85': (15, 12), 'I3': (1, 20), 'A1': (1, 1), 'B30': (11, 6), 'F18': (12, 28)}
coords2states_doors = {(13,3) : ["B33", "C3"], (2,7) : ["A12", "I5"], (9,7) : ["B18", "I33"], (13,9) : ["D4", "I56"], (14,21) : ["E3", "I78"], (12,22) : ["F13", "I68"], (7,22) : ["G7", "I28"], (2,22) : ["H7", "I8"], (5,26) : ["G4", "H22"]}

def plan(garbage_type, bins_fullness, random_doors):
	"""
	function used to plan the best moves to reach the nearest bin of a particular garbage type. 
	The inputs are:
		- garbage_type --> {plastic, paper, trash, compost}
		- bins_fullness: describes the current situation of fullness of all the bins in the school. So it tells us which bins
		are free and which are not.
		- random_doors: a list containing the doors (three actually) that are currently closed.
		
	Since the LOCATION of each bin or door of our custom grid world is described in different ways across the project, 
	we need some utils functions to overcome this problem. 
	In summary, we have locations described as COORDINATES of a matrix, CELLS from 0 to 599 for computing RL algorithms and 
	STATES for performing PDDL plans.
 
	The outputs are:
		- ris_plan: sequence of STATES to reach the goal, if there isn't such plan its value is 'None'
  					(we need a format to be able to perform the mapping STATES --> CELLS)
		- bins_fullness (updated): is the bin into which we have to throw garbage in (is used to update 'bins_fullness')
	"""
	Cell = UserType('Cell')
	Bin = UserType('Bin')
	Agent = UserType('Agent')

	## FLUENTS definition
	agent_at = unified_planning.model.Fluent('agent_at', BoolType(), robot=Agent, position=Cell)
	is_agent = unified_planning.model.Fluent('is_agent', BoolType(), robot=Agent)
	bin_at = unified_planning.model.Fluent('bin_at', BoolType(), bin=Bin, position=Cell)
	is_bin = unified_planning.model.Fluent('is_bin', BoolType(), bin=Bin)
	adj = unified_planning.model.Fluent('adj', BoolType(), from_position=Cell, to_position=Cell)
	throw_in_bin = unified_planning.model.Fluent('throw_in_bin', BoolType(), bin=Bin)
	level = unified_planning.model.Fluent("level", IntType(0,3), bin=Bin) # numerical fluents

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
	recycle = unified_planning.model.InstantaneousAction('recycle', robot=Agent, bin=Bin, position=Cell)
	robot = recycle.parameter('robot')
	bin_ = recycle.parameter('bin')
	position = recycle.parameter('position')
	recycle.add_precondition(is_agent(robot))
	recycle.add_precondition(agent_at(robot, position))
	recycle.add_precondition(is_bin(bin_))
	recycle.add_precondition(bin_at(bin_, position))
	recycle.add_precondition(LT(level(bin_), 3))  # definition of level inequality
	recycle.add_effect(throw_in_bin(bin_), True)

	## PROBLEM definition
	problem = unified_planning.model.Problem('school')
	problem.add_fluent(agent_at, default_initial_value=False)
	problem.add_fluent(is_agent, default_initial_value=False)
	problem.add_fluent(bin_at, default_initial_value=False)
	problem.add_fluent(is_bin, default_initial_value=False)
	problem.add_fluent(adj, default_initial_value=False)
	problem.add_fluent(throw_in_bin, default_initial_value=False)
	problem.add_fluent(level, default_initial_value=False)
	problem.add_action(move)
	problem.add_action(recycle)

	# instantiate OBJECTS
	robot = unified_planning.model.Object('robot', Agent)
	bin1 = unified_planning.model.Object('bin1', Bin)
	bin2 = unified_planning.model.Object('bin2', Bin)
	bin3 = unified_planning.model.Object('bin3', Bin)
	problem.add_object(robot)
	problem.add_object(bin1)
	problem.add_object(bin2)
	problem.add_object(bin3)

	room_list = [('A', 30),('B', 36),('C', 20),('D', 25),('E', 40),('F', 24),('G', 18),('H', 24),('I', 108)]
	cells, name2idx = [], {}
	i=0
	for elem in room_list:
		for j in range(elem[1]):
			cell_name = f'{elem[0]}{j+1}'
			cells.append(unified_planning.model.Object(cell_name, Cell))
			name2idx[cell_name] = i
			i+=1
	problem.add_objects(cells)

	# instantiate FLUENTS
	problem.set_initial_value(is_agent(robot), True)   
	problem.set_initial_value(agent_at(robot, cells[name2idx["I90"]]), True)
	problem.set_initial_value(is_bin(bin1), True)
	problem.set_initial_value(is_bin(bin2), True)
	problem.set_initial_value(is_bin(bin3), True)
	if garbage_type == "plastic":
		problem.set_initial_value(bin_at(bin1, cells[name2idx["C9"]]), True)
		problem.set_initial_value(bin_at(bin2, cells[name2idx["E39"]]), True)
		problem.set_initial_value(bin_at(bin3, cells[name2idx["H12"]]), True)
		problem.set_initial_value(level(bin1), bins_fullness[str(states2coords_bins["C9"])])
		problem.set_initial_value(level(bin2), bins_fullness[str(states2coords_bins["E39"])])
		problem.set_initial_value(level(bin3), bins_fullness[str(states2coords_bins["H12"])])
	elif garbage_type == "paper":
		problem.set_initial_value(bin_at(bin1, cells[name2idx["D22"]]), True)
		problem.set_initial_value(bin_at(bin2, cells[name2idx["E38"]]), True)
		problem.set_initial_value(bin_at(bin3, cells[name2idx["G12"]]), True)
		problem.set_initial_value(level(bin1), bins_fullness[str(states2coords_bins["D22"])])
		problem.set_initial_value(level(bin2), bins_fullness[str(states2coords_bins["E38"])])
		problem.set_initial_value(level(bin3), bins_fullness[str(states2coords_bins["G12"])])
	elif garbage_type == "compost":
		problem.set_initial_value(bin_at(bin1, cells[name2idx["A1"]]), True)
		problem.set_initial_value(bin_at(bin2, cells[name2idx["B30"]]), True)
		problem.set_initial_value(bin_at(bin3, cells[name2idx["F18"]]), True)
		problem.set_initial_value(level(bin1), bins_fullness[str(states2coords_bins["A1"])])
		problem.set_initial_value(level(bin2), bins_fullness[str(states2coords_bins["B30"])])
		problem.set_initial_value(level(bin3), bins_fullness[str(states2coords_bins["F18"])])
	elif garbage_type == "trash":
		problem.set_initial_value(bin_at(bin1, cells[name2idx["I85"]]), True)
		problem.set_initial_value(bin_at(bin2, cells[name2idx["I3"]]), True)
		problem.set_initial_value(level(bin1), bins_fullness[str(states2coords_bins["I85"])])
		problem.set_initial_value(level(bin2), bins_fullness[str(states2coords_bins["I3"])])
	else:
		print(f"no garbage type named {garbage_type}!!!")
		return
	
	# for 'adj' fluents was a bit more tricky and time-consuming...
	f = open("planning/PDDL/adj_fluents.txt", "r")
	l = (f.read()).split(")")
	for i in range(len(l)):
		l[i] = l[i].replace("(", "")
		l[i] = l[i].replace("\n", "")
	adj_obj_list = []
	for e in l[:-1]:
		if len(e.split(" "))==3:
			_, obj1, obj2 = e.split(" ")
		else:
			obj1, obj2 = e.split(" ")
		adj_obj_list.append((obj1, obj2))
	for c1,c2 in adj_obj_list:
		problem.set_initial_value(adj(cells[name2idx[c1]], cells[name2idx[c2]]), True)
	
	# 9 doors in total
	problem.set_initial_value(adj(cells[name2idx["A12"]], cells[name2idx["I5"]]), True)
	problem.set_initial_value(adj(cells[name2idx["I5"]], cells[name2idx["A12"]]), True)
	problem.set_initial_value(adj(cells[name2idx["B18"]], cells[name2idx["I33"]]), True)
	problem.set_initial_value(adj(cells[name2idx["I33"]], cells[name2idx["B18"]]), True)
	problem.set_initial_value(adj(cells[name2idx["B33"]], cells[name2idx["C3"]]), True)
	problem.set_initial_value(adj(cells[name2idx["C3"]], cells[name2idx["B33"]]), True)
	problem.set_initial_value(adj(cells[name2idx["D4"]], cells[name2idx["I56"]]), True)
	problem.set_initial_value(adj(cells[name2idx["I56"]], cells[name2idx["D4"]]), True)
	problem.set_initial_value(adj(cells[name2idx["E3"]], cells[name2idx["I78"]]), True)
	problem.set_initial_value(adj(cells[name2idx["I78"]], cells[name2idx["E3"]]), True)
	problem.set_initial_value(adj(cells[name2idx["F13"]], cells[name2idx["I68"]]), True)
	problem.set_initial_value(adj(cells[name2idx["I68"]], cells[name2idx["F13"]]), True)
	problem.set_initial_value(adj(cells[name2idx["G7"]], cells[name2idx["I28"]]), True)
	problem.set_initial_value(adj(cells[name2idx["I28"]], cells[name2idx["G7"]]), True)
	problem.set_initial_value(adj(cells[name2idx["G4"]], cells[name2idx["H22"]]), True)
	problem.set_initial_value(adj(cells[name2idx["H22"]], cells[name2idx["G4"]]), True)
	problem.set_initial_value(adj(cells[name2idx["H7"]], cells[name2idx["I8"]]), True)
	problem.set_initial_value(adj(cells[name2idx["I8"]], cells[name2idx["H7"]]), True)
	# each time only three random doors are closed!
	for door in random_doors:
		problem.set_initial_value(adj(cells[name2idx[coords2states_doors[door][0]]], cells[name2idx[coords2states_doors[door][1]]]), False)
		problem.set_initial_value(adj(cells[name2idx[coords2states_doors[door][1]]], cells[name2idx[coords2states_doors[door][0]]]), False)

	## set GOAL
	if garbage_type == "plastic":
		problem.add_goal( Or ( And(agent_at(robot, cells[name2idx["C9"]]), bin_at(bin1, cells[name2idx["C9"]]), throw_in_bin(bin1)),
							And(agent_at(robot, cells[name2idx["E39"]]), bin_at(bin2, cells[name2idx["E39"]]), throw_in_bin(bin2)),
							And(agent_at(robot, cells[name2idx["H12"]]), bin_at(bin3, cells[name2idx["H12"]]), throw_in_bin(bin3)) 
						) 
					)
	elif garbage_type == "paper":
		problem.add_goal( Or ( And(agent_at(robot, cells[name2idx["D22"]]), bin_at(bin1, cells[name2idx["D22"]]), throw_in_bin(bin1)),
							And(agent_at(robot, cells[name2idx["E38"]]), bin_at(bin2, cells[name2idx["E38"]]), throw_in_bin(bin2)),
							And(agent_at(robot, cells[name2idx["G12"]]), bin_at(bin3, cells[name2idx["G12"]]), throw_in_bin(bin3)) 
						) 
					)
	elif garbage_type == "compost":
		problem.add_goal( Or ( And(agent_at(robot, cells[name2idx["A1"]]), bin_at(bin1, cells[name2idx["A1"]]), throw_in_bin(bin1)),
							And(agent_at(robot, cells[name2idx["B30"]]), bin_at(bin2, cells[name2idx["B30"]]), throw_in_bin(bin2)),
							And(agent_at(robot, cells[name2idx["F18"]]), bin_at(bin3, cells[name2idx["F18"]]), throw_in_bin(bin3)) 
						) 
					)
	elif garbage_type == "trash":
		problem.add_goal( Or ( And(agent_at(robot, cells[name2idx["I85"]]), bin_at(bin1, cells[name2idx["I85"]]), throw_in_bin(bin1)),
							And(agent_at(robot, cells[name2idx["I3"]]), bin_at(bin2, cells[name2idx["I3"]]), throw_in_bin(bin2))
						) 
					)
 
	## SOLVE the PLAN
	ris_plan, bin_to_update = [], (0,0)
	with OneshotPlanner(problem_kind = problem.kind) as planner:
		result = planner.solve(problem)
		if result.status == up.engines.PlanGenerationResultStatus.SOLVED_SATISFICING:
			plan_split=str(result.plan).split("move(robot, ")[1:]
			goal=(plan_split[-1].split(")")[0]).split(", ")[1]
			for e in plan_split:
				ris_plan.append(e.split(",")[0])
			ris_plan.append(goal)
			# update the bin
			bin_to_update = states2coords_bins[goal]
		else:
			ris_plan = None

	return ris_plan, bin_to_update