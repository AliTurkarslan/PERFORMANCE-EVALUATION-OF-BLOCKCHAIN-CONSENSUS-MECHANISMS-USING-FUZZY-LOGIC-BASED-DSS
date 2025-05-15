import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz

# Define universe
x = np.linspace(0, 1, 100)

# Create a figure with subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 8))

# --- TPS Membership ---
axs[0, 0].plot(x, fuzz.trimf(x, [0.0, 0.0, 0.3]), label='Low')
axs[0, 0].plot(x, fuzz.trimf(x, [0.2, 0.5, 0.8]), label='Medium')
axs[0, 0].plot(x, fuzz.trimf(x, [0.7, 1.0, 1.0]), label='High')
axs[0, 0].set_title('TPS Membership')
axs[0, 0].legend()
axs[0, 0].set_xlabel("Normalized Value")
axs[0, 0].set_ylabel("Membership")

# --- Latency Membership ---
axs[0, 1].plot(x, fuzz.trimf(x, [0.0, 0.0, 0.3]), label='Low')
axs[0, 1].plot(x, fuzz.trimf(x, [0.2, 0.5, 0.8]), label='Medium')
axs[0, 1].plot(x, fuzz.trimf(x, [0.7, 1.0, 1.0]), label='High')
axs[0, 1].set_title('Latency Membership')
axs[0, 1].legend()
axs[0, 1].set_xlabel("Normalized Value")
axs[0, 1].set_ylabel("Membership")

# --- User Priority Membership ---
axs[1, 0].plot(x, fuzz.trimf(x, [0.0, 0.0, 0.3]), label='Low')
axs[1, 0].plot(x, fuzz.trimf(x, [0.2, 0.5, 0.8]), label='Medium')
axs[1, 0].plot(x, fuzz.trimf(x, [0.7, 1.0, 1.0]), label='High')
axs[1, 0].set_title('User Priority Membership')
axs[1, 0].legend()
axs[1, 0].set_xlabel("Normalized Value")
axs[1, 0].set_ylabel("Membership")

# --- Suitability Output Membership ---
axs[1, 1].plot(x, fuzz.trimf(x, [0.0, 0.0, 0.3]), label='Poor')
axs[1, 1].plot(x, fuzz.trimf(x, [0.2, 0.4, 0.6]), label='Fair')
axs[1, 1].plot(x, fuzz.trimf(x, [0.5, 0.7, 0.9]), label='Good')
axs[1, 1].plot(x, fuzz.trimf(x, [0.8, 1.0, 1.0]), label='Excellent')
axs[1, 1].set_title('Suitability Score Membership')
axs[1, 1].legend()
axs[1, 1].set_xlabel("Score (0-1)")
axs[1, 1].set_ylabel("Membership")

plt.tight_layout()
plt.savefig("fuzzy_dss_membership_functions.png")
plt.show()
