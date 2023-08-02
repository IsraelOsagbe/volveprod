import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("4-whp_data.txt", sep="\t")

plt.figure(figsize=(19,10))
plt.plot(data.Time, data["WHP_psig"])

data["whp-avg2"] = data["WHP_psig"].rolling(2).mean()
data["whp-avg10"] = data["WHP_psig"].rolling(10).mean()
plt.plot(data.Time, data["whp-avg2"], label="AVG Rolling 2")
plt.plot(data.Time, data["whp-avg10"], label="AVG Rolling 10")
plt.legend(); 