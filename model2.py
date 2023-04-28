#%%

import pulp
import init_data 
import time


def main(num):
    #定数の定義
    J,W,P,R = init_data.init_let_data(num)
    JK=[(j,k) for j in J for k in J if not j ==k]

    #変数の定義
    prob=pulp.LpProblem(name="prob", sense=pulp.LpMinimize)
    s = pulp.LpVariable.dicts('s', J, lowBound=0, cat='Integer')
    C = pulp.LpVariable.dicts('C', J, lowBound=0, cat='Integer')
    x = pulp.LpVariable.dicts('x',JK ,  cat='Binary')

    #制約条件の定義
    for j in J:
        prob += C[j] == s[j]+P[j]
        prob += s[j] >= R[j]
        for k in J:
            if not j == k:
                prob += x[j,k] + x[k,j] == 1
                prob += s[j] >= R[k] * x[k,j] + pulp.lpSum([P[i] * (x[i,j] - x[i,k])for i in J if not i == j if not i == k])
                for i in J:
                    if not k == i:
                        if not i == j:
                            prob += x[j,k] + x[k,i] + x[i,j] <= 2

    #目的関数の定義
    prob+=pulp.lpSum([W[j]*C[j] for j in J])

    #求解
    start = time.time()
    status = prob.solve()
    end = time.time()

    result = {f"job{j}": (pulp.value(s[j]),pulp.value(C[j]),R[j]) for j in J}
    sorted_data = sorted(result.items(), key=lambda x: x[1][0])
    sorted_job = [i[0] for i in sorted_data]
    for key, value in sorted_data:
        print('------------')
        print(key, f"s:{value[0]}", f"c:{value[1]}")
        
   

    t = round(end - start,3)

    return pulp.LpStatus[status],prob.objective.value(), t, sorted_job

if __name__ == "__main__":
    main(3)
# %%
