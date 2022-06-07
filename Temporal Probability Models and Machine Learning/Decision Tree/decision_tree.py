import pandas as pd
import numpy as np

Name = "Amirhossein Abedi"
Student_Number = "99105594"
# running the code takes about 5-10 mins sorry for the inconvenience

def x_logx(x): # x* log(x) base 2
    if x == 0:
        return 0
    return x*np.log2(x)

class Node:
    def __init__(self, x, y, feature=None, threshold=None, left=None, right=None, value=None, depth=None):
        self.x = x
        self.y = y # information in the node
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value
        self.depth = depth

    def is_leaf(self):
        return self.left == None and self.right == None

class DecisionTree:
    def __init__(self, max_depth=None, min_samples_split=2, feature_to_index=None, features=None, index_to_feature=None):
        self.max_depth = max_depth
        self.feature_to_index = feature_to_index
        self.features = features
        self.min_samples_split = min_samples_split
        self.root = None
        self.index_to_feature = index_to_feature

    def is_splitting_finished(self, node, array_used):
        if node.depth > self.max_depth:
            return True
        if len(node.y) < self.min_samples_split:
            return True
        if sum(node.y) == len(node.y) or sum(node.y) == 0:
            return True
        if sum(array_used) == len(self.features):
            return True
        return False

    def split(X, y, feature_index, threshold): # returns X_left, X_right, y_left, y_right
        return (X[X[:, feature_index] <= threshold], X[X[:, feature_index] > threshold], y[X[:, feature_index] <= threshold], y[X[:, feature_index] > threshold])

    def entropy(y): # suppose y is a binary vector with only ones and zeros
        if len(y) == 0:
            return 0
        num_one = sum(y)
        num_zero = len(y) - num_one
        l = len(y)
        s = x_logx(num_zero/l)
        s += x_logx(num_one/l)
        return (-1)*s

    def information_gain(X, y, feature, threshold, feature_to_index):
        if len(X) == 0:
            return 0
        index = feature_to_index[feature]
        num_less = len(X[X[:, index] <= threshold])
        num_greater = len(X) - num_less

        return DecisionTree.entropy(y) - (((num_less/len(X)) * DecisionTree.entropy(y[X[:, index] <= threshold])) 
            + ((num_greater/len(X)) * DecisionTree.entropy(y[X[:, index] > threshold])))

    def best_split(X, y, features, feature_to_index, used_feature): # returns (index_of_feature, threshold, ig)
        index_of_feature = np.argmin(used_feature)
        threshold_ret = 0
        ig_max = 0
        epsilon = 10**(-6)

        for feature in features:
            index = feature_to_index[feature]
            if used_feature[index]:
                continue

            thresholds = np.unique(X[:, index])
            for threshold in thresholds:
                temp = DecisionTree.information_gain(X, y, feature, threshold, feature_to_index)
                if temp > ig_max:
                    threshold_ret = threshold
                    index_of_feature = index
                    ig_max = temp

            threshold = min(thresholds) - epsilon
            temp = DecisionTree.information_gain(X, y, feature, threshold, feature_to_index)
            if temp > ig_max:
                threshold_ret = threshold
                index_of_feature = index
                ig_max = temp

        return (index_of_feature, threshold_ret, ig_max)

    def build_tree(self, X, y, array_used, depth=0):
        ret_node = Node(X, y, depth = depth)
        if self.is_splitting_finished(ret_node, array_used):
            if sum(y) >= len(y)//2:
                ret_node.value = 1
            else:
                ret_node.value = 0
            return ret_node
        
        index, threshold, ig = DecisionTree.best_split(X, y, self.features, self.feature_to_index, array_used)
        x_left, x_right, y_left, y_right = DecisionTree.split(X, y, index, threshold)

        if ig <= 0 or len(y_left) == 0 or len(y_right) == 0:
            if sum(y) >= len(y)//2:
                ret_node.value = 1
            else:
                ret_node.value = 0
            return ret_node
        
        ret_node.feature = self.index_to_feature[index]
        ret_node.threshold = threshold
        array_used[index] = True
        ret_node.right = self.build_tree(x_right, y_right, array_used, depth + 1)
        ret_node.left = self.build_tree(x_left, y_left, array_used, depth + 1)
        array_used[index] = False

        return ret_node

    def fit(self, X, y):
        used = [False] * len(self.features)
        self.root = self.build_tree(X, y, used)

    def predict(self, X):
        ans = []
        for i in range(len(X)):
            ans.append(self.predict_one_row(X[i]))
        return np.array(ans)

    def predict_one_row(self, x): # x vector of features
        node = self.root

        while not node.is_leaf():
            index = self.feature_to_index[node.feature]
            if x[index] <= node.threshold:
                node = node.left
            else:
                node = node.right
        return node.value

