import matplotlib.pyplot as plt
import numpy as np


N = 3
dos = (83, 65, 58)
codeexec = (2, 74, 65)
overflow = (31, 70, 59)
memcorrupt = (3, 71, 63)
sqlin = (7, 5, 4)
xss = (1, 0, 0)
bypass = (0, 8, 10)
info = (37, 23, 23)
priv = (16, 2, 5)

ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence

p1 = plt.bar(ind, dos, width)
bot = dos
p2 = plt.bar(ind, codeexec, width, bottom=bot)
bot = [i+j for i,j in zip(bot, codeexec)]
p3 = plt.bar(ind, overflow, width, bottom=bot)
bot = [i+j for i,j in zip(bot, overflow)]
p4 = plt.bar(ind, memcorrupt, width, bottom=bot)
bot = [i+j for i,j in zip(bot, memcorrupt)]
p5 = plt.bar(ind, sqlin, width, bottom=bot)
bot = [i+j for i,j in zip(bot, sqlin)]
p6 = plt.bar(ind, xss, width, bottom=bot)
bot = [i+j for i,j in zip(bot, xss)]
p7 = plt.bar(ind, bypass, width, bottom=bot)
bot = [i+j for i,j in zip(bot, bypass)]
p8 = plt.bar(ind, info, width, bottom=bot)
bot = [i+j for i,j in zip(bot, info)]
p9 = plt.bar(ind, priv, width, bottom=bot)


#plt.ylabel('Scores')
plt.title('CVE IDs by Category')
plt.xticks(ind, ('Chrome', 'Edge', 'IE'))


lgd = plt.legend((p1[0], p2[0], p3[0], p4[0], p5[0], p6[0], p7[0], p8[0], p9[0]), ('DoS', 'Code Execution', 'Overflow', 'Memory Corruption', 'SQL Injection', 'XSS', 'Bypass something', 'Gain Information', 'Gain Privileges'), loc='center left', bbox_to_anchor=(1, 0.5))

plt.tight_layout()
plt.savefig("browser_cve_detail_history.png", dpi=300, bbox_extra_artists=(lgd,), bbox_inches='tight')

