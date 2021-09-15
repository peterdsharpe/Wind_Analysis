import pandas as pd
import numpy as np


def load_data(filename: str) -> pd.DataFrame:
    with open(filename, "r") as f:
        raw_data = f.readlines()

    for line_number, line in enumerate(raw_data):

        if "TIME_UTC, seconds" in line:
            scaling_line_number = line_number + 2
            unrecorded_line_number = line_number + 3

        if "TIME_UTC" in line and line.count(",") > 6:
            header_line_number = line_number
            break

    scaling_factors = np.fromstring(
        raw_data[scaling_line_number],
        sep=","
    )
    scaling_factors = np.hstack(([1], scaling_factors))

    df = pd.read_csv(
        filename,
        delimiter=",",
        skiprows=header_line_number,
    )
    df.columns = [
        column.strip()
        for column in df.columns
    ]

    for i, column in enumerate(df.columns):
        # everything in base SI units please jesus christ

        if column == "P" or column == "Q" or column == "YDP" or column == "ADP":
            scaling_factors[i] *= 100

        df[column] = df[column].apply(
            lambda x: x * scaling_factors[i]
        )

        if column == "TEDR":
            df[column] = df[column].apply(
                lambda x: (10 ** x) * 1000
            )
        if column == "REYN":
            df[column] = df[column].apply(
                lambda x: 10 ** x
            )

    return df


if __name__ == '__main__':
    d = load_data("data/MMS-20Hz_DC8_20160712_R0.ict")
