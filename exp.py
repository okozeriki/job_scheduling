import model1
import model2
import model3
import model5
import csv

with open("result.csv", "w", newline='') as csvfile:

    writer = csv.writer(csvfile)
    writer.writerow(["model","J", "status", "value", "time",1,2,3,4,5,6,7,8,9,10])


    for i in range(1,11):
        status, value, t, sorted_job = model1.main(i)
        writer.writerow(["定式化1",i, status, value, t]+sorted_job)

        status, value, t, sorted_job = model2.main(i)
        writer.writerow(["定式化2",i, status, value, t]+sorted_job)

        status, value, t, sorted_job = model3.main(i)
        writer.writerow(["定式化3",i, status, value, t]+sorted_job)

        status, value, t, sorted_job = model5.main(i)
        writer.writerow(["定式化5",i, status, value, t]+sorted_job)
