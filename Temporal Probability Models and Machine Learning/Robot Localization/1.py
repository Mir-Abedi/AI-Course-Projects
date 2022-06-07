import numpy.random as rand
import numpy as np

def sample_in_plane(x_start = -170, x_end = 100, y_statr = -20, y_end = 50):
    return (rand.uniform(x_start, x_end), rand.uniform(y_statr, y_end))

def fill_weight(w, sample, evidence): # emission function
    for i in range(N):
        oly_err = evidence[0] - np.sqrt(((sample[i][0] - OLY_X)**2) + ((sample[i][1] - OLY_Y)**2))
        ars_err = evidence[1] - np.sqrt(((sample[i][0] - ARS_X)**2) + ((sample[i][1] - ARS_Y)**2))
        pav_err = evidence[2] - np.sqrt(((sample[i][0] - PAV_X)**2) + ((sample[i][1] - PAV_Y)**2))
        asc_err = evidence[3] - np.sqrt(((sample[i][0] - ASC_X)**2) + ((sample[i][1] - ASC_Y)**2))

        w[i] = normal_pdf(oly_err, 2, 1)*normal_pdf(ars_err, 2, 1)*normal_pdf(pav_err, 2, 1)*normal_pdf(asc_err, 2, 1)

def normal_pdf(x, mu, sigma2):
    return (1/np.sqrt(2*np.pi*sigma2))*np.exp(-(((x-mu)**2)/(2*sigma2)))

def create_new_sample(sample, indices):
    c = N//2
    sample_ret = []

    for i in range(N//2):
        temp = sample[indices[i + c]]
        sample_ret.append(temp)
        sample_ret.append((temp[0] + (2 * rand.randn()), temp[1] + (2 * rand.randn())))
    
    return sample_ret

def transition(sample): # transition function
    for i in range(len(sample)):
        sample[i] = (sample[i][0] + rand.randn() + 2, sample[i][1] + rand.randn() + 1)

def mean_2d(sample):
    l = len(sample)
    s_x = 0
    s_y = 0
    for i in sample:
        s_x += i[0]
        s_y += i[1]
    return s_x/l, s_y/l

N = 1000

w = [0] * N
sample = [None] * N

OLY_X, OLY_Y = -133, 18
ARS_X, ARS_Y = -121, -9
PAV_X, PAV_Y = -113, 1
ASC_X, ASC_Y = -104, 12

oly = []
ars = []
pav = []
asc = []

mounts = [oly, ars, pav, asc]
for i in range(4):
    input()
    for _ in range(20):
        mounts[i].append(float(input().strip()))


for i in range(N):
    sample[i] = sample_in_plane()

# sample initialized

for i in range(20):
    fill_weight(w, sample, [oly[i], ars[i], pav[i], asc[i]])
    indices = np.argsort(w)
    
    for j in range(N//2):
        w[indices[j]] = 0

    if i == 19:
        x, y = mean_2d(sample)
        print(int(np.ceil(x/10)*10))
        print(int(np.ceil(y/10)*10))

    sample = create_new_sample(sample, indices)

    transition(sample)

