"""
Step 2 - Define fuzzy input/output variables and rule base
Output: Returns fuzzy control system object
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def create_fuzzy_system():
    # Inputs
    latency = ctrl.Antecedent(np.linspace(0, 1, 100), 'latency')
    p95 = ctrl.Antecedent(np.linspace(0, 1, 100), 'p95')
    tps = ctrl.Antecedent(np.linspace(0, 1, 100), 'tps')
    energy = ctrl.Antecedent(np.linspace(0, 1, 100), 'energy')

    # Output
    performance = ctrl.Consequent(np.linspace(0, 1, 100), 'performance')

    # Membership functions (reversed logic for latency, p95, energy)
    latency['high'] = fuzz.trimf(latency.universe, [0.6, 1.0, 1.0])
    latency['medium'] = fuzz.trimf(latency.universe, [0.3, 0.5, 0.7])
    latency['low'] = fuzz.trimf(latency.universe, [0.0, 0.0, 0.4])

    p95['high'] = fuzz.trimf(p95.universe, [0.6, 1.0, 1.0])
    p95['medium'] = fuzz.trimf(p95.universe, [0.3, 0.5, 0.7])
    p95['low'] = fuzz.trimf(p95.universe, [0.0, 0.0, 0.4])

    tps['low'] = fuzz.trimf(tps.universe, [0.0, 0.0, 0.4])
    tps['medium'] = fuzz.trimf(tps.universe, [0.3, 0.5, 0.7])
    tps['high'] = fuzz.trimf(tps.universe, [0.6, 1.0, 1.0])

    energy['inefficient'] = fuzz.trimf(energy.universe, [0.0, 0.0, 0.4])
    energy['moderate'] = fuzz.trimf(energy.universe, [0.3, 0.5, 0.7])
    energy['efficient'] = fuzz.trimf(energy.universe, [0.6, 1.0, 1.0])

    # Output membership (performance)
    performance['poor'] = fuzz.trimf(performance.universe, [0.0, 0.0, 0.3])
    performance['acceptable'] = fuzz.trimf(performance.universe, [0.2, 0.4, 0.6])
    performance['good'] = fuzz.trimf(performance.universe, [0.5, 0.7, 0.9])
    performance['excellent'] = fuzz.trimf(performance.universe, [0.8, 1.0, 1.0])

    # Rule base (same logic, now matches normalized values properly)
    rule1 = ctrl.Rule(latency['high'] & tps['high'] & energy['efficient'], performance['excellent'])
    rule2 = ctrl.Rule(latency['medium'] & tps['medium'] & energy['efficient'], performance['good'])
    rule3 = ctrl.Rule(latency['low'] | p95['low'], performance['poor'])
    rule4 = ctrl.Rule(tps['low'] & energy['inefficient'], performance['poor'])
    rule5 = ctrl.Rule(latency['high'] & p95['high'] & tps['medium'], performance['acceptable'])
    rule6 = ctrl.Rule(latency['high'] & p95['high'] & tps['low'], performance['acceptable'])


    system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
    return ctrl.ControlSystemSimulation(system)
