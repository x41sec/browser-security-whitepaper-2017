import matplotlib.pyplot as plt
import pandas as pd

dates = ["9 March 2017",
"16 March 2017",
"29 March 2017",
"2 May 2017",
"9 May 2017",
"19 April 2017",
"25 January 2017",
"1 February 2017",
"3 August 2016",
"31 August 2016",
"12 October 2016",
"20 October 2016",
"7 September 2016",
"14 September 2016",
"13 September 2016",
"29 September 2016",
"1 November 2016",
"9 November 2016",
"1 December 2016",
"9 December 2016"]


X = pd.to_datetime(dates).order()

fig, ax = plt.subplots(figsize=(10,2))
ax.scatter(X, [1]*len(X), color='#d04b3e',
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
plt.savefig("chrome.png", dpi=300)

