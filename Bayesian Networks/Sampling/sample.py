import json
import os
import random as rand
import matplotlib.pyplot as plt

def find_unseen(n, seen):
    for i in range(n):
        if not seen[i]:
            return i

def topological_sort(n, son):
    seen = [False] * n
    num_seen = [0]
    order = []

    root = 0
    dfs(root, son , num_seen, seen, order)

    while num_seen[0] < n:
        root = find_unseen(n, seen)
        dfs(root, son , num_seen, seen, order)

    order.reverse()
    return order

def dfs(i, son, num_seen, seen, order):
    seen[i] = True
    num_seen[0] += 1
    for j in son[i]:
        if seen[j]:
            continue
        dfs(j, son, num_seen, seen, order)
    order.append(i)

class CPT(object):
    def __init__(self, args, table, i):
        self.args = args.copy()
        self.args.append(i)
        self.table = table
        self.var = i
        

    def query(self, q, num): # if num == -1 return wanted query else return table[num]

        if num != -1:
            return self.talbe[num]

        # q is a dict of arguments x_i : True\False
        # number of queries must match number of arguments
        inverse = q[self.var] == 0
        coef = 2**(len(self.args) - 1)
        index = 0
        for i in range(len(self.args)):
            if self.args[i] not in q:
                return 0
            elif self.var == self.args[i]:
                index = index // 2
            elif q[self.args[i]]:
                index += coef
            coef = coef // 2
        return 1 - self.table[index] if inverse else self.table[index] 
            
class factor(object):
    def __init__(self, args, table):
        self.args = args.copy()
        self.table = table
        self.has_arg = {}
        for j in args:
            self.has_arg[j] = True
        

    def query(self, q, num): # if num == -1 return wanted query else return table[num]

        if num != -1:
            return self.talbe[num]

        # q is a dict of arguments x_i : True\False
        # number of queries must match number of arguments
        coef = 2**(len(self.args) - 1)
        index = 0
        for i in range(len(self.args)):
            if self.args[i] not in q:
                return 0
            if q[self.args[i]]:
                index += coef
            coef = coef // 2
        return self.table[index] 
    
    def arg_exists(self, i):
        return i in self.has_arg
        
def cpt_to_factor(cpt, evidence): # returns factor
    args = []
    for i in cpt.args:
        if i in evidence:
            continue
        args.append(i)
    
    evidence_copy = evidence.copy()
    table = []
    fill_table(args, 0, evidence_copy, table, cpt)

    return factor(args, table)

def fill_table(args, index, dict, table, cpt):
    if index == len(args):
        table.append(cpt.query(dict, -1))
        return
    for i in range(2):
        dict[args[index]] = i
        fill_table(args, index + 1, dict, table, cpt)

def probability_by_elimination(n, son, par, cpts, q, evidence): # q array of queries, evidence -> dictionary of evidence
    
    # find hidden variables
    
    temp_arr = [False] * n
    hidden = []
    is_hidden = [False] * n

    for i in q:
        temp_arr[i] = True
    
    for k in evidence.keys():
        temp_arr[k] = True
    
    for i in range(n):
        if not temp_arr[i]:
            hidden.append(i)
            is_hidden[i] = True

    # now we have hidden ( list of hiddens ) and is_hidden ( check whether i is hidden )
    # in the initial cpt parents are in order

    
    factors = []
    for i in cpts:
        temp = cpt_to_factor(i, evidence)
        if temp.args:
            factors.append(temp)

    # now we have factors

    # order_elims = find_elim_order(is_hidden, n, son)
    order_elims = hidden

    # elim based on order
    for i in order_elims:
        eliminate(factors, based_on = i)
    
    return factors

def find_elim_order(is_hidden, n, son):
    sorted_list = topological_sort(n, son)
    ret = []
    for i in sorted_list:
        if is_hidden[i]:
            ret.append(i)
    ret.reverse()
    return ret

