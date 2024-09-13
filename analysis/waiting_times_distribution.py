import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


"""

-> This code requires you to run the "waiting_times_extraction.py" first so that
a "..._WaitingTimes.csv" file is created so it can be used here.
-> You will also need to choose a reasonable(depends on data size) 
bin_number and a save_path so that the result can be saved somewhere(you choose)

"""

###################################################

file_path = r'example\example_WaitingTimes.csv'
save_path = r'example\example.png'
bin_number = 50

###################################################


dg = pd.read_csv(file_path)
magnit = dg["WaitingTimes"].tolist()

hist, bins = np.histogram(magnit, bins=bin_number, density=True)
y, binEdges = np.histogram(magnit, bins=bins, density=True)

plt.hist(magnit, bins=bins, ec='white', color='white', density=True)
bincenters = 0.5 * (binEdges[1:] + binEdges[:-1])
x = bincenters

plt.plot(x, y, '-', c='black', label='Senseless text')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('τ(s)')
plt.ylabel('P(τ)')
plt.legend()
plt.savefig(save_path, dpi=300)
plt.show()




