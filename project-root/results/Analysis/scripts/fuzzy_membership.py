import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
import os

# Output directory
os.makedirs("results/fuzzy_prepared", exist_ok=True)

# Define universe of discourse
x = np.linspace(0, 1, 100)

# === 1. Latency ===
low_latency = fuzz.trimf(x, [0.0, 0.0, 0.4])
med_latency = fuzz.trimf(x, [0.3, 0.5, 0.7])
high_latency = fuzz.trimf(x, [0.6, 1.0, 1.0])

plt.figure(figsize=(8, 4))
plt.plot(x, low_latency, label="Low")
plt.plot(x, med_latency, label="Medium")
plt.plot(x, high_latency, label="High")
plt.title("Fuzzy Membership - Latency")
plt.xlabel("Normalized Latency")
plt.ylabel("Membership Degree")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("results/fuzzy_prepared/membership_latency.png")
plt.close()

# === 2. P95 Latency ===
low_p95 = fuzz.trimf(x, [0.0, 0.0, 0.4])
med_p95 = fuzz.trimf(x, [0.3, 0.5, 0.7])
high_p95 = fuzz.trimf(x, [0.6, 1.0, 1.0])

plt.figure(figsize=(8, 4))
plt.plot(x, low_p95, label="Low")
plt.plot(x, med_p95, label="Medium")
plt.plot(x, high_p95, label="High")
plt.title("Fuzzy Membership - P95 Latency")
plt.xlabel("Normalized P95 Latency")
plt.ylabel("Membership Degree")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("results/fuzzy_prepared/membership_p95.png")
plt.close()

# === 3. TPS ===
low_tps = fuzz.trimf(x, [0.0, 0.0, 0.4])
med_tps = fuzz.trimf(x, [0.3, 0.5, 0.7])
high_tps = fuzz.trimf(x, [0.6, 1.0, 1.0])

plt.figure(figsize=(8, 4))
plt.plot(x, low_tps, label="Low")
plt.plot(x, med_tps, label="Medium")
plt.plot(x, high_tps, label="High")
plt.title("Fuzzy Membership - Realized TPS")
plt.xlabel("Normalized TPS")
plt.ylabel("Membership Degree")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("results/fuzzy_prepared/membership_tps.png")
plt.close()

# === 4. Energy per Tx ===
efficient = fuzz.trimf(x, [0.0, 0.0, 0.4])
moderate = fuzz.trimf(x, [0.3, 0.5, 0.7])
inefficient = fuzz.trimf(x, [0.6, 1.0, 1.0])

plt.figure(figsize=(8, 4))
plt.plot(x, efficient, label="Efficient")
plt.plot(x, moderate, label="Moderate")
plt.plot(x, inefficient, label="Inefficient")
plt.title("Fuzzy Membership - Energy per Transaction")
plt.xlabel("Normalized Energy")
plt.ylabel("Membership Degree")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("results/fuzzy_prepared/membership_energy.png")
plt.close()

print("✅ Membership function plots saved.")
