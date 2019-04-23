# File: Schuld_Petruccion_2018_dev.py
#
# Qiskit Quantum Machine Learning Example (device version)
# from Section 1.2.3 in Ref. [Schuld & Petruccione, 2018]
# Note: In [Schuld & Petruccione, 2018] there is an error p. 16, 3rd equation.
#
# Author: Michel Barbeau, Carleton University
# Version: April 23, 2019
#
# Run with: (where "quantum" is the name of your Python quantum environment)
#    source activate quantum
#    pythonw Schuld_Petruccion_2018_dev.py
#
# Sample execution:
#   pythonw Schuld_Petruccion_2018_dev.py 
#   Available backends:
#   The best backend is ibmq_16_melbourne
#   Job Status: job has successfully run
#   Probability of label 0 (1) is 0.418 (0.582)
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
c = ClassicalRegister(2)
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
# Add a H gate on qubit 3 (leftmost)
circ.h(q[3])
# Measure leftmost qubit
circ.measure(q[3], c[1])
# Measure rightmost qubit
circ.measure(q[0], c[0])
circ.draw(output='mpl')
#
# Running on IBM Q
#
from qiskit import IBMQ
# Load credentials
IBMQ.load_accounts()
# List available devices
print("Available backends:")
IBMQ.backends()
# Choose device with least busy queue
from qiskit.providers.ibmq import least_busy
large_enough_devices = IBMQ.backends(filters=lambda x: x.configuration().n_qubits > 3 and not x.configuration().simulator)
backend = least_busy(large_enough_devices)
print("The best backend is " + backend.name())
# Execute the circuit
from qiskit.tools.monitor import job_monitor
# Number of shots to run the program
shots = 1024
# Maximum number of credits to spend on executions
max_credits = 3
job = execute(circ, backend=backend, shots=shots, max_credits=max_credits)
job_monitor(job)
# Wait until the job has finished
result = job.result()
#
# Print the results 
#
counts = result.get_counts(circ)
# Calculate probability of label 1
# q4=0 & q0=1 over q4=0 & (q0=0 or q0=1)
p1 = counts.get('01',0) / (counts.get('00',0)+counts.get('01')) 
print("Probability of label 0 (1) is %.3f (%.3f)" % ((1-p1),p1))
