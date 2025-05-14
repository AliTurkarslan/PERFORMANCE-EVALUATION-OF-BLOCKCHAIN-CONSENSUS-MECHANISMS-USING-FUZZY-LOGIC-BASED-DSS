"""
define_fuzzy_dss.py
Defines the fuzzy decision support system for evaluating consensus algorithm suitability
based on normalized performance metrics and user-defined priorities.
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def create_dss_system():
    # === 1. Define input variables (normalized performance metrics) ===
    latency_value = ctrl.Antecedent(np.linspace(0, 1, 100), 'latency_value')
    p95_value = ctrl.Antecedent(np.linspace(0, 1, 100), 'p95_value')
    tps_value = ctrl.Antecedent(np.linspace(0, 1, 100), 'tps_value')
    energy_value = ctrl.Antecedent(np.linspace(0, 1, 100), 'energy_value')

    # === 2. Define input variables (user-defined priorities) ===
    priority_latency = ctrl.Antecedent(np.linspace(0, 1, 100), 'priority_latency')
    priority_p95 = ctrl.Antecedent(np.linspace(0, 1, 100), 'priority_p95')
    priority_tps = ctrl.Antecedent(np.linspace(0, 1, 100), 'priority_tps')
    priority_energy = ctrl.Antecedent(np.linspace(0, 1, 100), 'priority_energy')

    # === 3. Define output variable ===
    suitability = ctrl.Consequent(np.linspace(0, 1, 100), 'suitability')

    # === 4. Membership functions for inputs ===
    for var in [latency_value, p95_value, tps_value, energy_value,
                priority_latency, priority_p95, priority_tps, priority_energy]:
        var['low'] = fuzz.trimf(var.universe, [0.0, 0.0, 0.35])
        var['medium'] = fuzz.trimf(var.universe, [0.25, 0.5, 0.75])
        var['high'] = fuzz.trimf(var.universe, [0.65, 1.0, 1.0])

    # === 5. Membership functions for output ===
    suitability['poor'] = fuzz.trimf(suitability.universe, [0.0, 0.1, 0.3])
    suitability['fair'] = fuzz.trimf(suitability.universe, [0.2, 0.45, 0.7])
    suitability['good'] = fuzz.trimf(suitability.universe, [0.6, 0.75, 0.9])
    suitability['excellent'] = fuzz.trimf(suitability.universe, [0.85, 0.95, 1.0])

    # === 6. Rule generator: metric × priority interactions ===
    def generate_metric_priority_rules(metric, priority):
        return [
            ctrl.Rule(metric['high'] & priority['high'], suitability['excellent']),
            ctrl.Rule(metric['medium'] & priority['high'], suitability['good']),
            ctrl.Rule(metric['low'] & priority['high'], suitability['poor']),

            ctrl.Rule(metric['high'] & priority['medium'], suitability['good']),
            ctrl.Rule(metric['medium'] & priority['medium'], suitability['fair']),
            ctrl.Rule(metric['low'] & priority['medium'], suitability['poor']),

            ctrl.Rule(metric['high'] & priority['low'], suitability['fair']),
            ctrl.Rule(metric['medium'] & priority['low'], suitability['fair']),
            ctrl.Rule(metric['low'] & priority['low'], suitability['poor']),
        ]

    rules = []

    # === 7. Add rules for each metric and its priority ===
    rules += generate_metric_priority_rules(latency_value, priority_latency)
    rules += generate_metric_priority_rules(p95_value, priority_p95)
    rules += generate_metric_priority_rules(tps_value, priority_tps)
    rules += generate_metric_priority_rules(energy_value, priority_energy)

    # === 8. Reward synergy: high TPS + high latency + high priority → good
    rules.append(ctrl.Rule(
        tps_value['high'] & latency_value['high'] &
        (priority_tps['high'] | priority_latency['high']),
        suitability['good']
    ))

    # === 9. Penalize: low TPS and energy + high priority → poor
    rules.append(ctrl.Rule(
        tps_value['low'] & priority_tps['high'] &
        energy_value['low'] & priority_energy['high'],
        suitability['poor']
    ))

    # === 10. Maximum alignment → excellent
    rules.append(ctrl.Rule(
        latency_value['high'] & p95_value['high'] & tps_value['high'] & energy_value['high'] &
        priority_latency['high'] & priority_p95['high'] & priority_tps['high'] & priority_energy['high'],
        suitability['excellent']
    ))

    # === 11. Minimum alignment → fair (not poor)
    rules.append(ctrl.Rule(
        latency_value['low'] & p95_value['low'] & tps_value['low'] & energy_value['low'] &
        priority_latency['low'] & priority_p95['low'] & priority_tps['low'] & priority_energy['low'],
        suitability['fair']
    ))

    # === 12. Compile and return the fuzzy system ===
    system = ctrl.ControlSystem(rules)
    return ctrl.ControlSystemSimulation(system)
