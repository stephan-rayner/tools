
import matplotlib.pyplot as plt
import numpy as np

# Dimensions and their scale endpoints
dimensions = [
    ('Communicating', 'Low-Context', 'High-Context'),
    ('Evaluating', 'Direct Neg. Feedback', 'Indirect Neg. Feedback'),
    ('Persuading', 'Principles-First', 'Applications-First/Holistic'),
    ('Leading', 'Egalitarian', 'Hierarchical'),
    ('Deciding', 'Consensual', 'Top-Down'),
    ('Trusting', 'Task-Based', 'Relationship-Based'),
    ('Disagreeing', 'Confrontational', 'Avoids Confrontation'),
    ('Scheduling', 'Linear-Time', 'Flexible-Time')
]

# Data for each country (0 to 10 scale)
data = {
    'USA':       [1.0, 6.0, 8.5, 4.0, 8.0, 2.0, 4.0, 2.0],
    'Australia': [2.0, 2.5, 7.5, 2.5, 4.5, 2.0, 3.0, 2.5],
    'Canada':    [2.0, 5.0, 8.0, 3.5, 4.5, 3.5, 6.5, 3.0],
    'Singapore': [9.0, 8.0, 10.0, 9.0, 7.5, 8.5, 9.0, 5.5]
}

# Colors and Markers
colors = {'USA': '#1f77b4', 'Australia': '#d62728', 'Canada': '#2ca02c', 'Singapore': '#ff7f0e'}
markers = {'USA': 'o', 'Australia': 's', 'Canada': 'D', 'Singapore': '^'}

# Plot setup
fig, ax = plt.subplots(figsize=(12, 10))

# Reverse dimensions for top-to-bottom layout
y_positions = np.arange(len(dimensions))
y_positions = y_positions[::-1]

# Plot each country
for country, values in data.items():
    ax.plot(values, y_positions, label=country, color=colors[country], marker=markers[country], linewidth=2.5, markersize=10, alpha=0.8)

# Customize Axes
ax.set_yticks(y_positions)
ax.set_yticklabels([d[0] for d in dimensions], fontsize=12, fontweight='bold')
ax.set_xticks([0, 10])
ax.set_xticklabels(['', ''], alpha=0) # Hide default x-labels
ax.set_xlim(-0.5, 10.5)

# Add endpoint labels for each scale
for i, (dim, left, right) in enumerate(dimensions):
    y = y_positions[i]
    # Left label
    ax.text(-0.5, y - 0.25, left, ha='left', va='top', fontsize=10, color='#555555', style='italic')
    # Right label
    ax.text(10.5, y - 0.25, right, ha='right', va='top', fontsize=10, color='#555555', style='italic')
    # Horizontal line for the scale
    ax.axhline(y, color='lightgrey', linestyle='--', linewidth=0.8, zorder=0)

# Grid and Legend
ax.grid(axis='x', color='whitesmoke', linestyle='-', linewidth=1)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=4, frameon=True, fontsize=12)

plt.title('The Culture Map: Multi-Country Comparison', fontsize=18, fontweight='bold', pad=20)
plt.tight_layout()

# Save the image
plt.savefig('culture_map_vertical.png', dpi=300, bbox_inches='tight')
print("Vertical culture map generated as 'culture_map_vertical.png'")
