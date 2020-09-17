import pandas as pd
import numpy as np
from pathlib import Path
base_path = Path(__file__).parent

raw_data = pd.read_csv(base_path / "gustfig_data.csv")

sigma_ft_per_sec = []
altitude_kft = []
probability_of_exceedance = []

for PoE_str in ["1e-6", "1e-5", "1e-4", "1e-3", "1e-2", "1e-1"]:
    x_index = list(raw_data.columns).index(f"{PoE_str} PoE")
    y_index = x_index + 1

    x = raw_data.iloc[1:, x_index].dropna().to_numpy().astype(float)
    y = raw_data.iloc[1:, y_index].dropna().to_numpy().astype(float)

    sigma_ft_per_sec.append(x.data)
    altitude_kft.append(y.data)
    probability_of_exceedance.append(
        np.array(
            [eval(PoE_str)] * len(x)
        )
    )

sigma_ft_per_sec = np.concatenate(sigma_ft_per_sec)
altitude_kft = np.concatenate(altitude_kft)
probability_of_exceedance = np.concatenate(probability_of_exceedance)

# MIL-Spec recommends minimum 3 ft/s RMS gust design load at any condition
sigma_ft_per_sec = np.maximum(sigma_ft_per_sec, 3)

sigma = sigma_ft_per_sec * 0.3048
altitude = altitude_kft * 0.3048 * 1000

### Build an interpolator for use in other things
from scipy import interpolate

class GustInterpolator():
    def __init__(self,
                 altitude_data,
                 probability_of_exceedance_data,
                 sigma_data,
                 ):
        self.altitude_data = altitude_data
        self.probability_of_exceedance_data = probability_of_exceedance_data
        self.sigma_data = sigma_data

    def __call__(self, altitude, probability_of_exceedance):
        return interpolate.griddata(
            points=(
                self.altitude_data / 1000,
                np.log10(self.probability_of_exceedance_data)
            ),
            values=self.sigma_data,
            xi=(
                altitude / 1000,
                np.log10(probability_of_exceedance)
            ),
            method="linear",
            rescale=True,
            fill_value=self.sigma_data.min(),
        )


von_karman_gust_intensity = GustInterpolator(
    altitude,
    probability_of_exceedance,
    sigma,
)
