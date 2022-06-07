from math import floor
import random as rand
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats as st
import os

def sample_uniform(a, b):
    return rand.uniform(a, b)

def pdf1(x):
    return (0.3*st.norm.pdf(x, loc = 4, scale = np.sqrt(2))) + (0.3*st.norm.pdf(x, loc = 3, scale = np.sqrt(2))) + (0.4*st.expon.pdf(x, scale = 100))

def pdf2(x):
    return (0.2*st.norm.pdf(x, loc = 0, scale = np.sqrt(10))) + (0.2*st.norm.pdf(x, loc = 20, scale = np.sqrt(15))) + (0.3*st.norm.pdf(x, loc = -10, scale = np.sqrt(8))) + (0.3*st.norm.pdf(x, loc = 50, scale = 5))

def pdf3(x):
    if x <= 0:
        return 0
    return (0.2*st.geom.pmf(x, 0.1)) + (0.2*st.geom.pmf(x, 0.5)) + (0.2*st.geom.pmf(x, 0.3)) + (0.4*st.geom.pmf(x, 0.04))

def cdf1(x):
    return (0.3*st.norm.cdf(x, loc = 4, scale = np.sqrt(2))) + (0.3*st.norm.cdf(x, loc = 3, scale = np.sqrt(2))) + (0.4*st.expon.cdf(x, scale = 100))

def cdf2(x):
    return (0.2*st.norm.cdf(x, loc = 0, scale = np.sqrt(10))) + (0.2*st.norm.cdf(x, loc = 20, scale = np.sqrt(15))) + (0.3*st.norm.cdf(x, loc = -10, scale = np.sqrt(8))) + (0.3*st.norm.cdf(x, loc = 50, scale = 5))

def cdf3(x): # returns F(floor(x))
    if x < 1:
        return 0
    return (0.2*st.geom.cdf(x, 0.1)) + (0.2*st.geom.cdf(x, 0.5)) + (0.2*st.geom.cdf(x, 0.3)) + (0.4*st.geom.cdf(x, 0.04))

def F_inverse_continuous(cdf, p, start = -10000, end = 10000):
    if p > 1 or p < 0 :
        return np.NaN
    for _ in range(100):
        mid = (start + end) / 2
        if cdf(mid) > p:
            end = mid
        else:
            start = mid
    return (start + end) / 2

def sample_mean(s):
    mean = 0
    for i in s:
        mean += i
    return mean / len(s)

def sample_var(s):
    m = sample_mean(s)
    var = 0

    for i in s:
        var += (i - m)**2
    return var/(len(s) - 1)

sample1 = []
sample2 = []
sample3 = []

try:
    os.mkdir('part1')
except:
    pass


x = np.arange(-100, 100, 0.1)

y = []
for i in x:
    y.append(pdf1(i))

plt.plot(x, y)
plt.savefig("part1\pdf1.png")

plt.clf()

y = []
for i in x:
    y.append(pdf2(i))


plt.plot(x, y)
plt.savefig("part1\pdf2.png")

x = np.arange(1, 200)

plt.clf()

y = []
for i in x:
    y.append(pdf3(i))


plt.plot(x, y)
plt.savefig("part1\pdf3.png")


for _ in range(1000):
    p1 = rand.uniform(0, 1)
    p2 = rand.uniform(0, 1)
    p3 = rand.uniform(0, 1)

    sample1.append(F_inverse_continuous(cdf1, p1))
    sample2.append(F_inverse_continuous(cdf2, p2))
    sample3.append(floor(F_inverse_continuous(cdf3, p3)))


plt.clf()

plt.hist(sample1, bins = 100)
plt.savefig("part1\pdf1_sample.png")

plt.clf()

plt.hist(sample2, bins = 100)
plt.savefig("part1\pdf2_sample.png")

plt.clf()

plt.hist(sample3, bins = 100)
plt.savefig("part1\pdf3_sample.png")

f = open("part1\log.txt", 'w')
f.write(f'1 {sample_mean(sample1):.4f} {np.sqrt(sample_var(sample1)):.4f}\n')
f.write(f'2 {sample_mean(sample2):.4f} {np.sqrt(sample_var(sample2)):.4f}\n')
f.write(f'3 {sample_mean(sample3):.4f} {np.sqrt(sample_var(sample3)):.4f}')
f.close()