def eliminate(factors, based_on):
    chosen_index = []
    chosen_factors = []

    for i in range(len(factors)):
        if factors[i].arg_exists(based_on):
            chosen_index.append(i)
    
    for i in chosen_index:
        chosen_factors.append(factors[i])
    
    query = {based_on:0}
    new_args = []

    for i in factors:
        for j in i.args:
            if j in query:
                continue
            new_args.append(j)
            query[j] = 0
    
    table = []
    join_table(new_args, 0, query, table, based_on, chosen_factors)

    i = len(chosen_index) - 1
    while i >= 0:
        factors.pop(chosen_index[i])
        i -= 1

    factors.append(factor(new_args, table))

def join_table(args, index, query, table, based_on, chosen_factors):
    if index == len(args):
        query[based_on] = 0
        s = pi_on_factors(chosen_factors, query)
        query[based_on] = 1
        s += pi_on_factors(chosen_factors, query)
        table.append(s)
        return
    
    for i in range(2):
        query[args[index]] = i
        join_table(args, index + 1, query, table, based_on, chosen_factors)
        
def pi_on_factors(factors, query):
    s = 1
    for f in factors:
        s *= f.query(query, -1)
    return s

def prior_sampling(n, par, cpts, order, query): # query and evidence -> dict
    sample = [0] * n
    acceptable = 0
    for i in range(10000):
        for j in order:
            p = rand.uniform(0, 1)
            if p <= cpts[j].table[choose_row(par[j], sample)]:
                sample[j] = 1
            else:
                sample[j] = 0
        if check_acceptable(sample, query):
            acceptable += 1
        
    return acceptable / 10000

def check_acceptable(sample, query):
    for k, v in query.items():
        if sample[k] != v:
            return False
    return True

def rejection_sampling(n, par, cpts, order, query, evidence):
    sample = [0] * n
    valid = 0
    acceptable = 0
    for i in range(1000):
        for j in order:
            p = rand.uniform(0, 1)
            if p <= cpts[j].table[choose_row(par[j], sample)]:
                sample[j] = 1
            else:
                sample[j] = 0
        if check_valid(sample, evidence):
            valid += 1
        if check_valid_acceptable(sample, evidence, query):
            acceptable += 1
        
    if valid == 0:
        return 0
    return acceptable / valid

def choose_row(parents, sample):
    coef = 2**(len(parents) - 1)
    index = 0
    for i in parents:
        if sample[i] == 1:
            index += coef
        coef = coef // 2
    return index

def check_valid(sample, evidence):
    for k, v in evidence.items():
        if sample[k] != v:
            return False
    return True

def check_valid_acceptable(sample, evidence, query):
    for k, v in evidence.items():
        if sample[k] != v:
            return False
    for k, v in query.items():
        if sample[k] != v:
            return False
    return True

def LW_sampling(n, par, cpts, order, query, evidence):
    sum_w = 0
    w = 0
    sample = [0] * n
    for i in range(1000):
        w_current = 1
        for j in order:
            if j in evidence:
                sample[j] = evidence[j]
                if evidence[j] == 1:
                    w_current *= cpts[j].table[choose_row(par[j], sample)]
                else:
                    w_current *= 1 - cpts[j].table[choose_row(par[j], sample)]
                continue
            p = rand.uniform(0, 1)
            if p <= cpts[j].table[choose_row(par[j], sample)]:
                sample[j] = 1
            else:
                sample[j] = 0
        if check_acceptable(sample, query):
            w += w_current
        sum_w +=  w_current
        
    return w / sum_w

def gibbs_sampling(n, par, cpts, query, evidence):
    sample = [0] * n
    acceptable = 0
    for k in evidence.keys():
        sample[k] = evidence[k]
    random_order = [i for i in range(n)]
    rand.shuffle(random_order)
    for i in range(1000):
        for j in random_order:
            if j in evidence:
                continue
            p = rand.uniform(0, 1)
            if p <= cpts[j].table[choose_row(par[j], sample)]:
                sample[j] = 1
            else:
                sample[j] = 0

    # random walked to some state

    for i in range(10000):
        for j in random_order:
            if j in evidence:
                continue
            p = rand.uniform(0, 1)
            if p <= cpts[j].table[choose_row(par[j], sample)]:
                sample[j] = 1
            else:
                sample[j] = 0
        if check_acceptable(sample, query):
            acceptable += 1

        
    return acceptable / 10000

