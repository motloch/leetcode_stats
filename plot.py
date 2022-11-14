"""
This code plots results for our analysis - percentage of users that 'beat' us if we solve
any given number of Easy/Medium/Hard Leetcode problems. Data are loaded from results.csv
and were obtained using leetcode_scrape.py
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Make fontsize bigger
plt.rc('font', size=18)

# Load the data
dat = pd.read_csv('results.csv')

# Plot
fig = plt.figure(dpi=400)
fig.set_size_inches(14.1, 9.7)

difficulties = ['Easy', 'Medium', 'Hard']
colors = ['g', 'orange', 'r']
for diff, color in zip(difficulties, colors):
    dat = dat.sort_values(by = diff + '_num')
    plt.plot(   dat[diff + '_num'], 
                100-dat[diff + '_pct'], 
                label = diff, 
                c = color, 
                marker = 'o', 
                lw = 2,
            )
    plt.text(1800, 20, 'www.motloch.net', rotation = 270, fontsize = 10, alpha = 0.8)

# Style the plot
plt.yscale('log')
plt.xscale('log')
plt.legend()
plt.grid(alpha = 0.2)
plt.xlabel('Number of Leetcode problems solved')
plt.ylabel('Needed to be top')
plt.yticks([100, 10, 1, 0.1, 0.01], ['100%', '10%', '1%', '0.1%', '0.01%'])
plt.xticks([1000, 100, 10, 1], [1000, 100, 10, 1])
plt.savefig('leetcode.jpg', bbox_inches = 'tight')
