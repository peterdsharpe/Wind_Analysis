import numpy as np
from data import von_karman_gust_intensity


def spatial_psds(Omega,
                 altitude,
                 probability_of_exceedance
                 ):
    ### Intensities and length scales
    L_u = 2500 * 0.3048  # 2500 ft., specified by von Karman model
    sigma_u = von_karman_gust_intensity(
        altitude=altitude,
        probability_of_exceedance=probability_of_exceedance,
    )

    ### Assumptions due to isotropic turbulence at high alts
    sigma_v = sigma_u
    sigma_w = sigma_u
    L_v = L_u / 2
    L_w = L_u / 2

    ### PSDs
    u_psd = (
            sigma_u ** 2 *
            2 * L_u / np.pi /
            (1 + (1.339 * L_u * Omega) ** 2) ** (5 / 6)
    )
    v_psd = (
            sigma_v ** 2 *
            2 * L_v / np.pi *
            (1 + 8 / 3 * (2.678 * L_v * Omega) ** 2) /
            (1 + (2.678 * L_v * Omega) ** 2) ** (11 / 6)
    )
    w_psd = (
            sigma_w ** 2 *
            2 * L_w / np.pi *
            (1 + 8 / 3 * (2.678 * L_w * Omega) ** 2) /
            (1 + (2.678 * L_w * Omega) ** 2) ** (11 / 6)
    )
    return u_psd, v_psd, w_psd


if __name__ == '__main__':
    Omega = np.logspace(-5, 1, 500)  # Spatial frequency [rads/meter]
    wavelength = 2 * np.pi / Omega  # Wavenumber [m]

    altitude = 20000
    probability_of_exceedance = 1e-5

    ### Plot PSDs
    import matplotlib.pyplot as plt
    import seaborn as sns

    sns.set(palette=sns.color_palette("husl"))
    fig, ax = plt.subplots(1, 1, figsize=(6.4, 4.8), dpi=200)
    plt.xscale('log')
    plt.yscale('log')
    psds = spatial_psds(
        Omega,
        altitude=altitude,
        probability_of_exceedance=probability_of_exceedance
    )
    plt.plot(Omega, psds[0], label=r"$\Phi_u$")
    plt.plot(Omega, psds[1], label=r"$\Phi_v$")
    plt.plot(Omega, psds[2], label=r"$\Phi_w$")
    plt.annotate(
        s="Data: \"Flying Qualities of Piloted Aircraft\"\nMIL-STD-1797A (1990), U.S. DoD",
        xy=(0.02, 0.02),
        xycoords="axes fraction",
        ha="left",
        va="bottom",
        fontsize=8,
        color=(0, 0, 0, 1)
    )
    plt.axis("equal")
    plt.xlabel(r"Spatial Frequency [rads/meter]")
    plt.ylabel(r"Gust Power Spectral Density ($\Phi$) [$m^3/s^2$]")
    plt.title(r"Von Karman Gusts: Power Spectral Density Models"
              f"\n{altitude} m Altitude, $10^{'{'}{np.log10(probability_of_exceedance):.0f}{'}'}$ Prob. of Exceedance")
    plt.tight_layout()
    plt.legend()
    # plt.savefig("C:/Users/User/Downloads/temp.svg")
    plt.show()
