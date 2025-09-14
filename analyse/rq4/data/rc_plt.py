import matplotlib.pyplot as plt
import numpy as np
import json

with open('/Users/st/Desktop/linux/analyse/rq3/data/bugzilla_rc_sub.json', 'r') as f:
    bugzilla = json.load(f)

with open('/Users/st/Desktop/linux/analyse/rq3/data/syz_rc_sub.json', 'r') as f:
    syzbot = json.load(f)


# Get the union of all keys
categories = sorted(set(bugzilla.keys()) | set(syzbot.keys()))
bugzilla_vals = [bugzilla.get(cat, 0) for cat in categories]
syzbot_vals = [syzbot.get(cat, 0) for cat in categories]

totals = [b + s for b, s in zip(bugzilla_vals, syzbot_vals)]
total_sum = sum(totals)
percentages = [(t / total_sum) * 100 for t in totals]

# Sort by total descending
sorted_indices = np.argsort(totals)[::-1]
categories = [categories[i] for i in sorted_indices]
bugzilla_vals = [bugzilla_vals[i] for i in sorted_indices]
syzbot_vals = [syzbot_vals[i] for i in sorted_indices]
percentages = [percentages[i] for i in sorted_indices]


fig, ax = plt.subplots(figsize=(10, 6))
y_pos = np.arange(len(categories))

# Swap order: syzbot first, then Bugzilla
ax.barh(y_pos, syzbot_vals, color="#C4E1A4", label="syzbot")
ax.barh(y_pos, bugzilla_vals, left=syzbot_vals, color="#7BC8C8", label="Bugzilla")

# Add counts
for i, (s, b) in enumerate(zip(syzbot_vals, bugzilla_vals)):
    if s > 0:
        ax.text(s / 2, i, str(s), va='center', ha='center', fontsize=9, fontweight='bold')
    if b > 0:
        ax.text(s + b / 2, i, str(b), va='center', ha='center', fontsize=9, fontweight='bold')

# Add percentage labels
for i, (s, b, pct) in enumerate(zip(syzbot_vals, bugzilla_vals, percentages)):
    ax.text(s + b + 1, i, f"{pct:.2f}%", va='center', ha='left', fontsize=9)

ax.set_yticks(y_pos)
ax.set_yticklabels(categories, fontsize=10, fontweight='bold')
ax.invert_yaxis()
ax.set_xlabel("Number of False-Positive Reports")
ax.legend()

plt.title("False-Positive Bug Reports Distribution by Components", fontsize=12, fontweight='bold')
plt.tight_layout()
# plt.show()
plt.savefig('/Users/st/Desktop/linux/analyse/rq3/plt/root_cause.png', dpi=300)
plt.close(fig)