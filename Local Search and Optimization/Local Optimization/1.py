import random as rand
import matplotlib.pyplot as plt
import numpy as np


def draw_function(f, start, end):
    x = []
    y = []

    rate = 0.01
    while start <= end:
        x.append(start)
        y.append(f(start))

        start += rate
    plt.plot(x, y)
    plt.show()

def f1(x):
    return (((x**4)*(np.exp(x))) - np.sin(x))/2

def f2(x):
    return 5*np.log10(np.sin(5*x) + np.sqrt(x))

def f3(x):
    return np.cos(5*np.log10(x)) - ((x**3)/10)

def derivative(f, x): # returns derivative of single variable function at point x
    h = 10**(-6)
    return (f(x + h) - f(x))/h

def second_derivative(f, x):
    h = 10**(-6)
    return (derivative(f, x + h) - derivative(f, x))/h  

def GC_single_variable(f, l_rate, max_rep, start, end): # returns (array_#_try, array_x_found)
    point = rand.uniform(start, end)
    x = []
    times = []

    times.append(1)
    x.append(point)

    for i in range(2, max_rep + 1):
        times.append(i)

        point = point - (l_rate * derivative(f, point))
        if point >= end:
            point = end
        if point <= start:
            point = start
        x.append(point)
    return times, x

def run_GC_1000_times(f, l_rate, start, end):
    chosen = []
    for _ in range(1000):
        chosen.append(GC_single_variable(f, l_rate, 100, start, end)[1][-1])
    return chosen

def get_percent_in_GC(f, l_rate, start, end, ans):
    temp = run_GC_1000_times(f, l_rate, start, end)
    error = 10**(-3)
    s = 0
    for i in temp:
        if abs(i - ans) <= error:
            s += 1
    return s / 10

def get_0_derivative(f, start, end): # newton_raphson approach
    x = rand.uniform(start, end)

    error = 10**(-3)
    while True:
        if abs(derivative(f, x)) <= error:
            return x
        x = x - (derivative(f, x)/second_derivative(f, x))
        if x >= end:
            return end
        if x <= start:
            return start

def run_newton_raphson_1000_times(f, start, end):
    ans = []
    for _ in range(1000):
        ans.append(get_0_derivative(f, start, end))
    return ans

def get_percent_newton_raphson(f, start, end, ans):
    temp = run_newton_raphson_1000_times(f, start, end)
    error = 10**(-3)
    s = 0
    for i in temp:
        if abs(i - ans) <= error:
            s += 1
    return s / 10

def draw_points(func, x_1_sequence, x_2_sequence):
    fig = plt.figure(figsize=plt.figaspect(0.5))
    X1, X2 = np.meshgrid(np.linspace(-15.0, 15.0, 1000), np.linspace(-15.0, 15.0, 1000))
    Y = func(X1, X2)
    f_sequence = [func(x_1_sequence[i], x_2_sequence[i]) for i in range(len(x_1_sequence))]

    # First subplot
    ax = fig.add_subplot(1, 2, 1)

    cp = ax.contour(X1, X2, Y, colors='black', linestyles='dashed', linewidths=1)
    ax.clabel(cp, inline=1, fontsize=10)
    cp = ax.contourf(X1, X2, Y, )
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.scatter(x_1_sequence, x_2_sequence, s=10, c="y")

    # Second subplot
    ax = fig.add_subplot(1, 2, 2, projection='3d')

    ax.contour3D(X1, X2, Y, 50, cmap="Blues")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.scatter3D(x_1_sequence, x_2_sequence, f_sequence, s=10, c="r")

    plt.show()

def f4(x, y):
    return ((2*(x))/10000) + (np.exp(y)/20000) + (x**2) + (4*(y**2)) - (2*x) - (3*y)

def derivate_two_var_WRT_x(f, x, y):
    h = 10**(-6)
    return (f(x + h, y) - f(x, y))/h

def derivative_two_var_WRT_y(f, x, y):
    h = 10**(-6)
    return (f(x, y + h) - f(x, y))/h

