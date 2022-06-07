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

    order_elims = find_elim_order(is_hidden, n, son)
    # order_elims = hidden

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

def see_all_fathers(i, arr, par):
    for j in par[i]:
        if arr[j]:
            continue
        arr[j] = True
        see_all_fathers(j, arr, par)

def dfs_path(prev, curr, u, v, arr, son , par, active, path, evidence, state = 0):
    # state == 1 : prev -> curr
    # state == 0 : prev <- curr

    active[curr] = True

    # if curr == 2:
    #     print(1)
    if curr == v:
        global indep
        indep = False
        raise Exception()


    if prev == -1:
        for i in son[curr]:
            dfs_path(curr, i, u, v, arr, son, par, active, path, evidence, 1)
        for i in par[curr]:
            dfs_path(curr, i, u, v, arr, son, par, active, path, evidence, 0)

    elif state == 1:
        if curr in evidence or arr[curr]:
            for i in par[curr]:
                if not active[i]:
                    path[i] = curr
                    dfs_path(curr, i, u, v, arr, son, par, active, path, evidence, 0)
        if curr not in evidence:
            for i in son[curr]:
                if not active[i]:
                    path[i] = curr
                    dfs_path(curr, i, u, v, arr, son, par, active, path, evidence, 1)

    elif state == 0:
        if curr not in evidence:
            for i in son[curr]:
                if not active[i]:
                    path[i] = curr
                    dfs_path(curr, i, u, v, arr, son, par, active, path, evidence, 1)

    active[curr] = False

n = int(input().strip())

par = [[] for _ in range(n)]
son = [[] for _ in range(n)]
cpts = [None for _ in range(n)]

for i in range(n):
    pars = [int(j) - 1 for j in input().split()]
    par[i].extend(pars)

    for j in pars:
        son[j].append(i)

    table = [float(j) for j in input().split()]
    table.reverse()
    cpts[i] = CPT(par[i], table, i)

evidence = {}
for i in input().split(','):
    e, value = i.split('->')
    evidence[int(e.strip()) - 1] = int(value.strip())

u, v = map(lambda x: int(x) - 1 , input().split())

has_son_seen = [False] * n
active = [False]*n
path = [-1] * n

for k in evidence.keys():
    see_all_fathers(k, has_son_seen, par)

# print(evidence)

indep = True
try:
    if u in par[v] or v in par[u]:
        raise Exception()
    dfs_path(-1, u, u, v, has_son_seen, son , par, active, path, evidence)
except:
    pass

print('independent' if indep else 'dependent')
# exit(0)

temp = probability_by_elimination(n, son, par, cpts, [u, v], evidence)
q = {u:1, v:1}
s1 = pi_on_factors(temp, q)

q = {u:0, v:1}
s2 = pi_on_factors(temp, q)

q = {u:1, v:0}
s3 = pi_on_factors(temp, q)

q = {u:0, v:0}
s4 = pi_on_factors(temp, q)

s5 = s1 + s2 + s3 + s4

print(f'0.{round(100*((s1 + s3)/s5))}')
print(f'0.{round(100*((s1 + s2)/s5))}')



