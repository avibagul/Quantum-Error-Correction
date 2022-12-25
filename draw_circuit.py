from qiskit import *


def draw_qc(code_qubit):

    ## Ancilla Qubit
    link_qubit = code_qubit - 1

    code_qregisters = []  # List of quantum code registers
    link_qregisters = []  # List of quantum link registers
    code_cregisters = ClassicalRegister(code_qubit, 'code bits (syndrome)')  # List of classical quantum registers
    link_cregisters = ClassicalRegister(link_qubit, 'ancilla bits (syndrome)') # List of classical link registers
    
    ### appending code register list with code qubits and custom names
    for x in range(code_qubit):

        code_qregisters.append(QuantumRegister(1, 'c'+ str(x)))
    
    ### appending link register list with code qubits and custom names
    for y in range(link_qubit):

        link_qregisters.append(QuantumRegister(1, 'a'+ str(y)))
    
    ### appending parameter list with QuantumCircuit parameters
    param = []
    for x in range(code_qubit):
        param.append(code_qregisters[x])
        
        if x != code_qubit-1:
            param.append(link_qregisters[x])
    
    bparam = param.copy()
    
    param.append(code_cregisters)
    param.append(link_cregisters)

    qc = QuantumCircuit(*param)

    ### Adding X Gate to code qubits
    for x in range(code_qubit):
        qc.x(code_qregisters[x])
    
    qc.barrier(*bparam)
    
    for x in range(link_qubit):
        for y in range(x, x+2):
            qc.cx(code_qregisters[y], link_qregisters[x])
    
    qc.barrier(*bparam)
    
    #qc.measure(c0, cb[0])
    
    for x in range(code_qubit):
        qc.measure(code_qregisters[x], code_cregisters[x])
    
    for x in range(link_qubit):
        qc.measure(link_qregisters[x], link_cregisters[x])

    return qc