import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def create_dss_system():
    # === 1. Inputs ===
    latency_value = ctrl.Antecedent(np.linspace(0, 1, 100), 'latency_value')
    p95_value = ctrl.Antecedent(np.linspace(0, 1, 100), 'p95_value')
    tps_value = ctrl.Antecedent(np.linspace(0, 1, 100), 'tps_value')
    energy_value = ctrl.Antecedent(np.linspace(0, 1, 100), 'energy_value')

    priority_latency = ctrl.Antecedent(np.linspace(0, 1, 100), 'priority_latency')
    priority_p95 = ctrl.Antecedent(np.linspace(0, 1, 100), 'priority_p95')
    priority_tps = ctrl.Antecedent(np.linspace(0, 1, 100), 'priority_tps')
    priority_energy = ctrl.Antecedent(np.linspace(0, 1, 100), 'priority_energy')

    # === 2. Output ===
    suitability = ctrl.Consequent(np.linspace(0, 1, 100), 'suitability')

    # === 3. Membership functions ===
    for var in [latency_value, p95_value, tps_value, energy_value,
                priority_latency, priority_p95, priority_tps, priority_energy]:
        var['low'] = fuzz.trimf(var.universe, [0.0, 0.0, 0.35])
        var['medium'] = fuzz.trimf(var.universe, [0.25, 0.5, 0.75])
        var['high'] = fuzz.trimf(var.universe, [0.65, 1.0, 1.0])

    suitability['poor'] = fuzz.trimf(suitability.universe, [0.0, 0.1, 0.3])
    suitability['fair'] = fuzz.trimf(suitability.universe, [0.2, 0.45, 0.7])
    suitability['good'] = fuzz.trimf(suitability.universe, [0.6, 0.75, 0.9])
    suitability['excellent'] = fuzz.trimf(suitability.universe, [0.85, 0.95, 1.0])

    # === 4. Rule generator ===
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
    rules += generate_metric_priority_rules(latency_value, priority_latency)
    rules += generate_metric_priority_rules(p95_value, priority_p95)
    rules += generate_metric_priority_rules(tps_value, priority_tps)
    rules += generate_metric_priority_rules(energy_value, priority_energy)

    # === 5. Ödül: TPS + Latency yüksekse + kullanıcı önemsiyorsa → good
    rules.append(ctrl.Rule(
        tps_value['high'] & latency_value['high'] &
        (priority_tps['high'] | priority_latency['high']),
        suitability['good']
    ))

    # === 6. Ceza: TPS ve Energy düşük + kullanıcı önemsiyorsa → poor
    rules.append(ctrl.Rule(
        tps_value['low'] & priority_tps['high'] &
        energy_value['low'] & priority_energy['high'],
        suitability['poor']
    ))

    # === 7. Tam uyum varsa → excellent
    rules.append(ctrl.Rule(
        latency_value['high'] & p95_value['high'] & tps_value['high'] & energy_value['high'] &
        priority_latency['high'] & priority_p95['high'] & priority_tps['high'] & priority_energy['high'],
        suitability['excellent']
    ))

    # === 8. Tam kötü durumda bile biraz pozitiflik: minimum fair
    rules.append(ctrl.Rule(
        latency_value['low'] & p95_value['low'] & tps_value['low'] & energy_value['low'] &
        priority_latency['low'] & priority_p95['low'] & priority_tps['low'] & priority_energy['low'],
        suitability['fair']
    ))

    # === 9. Build and return ===
    system = ctrl.ControlSystem(rules)
    return ctrl.ControlSystemSimulation(system)
