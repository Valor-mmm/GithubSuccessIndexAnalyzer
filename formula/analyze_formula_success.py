from matplotlib import pyplot as plt
import pandas as pd

df = pd.read_pickle('formula_analysis_df.pkl')

plt.figure()
df.plot()
plt.show()