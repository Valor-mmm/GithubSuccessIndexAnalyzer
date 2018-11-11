from matplotlib import pyplot as plt
from numpy import arange

import pandas as pd

df = pd.read_pickle('formula_analysis_df.pkl')
del df['formula3']
plt.figure()
df.plot()
plt.xticks(arange(5), list(df.index), rotation=25)
plt.tight_layout()
plt.savefig('formulaAnalysis.png', dpi=400)
plt.show()
