import sys
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    f = sys.argv[1]
    df = pd.read_csv(f, delimiter=" ", encoding="iso8859_15")['tf-idf']

    print("Min: {}\tMax: {}\tMean: {}\tMedian: {}".format(df.min(), df.max(), df.mean(), df.median()))

    print(df.quantile([0, 0.25, 0.5, 0.75, 1]))

#    df.plot(kind="hist", bins=1000)

#    plt.show()

