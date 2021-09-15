from load_single_file import data
import aerosandbox.numpy as np
from scipy import fft, signal, interpolate

w = data["W"].values
N = len(w)

w_windowed = w * signal.windows.hann(N)

freq_rads_per_sec = fft.fftfreq(N, 1 / 20)
fft_output = fft.fft(w_windowed)

freq_rads_per_sec = freq_rads_per_sec[:N // 2]
fft_output = fft_output[:N // 2]

freq_hz = freq_rads_per_sec / (2 * np.pi)
amp = np.abs(fft_output)
power = amp ** 2

psd = power / (2 * (freq_rads_per_sec[1] - freq_rads_per_sec[0]))

from aerosandbox.tools.pretty_plots import plt, show_plot

freq_hz_plot = np.geomspace(freq_hz[1], freq_hz[-1], 1000)
psd_plot = np.exp(
    interpolate.PchipInterpolator(
        np.log(freq_hz[1:]),
        np.log(psd[1:]),
    )(
        np.log(freq_hz_plot)
    )
)
plt.loglog(freq_hz_plot, psd_plot)
show_plot(
    "Power Spectral Density",
    "Frequency [$Hz$]",
    "Power Spectral Density [$m/s^3$]"
)

print(fft_output)
