import sys
import pandas as pd

if __name__ == '__main__':
    f = sys.argv[1]
    df = pd.read_csv(f, delimiter=" ", encoding="iso8859_15")

    for row in df.itertuples():