def gradient_two_var(f, x, y):
    return derivate_two_var_WRT_x(f, x, y), derivative_two_var_WRT_y(f, x, y)

def GC_two_variables(f, x_start, x_end, y_start, y_end, max_rep, l_rate): # minimizez f using GC
    x = rand.uniform(x_start, x_end)
    y = rand.uniform(y_start, y_end)
    x_s = [x]
    y_s = [y]

    for _ in range(max_rep - 1):
        gradient = gradient_two_var(f, x, y)
        x = x - (l_rate * gradient[0])
        y = y - (l_rate * gradient[1])
        if x >= x_end:
            x = x_end
        if x <= x_start:
            x = x_start
        if y >= y_end:
            y = y_end
        if y <= y_start:
            y = y_start
        x_s.append(x)
        y_s.append(y)
    return x_s, y_s

def SA(f, start, end, stopping_temp, stopping_iter, alpha, t, gamma):
    x = rand.uniform(start, end)
    for _ in range(stopping_iter):
        if t <= stopping_temp:
            return x
        x_next = rand.uniform(x - alpha, x + alpha)
        if f(x_next) <= f(x):
            x = x_next
            if x >= end:
                x = end
            if x <= start:
                x = start
            t = gamma*t
            continue
        x = x_next if rand.uniform(0, 1) <= np.exp((f(x) - f(x_next))/t) else x
        t = gamma*t
        if x >= end:
            x = end
        if x <= start:
            x = start
    return x

def run_SA_1000_times(f, start, end, alpha):
    ans = []
    for _ in range(1000):
        ans.append(SA(f, start, end, 0.00001, 100000, alpha, 100, 0.99))
    return ans

def get_percent_SA(f, start, end, alpha, ans):
    temp = run_SA_1000_times(f, start, end, alpha)
    error = 10**(-3)
    s = 0
    for i in temp:
        if abs(i - ans) <= error:
            s += 1
    return s / 10


# draw_function(f1, -2, 1)
# draw_function(f3, 2, 6)
# draw_function(f3, 0.5, 2)

# --------------------------------------------------------

# for alpha in [0.1, 0.4, 0.6, 0.9]:
#     ans = GC_single_variable(f1, alpha, 1000, -2, 1)
#     plt.plot(ans[0], ans[1])
#     plt.show()

# --------------------------------------------------------

# ans = GC_single_variable(f2, 0.1, 1000, 2, 6)
# plt.plot(ans[0], ans[1])
# plt.show()

# ans = GC_single_variable(f3, 0.1, 1000, 0.5, 2)
# plt.plot(ans[0], ans[1])
# plt.show()

# --------------------------------------------------------

# alphas = [0.1, 0.4, 0.6, 0.9]

# for i in alphas:
#     print(f'f2 with {i} learning rate : {get_percent_in_GC(f2, i, 2, 6, 2.186)}%')

# for i in alphas:
#     print(f'f3 with {i} learning rate : {get_percent_in_GC(f3, i, 0.5, 2, 2.0)}%')

# --------------------------------------------------------

# print(f'f2 with newton-raphson , x found : {get_0_derivative(f2, 2, 6)}')
# print(f'f3 with newton-raphson , x found : {get_0_derivative(f3, 0.5, 2)}')

# print(f'f2 newton-raphson percentage : {get_percent_newton_raphson(f2, 2, 6, 2.186)}')
# print(f'f3 newton-raphson percentage : {get_percent_newton_raphson(f3, 0.5, 2, 2)}')

# --------------------------------------------------------

# alphas = [0.01, 0.1, 0.18, 0.25]

# for alpha in alphas:
#     temp = GC_two_variables(f4, -15, 15, -15, 15, 1000, alpha)
#     draw_points(f4, temp[0], temp[1])

# --------------------------------------------------------

for i in range(1, 11):
    alpha = i/10
    print(f'SA percentage using alpha = {alpha} : {get_percent_SA(f2, 2, 6, alpha, 2.186)}')