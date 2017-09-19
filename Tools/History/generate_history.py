import pandas as pd
import matplotlib.pyplot as plt

s = pd.Series(
    [172, 135, 129],
    index = ["Chrome", "Edge", "IE"]
)

#Set descriptions:
plt.ylabel('# of CVE-IDs 2016')
plt.xlabel('Browser')

#Set tick colors:
ax = plt.gca()

#Plot the data:
my_colors = ['#d04b3e', '#0078d7', '#1ebbee']  #red, green, blue, black, etc.

s.plot(
    kind='bar', 
    color=my_colors,
)

#plt.show()
plt.tight_layout()
plt.savefig("browser_cve_history.png", dpi=300)

