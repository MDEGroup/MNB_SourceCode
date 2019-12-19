

import matplotlib.pyplot as plt

names = ['2-topic', '5-topic', '8-topic']
values = [1, 10, 100]

f=plt.figure(figsize=(9, 3))

plt.subplot(131)
plt.bar(names, values)
plt.show()

f.savefig("foo.pdf", bbox_inches='tight')