def acc_kfold(x_folds, y_folds, m, n):
    dt = DecisionTree(m, n, col_to_index, d.columns[0:-1], index_to_col)
    x = np.concatenate((x_folds[0], x_folds[1], x_folds[2], x_folds[3]))
    y = np.concatenate((y_folds[0], y_folds[1], y_folds[2], y_folds[3]))
    dt.fit(x, y)
    temp = dt.predict(x_folds[4])
    acc4 = 0
    for i in range(len(temp)):
        if temp[i] == y_folds[4][i]:
            acc4 += 1
    acc4 = acc4 / len(temp)

    dt = DecisionTree(m, n, col_to_index, d.columns[0:-1], index_to_col)
    x = np.concatenate((x_folds[0], x_folds[1], x_folds[2], x_folds[4]))
    y = np.concatenate((y_folds[0], y_folds[1], y_folds[2], y_folds[4]))
    dt.fit(x, y)
    temp = dt.predict(x_folds[3])
    acc3 = 0
    for i in range(len(temp)):
        if temp[i] == y_folds[3][i]:
            acc3 += 1
    acc3 = acc3 / len(temp)

    dt = DecisionTree(m, n, col_to_index, d.columns[0:-1], index_to_col)
    x = np.concatenate((x_folds[0], x_folds[1], x_folds[3], x_folds[4]))
    y = np.concatenate((y_folds[0], y_folds[1], y_folds[3], y_folds[4]))
    dt.fit(x, y)
    temp = dt.predict(x_folds[2])
    acc2 = 0
    for i in range(len(temp)):
        if temp[i] == y_folds[2][i]:
            acc2 += 1
    acc2 = acc2 / len(temp)

    dt = DecisionTree(m, n, col_to_index, d.columns[0:-1], index_to_col)
    x = np.concatenate((x_folds[0], x_folds[2], x_folds[3], x_folds[4]))
    y = np.concatenate((y_folds[0], y_folds[2], y_folds[3], y_folds[4]))
    dt.fit(x, y)
    temp = dt.predict(x_folds[1])
    acc1 = 0
    for i in range(len(temp)):
        if temp[i] == y_folds[1][i]:
            acc1 += 1
    acc1 = acc1 / len(temp)

    dt = DecisionTree(m, n, col_to_index, d.columns[0:-1], index_to_col)
    x = np.concatenate((x_folds[1], x_folds[2], x_folds[3], x_folds[4]))
    y = np.concatenate((y_folds[1], y_folds[2], y_folds[3], y_folds[4]))
    dt.fit(x, y)
    temp = dt.predict(x_folds[0])
    acc0 = 0
    for i in range(len(temp)):
        if temp[i] == y_folds[0][i]:
            acc0 += 1
    acc0 = acc0 / len(temp)

    return (acc0 + acc1 + acc2 + acc3 + acc4) / 5

# import data

d = pd.read_csv(open('breast_cancer.csv', 'r'))

col_to_index = {}
index_to_col = {}
index = 0
for i in d.columns:
    col_to_index[i] = index
    index_to_col[index] = i
    index += 1

# create numpy arrays from data :
x = np.array(d[d.columns[0:30]])
y = np.array(d[d.columns[30]])

# Split your data to train and validation sets

# using only one sub-set of data for testing , has the risk of overfitting hyperparams to test data
# for this reason we use k-fold validation to choose best hyperparams
# accuracy for a particular hyperparam is the mean accuracy among k iterations

# k-folding : suppose k = 5
l = d.shape[0] # #rows df
ranges = [0, l//5, 2*(l//5), 3*(l//5), 4*(l//5), l]

x1, y1 = x[ranges[0]:ranges[1]], y[ranges[0]:ranges[1]]
x2, y2 = x[ranges[1]:ranges[2]], y[ranges[1]:ranges[2]]
x3, y3 = x[ranges[2]:ranges[3]], y[ranges[2]:ranges[3]]
x4, y4 = x[ranges[3]:ranges[4]], y[ranges[3]:ranges[4]]
x5, y5 = x[ranges[4]:ranges[5]], y[ranges[4]:ranges[5]]

x_folds = [x1, x2, x3, x4, x5]
y_folds = [y1, y2, y3, y4, y5]

# Tune your hyper-parameters using validation set

# foreach (m, n) in possible hyper values 
# find accuracy using kfold
# return argmax(m, n) accuracy # todo

max_acc = 0
m_star = 0
n_star = 0

for n in range(5, 26, 5):
    # m for max_depth
    for m in range(1, 8):
        acc = acc_kfold(x_folds, y_folds, m, n)
        if acc > max_acc:
            m_star = m
            n_star = n
            max_acc = acc


# Train your model with hyper-parameters that works best on validation set

# found m_star, n_star
dt = DecisionTree(m_star, n_star, col_to_index, d.columns[0:-1], index_to_col)
dt.fit(x, y)

d_validation = pd.read_csv(open('test.csv'))
validation_set = np.array(d_validation)
prediction = dt.predict(validation_set)

# Predict test set's labels
with open('output.csv', 'w') as f:
    f.write('target\n')
    for i in prediction:
        f.write(f'{i}\n')

