import math
import random
import glob
import numpy as np
import matplotlib.pyplot as plt
import scipy

folder = "/home/phmoll/ITEC/Allgemeines/Papers/NetGames 2018/traces/joined/"

files = glob.glob(folder + "*.log")

logs = {}

for file in files:
    f = open(file)
    content = f.readlines()
    f.close()
    finished = False
    for l in content:
        l = l.split("\t")
        time = int(l[2])
        players = None
        if l[3] != "":
            players = int(l[3])
        if time > 0 and players is not None and not finished:
            if time not in logs:
                logs[time] = []
            logs[time].append(players)
            if players == 1:
                finished = True

x = []
y = []
for time in logs:
    entries = logs[time]
    avg = sum(entries) / float(len(entries))
    logs[time] = avg
    x.append(time)
    y.append(avg)


z = np.polyfit(x, y, 5)
p = np.poly1d(z)

#np.random.seed(0)
exp_x = np.append(scipy.random.exponential(15, 3), scipy.random.exponential(3, 27))
exp_x = np.append(exp_x, scipy.random.exponential(5, 31))
exp_x = np.append(exp_x, scipy.random.exponential(10, 10))
exp_x = np.append(exp_x, scipy.random.exponential(18, 20))
exp_x = np.append(exp_x, scipy.random.exponential(30, 5))
exp_x = np.append(exp_x, scipy.random.exponential(120, 4))
exp_y = range(1, 101)
exp_y.reverse()
exp_x = np.cumsum(exp_x)
exp_x = [int(round(_)) for _ in exp_x]

player_tuples = []
for i in range(0, len(exp_y)):
    player_tuples.append((exp_x[i], exp_y[i]))

values = [(_, round(p(_))) for _ in range(min(x), max(x) + 1)]
values_falling = [(x[0], round(y[0])), (x[1], round(y[1])), (x[2], round(y[2])), (x[3], round(y[3]))]
for i in range(4, len(values)):
    values_falling.append((i, min(values[i][1], values_falling[-1][1])))
values_falling.append((values_falling[-1][0] + 1, 1))


xp = np.linspace(min(x), max(x), 500)
#_ = plt.plot(x, y, '-',
#             [v[0] for v in values], [v[1] for v in values], '.',
#             [v[0] for v in values_falling], [v[1] for v in values_falling], 'rx')
_ = plt.plot(x, y, '-',
             exp_x, exp_y, 'r-')
plt.ylim(1, 100)
plt.xlim(1, 1400)
#plt.show()
plt.savefig("players.pdf")
plt.close()

print(values_falling)
print(player_tuples)
