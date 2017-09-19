import matplotlib.pyplot as plt
import pandas as pd

dates = ["08-Nov-16",
"09-Aug-16",
"11-Apr-17",
"11-Oct-16",
"13-Dec-16",
"13-Sep-16",
"14-Mar-17"]

X = pd.to_datetime(dates).order()

fig, ax = plt.subplots(figsize=(10,2))
ax.scatter(X, [1]*len(X), color='#1ebbee',
           marker='s', s=10)
fig.autofmt_xdate()

# everything after this is turning off stuff that's plotted by default

ax.yaxis.set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')

ax.get_yaxis().set_ticklabels([])
day = pd.to_timedelta("1", unit='D')
plt.xlim(X[0] - day, X[-1] + day)
plt.tight_layout()
plt.savefig("ie.png", dpi=300)

