from von_karman_psds import spatial_psds, von_karman_gust_intensity
import numpy as np
import pytest

altitude = 20000
probability_of_exceedance = 1e-5

np.random.seed(0)

x_max = 10000
dx_approx = 0.1

### Scary FFT magic below this line...

fft_exponent = int(np.round(np.log2(x_max / dx_approx))) - 1
k = np.arange(2 ** fft_exponent + 1)

dOmega = 2 * np.pi / x_max
Omega = dOmega * k

spatial_power = np.array(spatial_psds(
    Omega=Omega,
    altitude=altitude,
    probability_of_exceedance=probability_of_exceedance
)).T
spatial_power[0] = 0  # Zero the DC-mode power

rms_from_spatial_power = np.sqrt(np.sum(spatial_power, axis=0) * dOmega)

spatial_amps = np.sqrt(2 * spatial_power * dOmega)
spatial_phase = np.random.random(spatial_amps.shape) * 2 * np.pi
spatial_freq_signal = spatial_amps * np.exp(1j * spatial_phase)

spatial_space_signal = np.fft.irfft(
    spatial_freq_signal,
    axis=0
)
spatial_space_signal = np.real(spatial_space_signal) * k.max()

rms_from_signal = np.sqrt(np.mean(spatial_space_signal**2, axis=0))
assert rms_from_spatial_power == pytest.approx(rms_from_signal, rel = 0.01), "Something went wrong in the IFFT!"

dx = x_max / len(spatial_space_signal)
x = dx * np.arange(len(spatial_space_signal))

import matplotlib.pyplot as plt
import seaborn as sns

sns.set(palette=sns.color_palette("husl"))
fig, ax = plt.subplots(1, 1, figsize=(6.4, 4.8), dpi=200)
for i, label in enumerate(["u", "v", "w"]):
    plt.plot(
        x,
        spatial_space_signal[:, i],
        linewidth=1,
        label=f"${label}_g$",
        color = sns.husl_palette(1, h=i/3)[0]
    )
plt.xlim(0, 100)
plt.xlabel(r"Distance Along Flight Path [m]")
plt.ylabel(r"Local Gusts [m/s]")
plt.title(r"Von Karman Gusts: Sample Generated Gust Profile"
          f"\n{altitude} m Altitude, $10^{'{'}{np.log10(probability_of_exceedance):.0f}{'}'}$ Prob. of Exceedance")
plt.tight_layout()
plt.legend()
# plt.savefig("C:/Users/User/Downloads/temp.svg")
plt.show()

