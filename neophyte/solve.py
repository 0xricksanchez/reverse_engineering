import angr
import claripy

# Open up an angr project on this file
project = angr.Project("./neophyte")

# Using claripy to generate a symbolic buffer.
# We know this needs to be 41 bytes in length (our input)
arg1 = claripy.BVS('arg1', 8*41)

# Create the argv array which is just the binary name and our arg
args = ["./neophyte", arg1]

'''
 Initializes an entry state starting at the address of the program entry point
 We simply pass it the same kind of argument vector that would be passed to the
 program, in execv() for example.
'''
state = project.factory.entry_state(args=args)

'''
 Create a new SimulationManager from the entry state
'''
pg = project.factory.simgr(state)

# Explore. Find the puts("yes") location. Avoid the locations where we know we
# have failed (such as setting the success variable to False)
pg.explore(find=0x804930d, avoid=(0x804931b, 0x80492ad))

# Print out our winning flag.
print("Flag: {0}".format(pg.found[0].state.se.eval(arg1, cast_to=str)))
