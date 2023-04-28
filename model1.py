#%%
import click
import pulp
import init_data 
import time

# @click.command()
# @click.option('--num', default = 3, help='the number of jobs')
def main(num):
    J,W,P,R = init_data.init_let_data(num)
    JK=[(j,k) for j in J for k in J if not j ==k]
    prob=pulp.LpProblem(name="prob", sense=pulp.LpMinimize)
    s = pulp.LpVariable.dicts('s', J, lowBound=0, cat='Integer')
    C = pulp.LpVariable.dicts('C', J, lowBound=0, cat='Integer')
    x = pulp.LpVariable.dicts('x',JK ,  cat='Binary')


    M = 1000

    for j in J:
        prob += C[j] == s[j] + P[j]
        prob += s[j] >= R[j]
    for j in J:
        for k in J:
            if not j == k:
                prob += C[j] <= s[k] + M*(1-x[j,k])
                prob += x[j,k] +x[k,j] ==1


    start = time.time()

    prob+=pulp.lpSum([W[j]*C[j] for j in J])
    status = prob.solve()
    print("************Result************")
    print(pulp.LpStatus[status])
    print("Optimal value=",prob.objective.value())

    for v in prob.variables():
        if not "s" in v.name and not "C" in v.name :
            print(v.name,"=",v.varValue) if v.varValue == 1 else None

    result = {f"job{j}": (pulp.value(s[j]),pulp.value(C[j]),R[j]) for j in J}
    sorted_data = sorted(result.items(), key=lambda x: x[1][0])
    sorted_job = [i[0] for i in sorted_data]
    for key, value in sorted_data:
        print('------------')
        print(key, f"s:{value[0]}", f"c:{value[1]}")
        
    end = time.time()

    t = round(end - start,3)

    return pulp.LpStatus[status],prob.objective.value(), t, sorted_job

if __name__ == "__main__":
    main(3)
# %%
