import numpy as np

alts = np.load("altitudes.npy")
lats = np.load("latitudes.npy")
speeds = np.load("wind_99_vs_latitudes_altitudes.npy")

import scipy.io as io

io.savemat("wind_data_99.mat", {
    "alts": alts,
    "lats": lats,
    "speeds": speeds
})