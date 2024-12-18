file_path=('real power amplifier.txt')
lines = ""
import numpy as np
with open(file_path) as f:
  lines = f.readlines()

import re

frequency_list = []
magnitude_list = []
phase_list = []
colour = (255,0,255)

def clean_string(input_string):
    # Use regex to find the numbers
    matches = re.findall(r"[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?", input_string)

    if len(matches) >= 3:
        # Parse the values in the order expected
        first_item = float(matches[0])
        second_item = float(matches[1])  # Strip 'dB' manually
        third_item = float(matches[2])
        return first_item, second_item, third_item
    else:
        raise ValueError("The input string does not contain enough numerical items.")


## Parse text
for line in lines[1::]:
  frequency, magnitude, phase = clean_string(line)

  frequency_list.append(frequency)
  magnitude_list.append(magnitude)
  phase_list.append(phase)


x,y= frequency_list,magnitude_list

from matplotlib import pyplot as plt
# Create the plot
fig, ax1 = plt.subplots(figsize=(10, 7))

# Plot magnitude on the primary y-axis
ax1.plot(frequency_list, magnitude_list, label="Magnitude (dB)", linestyle='-', color='g', linewidth=1)
ax1.set_xscale('log')
ax1.set_xlim(1, 100000)
ax1.set_ylim(0,35)
ax1.set_xlabel("Frequency (Hz)", fontsize=12)
ax1.set_ylabel("Magnitude (dB)", fontsize=12, color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.grid(True, which="both", linestyle="--", linewidth=0.5)

# Create a secondary y-axis for phase
ax2 = ax1.twinx()
ax2.plot(frequency_list, phase_list, label="Phase (degrees)", linestyle=':', color='g', linewidth=1)
ax2.set_ylabel("Phase (degrees)", fontsize=12, color='black')
ax2.set_ylim(-150, 150)  # Phase range: -90 to 90 degrees
ax2.tick_params(axis='y', labelcolor='black')

# Add title and legends
plt.title("Frequency Response", fontsize=14)
fig.tight_layout()  # Adjust layout to prevent overlap

# Combine legends from both axes
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='lower right', fontsize=10)
def annot_max(x,y, ax=None):
    xmax = x[np.argmax(y)]
    ymax = max(y)
    text= "f={:.1f}Hz, mag={:.2f}dB".format(xmax, ymax)
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=90")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
    ax1.annotate(text, xy=(xmax, ymax), xytext=(0.69,0.96), **kw)

def annot_3db_low(x,y, ax=None):
    y_3db_low = max(y)-3
    for a, b in zip(y, x):
        if y_3db_low - 0.0025 < a < y_3db_low + 0.0025:
            if b < 100:
                x_3db = b

    text= "f={:.1f}Hz, mag={:.2f}dB".format(x_3db , y_3db_low)
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=100")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
    ax1.annotate(text, xy=(x_3db , y_3db_low), xytext=(0.35,0.96), **kw)

def annot_3db_high(x,y, ax=None):
    y_3db_high = max(y)-3
    for a, b in zip(y, x):
        if y_3db_high-0.0025<a < y_3db_high+0.0025:
            if b>100:
                x_3db = b

    text= "f={:.1f}kHz, mag={:.2f}dB".format(x_3db/1000 , y_3db_high)
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=100")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
    ax1.annotate(text, xy=(x_3db , y_3db_high), xytext=(0.96,0.96), **kw)

annot_3db_low(x,y)
annot_max(x,y)
annot_3db_high(x,y)


# Show the plot
plt.show()
