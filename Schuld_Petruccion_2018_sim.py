# File: Schuld_Petruccion_2018_sim.py
#
# Qiskit Quantum Machine Learning Example (simulation version)
# from Section 1.2.3 in Ref. [Schuld & Petruccione, 2018]
# Note: In [Schuld & Petruccione, 2018] there is an error p. 16, 3rd equation.
#
# Author: Michel Barbeau, Carleton University
# Version: April 22, 2019
#
# Run with: (where "quantum" is the name of your Python quantum environment)
#    source activate quantum
#    pythonw Schuld_Petruccion_2018_sim.py
#
# Init of Qiskit environment
#
# Qiskit numbers qubits right to left: q3,q2,q1,q0
# Corresponding Python qubits are: q[3],q[2],q[1],q[0]
#
import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute
import math
import numpy
#
# State and circuit creation
#
# Create a 4 qubit quantum register
q = QuantumRegister(4)
# Create a classical register for measurements
c = ClassicalRegister(4)
# Create a quantum circuit with innput q & output c
circ = QuantumCircuit(q,c)
# Initialize the register content
v = numpy.zeros(16)
v[ 1] = 0.920843009649141/2 # |0001>
v[ 3] = 0.389933522001265/2 # |0011>
v[ 4] = 0.141001339519088/2 # |0100>
v[ 6] = 0.990009405134023/2 # |0110>
v[ 9] = 0.866019052628739/2 # |1001>
v[11] = 0.500011000363013/2 # |1011>
v[12] = 0.866019052628739/2 # |1100>
v[14] = 0.500011000363013/2 # |1110>
circ.initialize(v, q)
# Add a H gate on qubit 3 (left most)
circ.h(q[3])
# Measure leftmost qubit
circ.measure(q[3], c[3])
# Measure leftmost qubit
circ.measure(q[0], c[0])
#
# Simulation with OpenQASM backend
#
# Import Aer
from qiskit import BasicAer
# Use Aer's qasm_simulator
backend_sim = BasicAer.get_backend('qasm_simulator')
# Execute the circuit on the qasm (local) simulator
shots=1024*10
job = execute(circ, backend_sim, shots=shots)
#
# Print the results 
#
result = job.result()
counts = result.get_counts(circ)
# Calculate probability of label 1
# q4=0 & q0=1 over q4=0 & (q0=0 or q0=1)
p1 = counts.get('0001',0) / \
     (counts.get('0000',0)+counts.get('0001')) 
print("Probability of label 0 (1) is %.3f (%.3f)" % ((1-p1),p1))
