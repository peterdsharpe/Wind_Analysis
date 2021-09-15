from load_single_file import data
import numpy as np
from scipy import fft, signal

w = data["W"].values
N = len(w)

w_windowed = w * signal.windows.hann(N)

freq = fft.fftfreq(N, 1/20)
out = fft.fft(w_windowed)

freq = freq[:N//2]
out = out[:N//2]

freq = freq / (2 * np.pi)

from aerosandbox.tools.pretty_plots import plt, show_plot
plt.loglog(freq, np.abs(out) ** 2)
show_plot(
    "Power Spectral Density",
    "Frequency [Hz]",
    "Power Spectral Density"
)

print(out)