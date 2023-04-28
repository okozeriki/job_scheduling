import pulp

# 定数
J = [1, 2, 3]
K = [1, 2, 3]
J_num = len(J)
ps = [2, 2, 3]
ws = [3, 2, 1]
rs = [1, 0, 0]
p, w, r = dict(zip(J,ps)), dict(zip(J,ws)), dict(zip(J,rs))
JK=[(j,k) for j in J for k in J if not j ==k]

prob=pulp.LpProblem(name="prob", sense=pulp.LpMinimize)
s = pulp.LpVariable.dicts('s', J, lowBound=0, cat='Continuous')
C = pulp.LpVariable.dicts('C', J, lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts('y',JK ,  cat='Binary')



for j in J:
    prob += C[j] == s[j] + p[j]
    prob += s[j] >= r[j]
for j in J:
    K2 = [k for k in K if not k == j]
    prob += pulp.lpSum([y[j,k] for k in K2])<= 1
    
for k in K:
    J2 = [j for j in J if not j == k]
    prob += pulp.lpSum([y[j,k] for j in J2])<= 1
    
prob += pulp.lpSum([y[j,k] for j,k in JK]) == J_num-1

for j,k in JK:
    prob += y[j,k]+y[k,j] <= 1


M=1000
for j,k in JK:
    prob+=C[j]<=s[k]+M*(1-y[j,k])

prob+=pulp.lpSum([w[j]*C[j] for j in J])

prob.solve()
print(pulp.LpStatus[prob.status])
for v in prob.variables():
    if "x" in v.name:
        print(v.name,"=",v.varValue) if v.varValue == 1 else None
    else:
        print(v.name,"=",v.varValue)
print("Optimal value=",prob.objective.value())