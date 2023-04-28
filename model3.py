#%%
import click
import pulp
import init_data 
import time

# @click.command()
# @click.option('--num', default = 3, help='the number of jobs')
def main(num):
    J,W,P,R = init_data.init_let_data(num)
    T = max(list(R.values())) + sum(list(P.values()))
    JT = [(j+1,t) for j in range(len(J)) for t in range(T+1)]
    
    prob=pulp.LpProblem(name="prob", sense=pulp.LpMinimize)
    C = pulp.LpVariable.dicts('C', J, lowBound=0, cat='Integer')
    z = pulp.LpVariable.dicts('y',JT ,  cat='Binary')



    prob += pulp.lpSum([t*z[j,t] + P[j] for j in J for t in range(T)])


    # 制約式
    for j in J:
        prob += pulp.lpSum(z[j,t] for t in range(R[j],T-P[j])) == 1

    for t in range(T+1):
        prob += pulp.lpSum(pulp.lpSum(z[j,t2] for t2 in range(max(t-P[j],0)+1,t) for j in J)) <= 1


    start = time.time()
    status = prob.solve()
    end = time.time()

    
    print("************Result************")
    print(pulp.LpStatus[status])
    print("Optimal value=",prob.objective.value())

    result = {j:t for j,t in JT if z[j,t].value() == 1}
    sorted_data = sorted(result.items(), key=lambda x: x[1])
    sorted_job = [f"job{i[0]}" for i in sorted_data]
    print(sorted_job)
    for key, value in sorted_data:
        print('------------')
        print(key, value)
        
    

    t = round(end - start,3)

    return pulp.LpStatus[status],prob.objective.value(), t, sorted_job

if __name__ == "__main__":
    main(7)
# %%
