# Quantum Machine Learning Example: Drone Formation Transition 
#
# Author: Michel Barbeau, Carleton University
# Version: April 23, 2019
#
# Run with: (where "quantum" is the name of your Python quantum environment)
#    source activate quantum
#    pythonw mtion_transition_sim.py
#
# Sample execution:
#    pythonw formation_transition_sim.py 
#    Probability of label 0 (1) is 0.466 (0.534)
#
# Init of Qiskit environment
#
# Qiskit numbers qubits right to left: q4,q3,q2,q1,q0
# Corresponding Python qubits are: q[4],q[3],q[2],q[1],q[0]
#
import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute
import math
import numpy
#
# State and circuit creation
#
# Create a 5 qubit register
q = QuantumRegister(5)
# Create classical register for measurements
c = ClassicalRegister(2)
# Create a quantum circuit acting on q and c 
circ = QuantumCircuit(q,c)
# Initialize the register content
v = numpy.zeros(32)
v[ 0] = 0.854599108706791/2 # |0>|0>|00>|0>
v[ 2] = 0.519288323956507/2 # |0>|0>|01>|0>
v[ 9] = 0.707106781186547/2 # |0>|1>|00>|1>
v[11] = 0.707106781186547/2 # |0>|1>|01>|1>
v[16] = 0.669571630148232/2 # |1>|0>|00>|0>
v[18] = 0.742747488787838/2 # |1>|0>|01>|0>
v[25] = 0.669571630148232/2 # |1>|1>|00>|1>
v[27] = 0.742747488787838/2 # |1>|1>|01>|1>
circ.initialize(v, q)
# Add a H gate on qubit 4 (leftmost)
circ.h(q[4])
# Measure leftmost qubit
circ.measure(q[4], c[1])
# Measure rightmost qubit
circ.measure(q[0], c[0])
#
# Simulation OpenQASM backend
#
# Import Aer
from qiskit import BasicAer
# Use Aer's qasm_simulator
backend_sim = BasicAer.get_backend('qasm_simulator')
# Execute the circuit on the qasm (local) simulator
shots=1024
job = execute(circ, backend_sim, shots=shots)
#
# Print the results 
#
result = job.result()
n_qubits_qureg = q.size
counts = result.get_counts(circ)
p0 = counts.get('00',0) / (counts.get('00',0)+counts.get('01',0))
print("Probability of label 0 (1) is %.3f (%.3f)" % (p0, (1-p0)))