def add_parents_to_list(s, name_to_num, num):
    for i in s.split():
        if i in name_to_num:
            continue
        name_to_num[i] = num[0]
        num[0] += 1

def sum_over_all(factors, args, index, query, sum_):
    if index == len(args):
        sum_[0] += pi_on_factors(factors, query)
        return
    for i in range(2):
        query[args[index]] = i
        sum_over_all(factors, args, index + 1, query, sum_)

try:
    os.mkdir('output')
except:
    pass

index = 1
while True:
    if not os.path.isdir(f'inputs\\{index}'):
        break
    with open(f'inputs\\{index}\\input.txt') as bn, open(f'inputs\\{index}\\q_input.txt') as q:
        real_values = []
        p_s = []
        r_s = []
        lw_s = []
        g_s = []

        n = int(bn.readline().strip())

        par = [[] for _ in range(n)]
        son = [[] for _ in range(n)]
        cpts = [None for _ in range(n)]

        name_to_num = {}
        num_names = [0]

        for i in range(n):
            name = bn.readline().strip()
            if name not in name_to_num:
                name_to_num[name] = num_names[0]
                num_names[0] += 1
            
            s = bn.readline().strip()
            table = []

            if s.startswith('0.') or s == '1' or s == '0':
                table.append(float(s))
                cpts[name_to_num[name]] = CPT([], table, name_to_num[name])
                continue

            add_parents_to_list(s, name_to_num, num_names)

            for i in s.split():
                par[name_to_num[name]].append(name_to_num[i])
                son[name_to_num[i]].append(name_to_num[name])

            num_par = len(par[name_to_num[name]])

            table = [0.1] * (2**num_par)

            for i in range(2**num_par):
                s = bn.readline().strip().split()
                table[i] = float(s[-1])

            cpts[name_to_num[name]] = CPT(par[name_to_num[name]], table, name_to_num[name])
        
        order = topological_sort(n, son)

        queries = json.loads(q.readline())
        for query, evidence in queries:
            q = []

            for k in query.keys():
                q.append(name_to_num[k])
            
            e = {}

            for k, v in evidence.items():
                e[name_to_num[k]] = v
            
            sum_ = [0]

            factors = probability_by_elimination(n, son, par, cpts, q, e)
            sum_over_all(factors, q, 0, {}, sum_)

            q = {}
            for k, v in query.items():
                q[name_to_num[k]] = v

            q_temp_for_prior = {}
            for k, v in q.items():
                q_temp_for_prior[k] = v
            for k, v in e.items():
                q_temp_for_prior[k] = v

            temp = prior_sampling(n, par, cpts, order, e)
            p_s.append(0 if temp <= 10**(-9) else min(prior_sampling(n, par, cpts, order, q_temp_for_prior) / temp, 1))
            r_s.append(rejection_sampling(n, par, cpts, order, q, e))
            lw_s.append(LW_sampling(n, par, cpts, order, q, e))
            g_s.append(gibbs_sampling(n, par, cpts, q, e))
            ans = pi_on_factors(factors, q)
            real_values.append(ans/sum_[0])

        x = [i + 1 for i in range(len(real_values))]

        f = open(f'output\\{index}.txt', 'w')
        for i in range(len(real_values)):
            f.write(f'{real_values[i]:.5f} {p_s[i]:.5f} {r_s[i]:.5f} {lw_s[i]:.5f} {g_s[i]:.5f}\n')

        f.close()

        for i in range(len(real_values)):
            r_s[i] = abs(r_s[i] - real_values[i])
            g_s[i] = abs(g_s[i] - real_values[i])
            p_s[i] = abs(p_s[i] - real_values[i])
            lw_s[i] = abs(lw_s[i] - real_values[i])

        plt.plot(x, r_s)
        plt.plot(x, p_s)
        plt.plot(x, lw_s)
        plt.plot(x, g_s)
        plt.legend(['Rejection', 'Prior', 'LW', 'Gibbs'])
        plt.savefig(f'output\\{index}.png')
        plt.clf()

    index += 1
