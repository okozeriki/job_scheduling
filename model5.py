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
    s = pulp.LpVariable.dicts('s', J, lowBound=0, cat='Continuous')
    C = pulp.LpVariable.dicts('C', J, lowBound=0, cat='Continuous')
    y = pulp.LpVariable.dicts('y',JK ,  cat='Binary')



    for j in J:
        prob += C[j] == s[j] + P[j]
        prob += s[j] >= R[j]
    for j in J:
        K2 = [k for k in J if not k == j]
        prob += pulp.lpSum([y[j,k] for k in K2])<= 1
        
    for k in J:
        J2 = [j for j in J if not j == k]
        prob += pulp.lpSum([y[j,k] for j in J2])<= 1
        
    prob += pulp.lpSum([y[j,k] for j,k in JK]) == num-1

    for j,k in JK:
        prob += y[j,k]+y[k,j] <= 1


    M=1000
    for j,k in JK:
        prob+=C[j]<=s[k]+M*(1-y[j,k])

    prob+=pulp.lpSum([W[j]*C[j] for j in J])


    start = time.time()
    status = prob.solve()
    end = time.time()

    
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
        
    

    t = round(end - start,3)

    return pulp.LpStatus[status],prob.objective.value(), t, sorted_job

if __name__ == "__main__":
    main(3)
# %%
