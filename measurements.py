
import numpy as np
from scipy.interpolate import make_interp_spline
import math
import re
from matplotlib import pyplot as plt

frequencies = []

phases = []

magnitudes = []

def phase_calculation(frequencie):
    f = frequencie
    om = f * 2 * math.pi

    C_1 = 166.5 * (10 ** -9)
    R_2 = 47000
    C_a = 4.05 * (10 ** -9)
    R_a = 987
    R_b = 81800
    C_x = 968 * (10 ** -9)
    R_c = 1.98 * (10 ** 6)

    pre = (1 - (om ** 2) * C_a * C_1 * R_a * R_2)
    A = C_1 * R_2 * om * pre
    E = ((R_b * om * ((C_a * R_a) + (C_1 * R_2))) - (1 / (om * C_x)) + ((om * C_1 * C_a * R_2 * R_a) / C_x))
    F = R_c * R_2 * C_1
    G = (R_b * pre) + (((C_a * R_a) + C_1 * R_2) / C_x)
    H = (((C_1 * R_2) + (C_a * R_a)) * om)
    D = E * F
    B = F * G
    C = (C_1 * R_2 * om) * H
    x = (G ** 2) - (E ** 2)
    y = (pre ** 2) - (H ** 2)
    total = ((A * x) + (y * B)) / ((x * C) + (y * D))
    phase = np.degrees(math.atan(total))
    return phase

file_path = "measurement results.txt"
with open(file_path, 'r') as file:

    next(file)  # Skip the header line

    for line in file:

        freq, mag,phase  = map(float, line.split())

        frequencies.append(freq)

        magnitudes.append(mag)
        phases.append(phase_calculation(freq))
    # for i in range(0,6):
    #     for x in range(100):
    #         frequencie = (10**i)+x*(10**(i-1))
    #         new_phase =phase_calculation(frequencie)
    #         if not (new_phase in phases):
    #             phases.append(new_phase)

print(len(phases))
frequencies = np.array(frequencies)
log_frequencies = np.log10(frequencies)
log_frequencies_smooth = np.linspace(log_frequencies.min(),log_frequencies.max(),2000)

spl = make_interp_spline(log_frequencies,magnitudes,k=1)
magnitudes_smooth = spl(log_frequencies_smooth)
spl = make_interp_spline(log_frequencies,phases,k=1)
phases_smooth = spl(log_frequencies_smooth)
frequencies_smooth = 10**log_frequencies_smooth


frequency_list = frequencies_smooth
magnitude_list = magnitudes_smooth
phase_list = phases_smooth
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


# Parse text
x,y,y2= frequency_list,magnitude_list,phase_list

# Create the plot
fig, ax1 = plt.subplots(figsize=(10, 7))

# Plot magnitude on the primary y-axis
ax1.plot(frequency_list, magnitude_list, label="Magnitude (dB)", linestyle='-', color='g', linewidth=1.5)
ax1.set_xscale('log')
ax1.set_xlim(1, 1000000)
ax1.set_ylim(0,35)
ax1.set_xlabel("Frequency (Hz)", fontsize=12)
ax1.set_ylabel("Magnitude (dB)", fontsize=12, color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.grid(True, which="both", linestyle="--", linewidth=0.5)

#Create a secondary y-axis for phase
ax2 = ax1.twinx()
ax2.plot(frequency_list, phase_list, label="Phase (degrees)", linestyle='--', color='g', linewidth=1.5)
ax2.set_ylabel("Phase (degrees)", fontsize=12, color='black')
ax2.set_ylim(-150, 150)  # Phase range: -90 to 90 degrees
ax2.tick_params(axis='y', labelcolor='black')

# Add title and legends
plt.title("Frequency Response measurements with calculated phase", fontsize=14)
fig.tight_layout()  # Adjust layout to prevent overlap

# Combine legends from both axes
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1  + lines_2, labels_1 +labels_2 , loc='lower right', fontsize=10)
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

def annot_phase_45(x,y, ax=None):
    phase = 45

    for a, b in zip(y, x):
        if phase - 0.05 < a < phase + 0.05:
            if b < 100:
                x_3db_phase = b
                y_phase = a

    text= "f={:.1f}Hz, phase={:.2f}".format(x_3db_phase , phase)

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=100")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="left", va="top")
    ax2.annotate(text, xy=(x_3db_phase , y_phase), xytext=(0.30,0.66), **kw)

def annot_phase_min45(x,y, ax=None):
    phase = -45

    for a, b in zip(y, x):
        if phase - 0.05 < a < phase + 0.05:
            if b > 10000:
                x_3db_phase = b
                y_phase = a

    text= "f={:.1f}kHz, phase={:.2f}".format(x_3db_phase/1000 , phase)

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=100")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="left", va="top")
    ax2.annotate(text, xy=(x_3db_phase , y_phase), xytext=(0.65,0.50), **kw)
annot_3db_low(x,y)
annot_max(x,y)
annot_3db_high(x,y)
annot_phase_45(x,y2)
annot_phase_min45(x,y2)
# Show the plot
plt.show()