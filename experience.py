import time
import subprocess
import csv

# 実行するPythonファイルと出力するCSVファイルの名前をリストに格納する
file_names = ["model1.py"]

# CSVファイルを書き込むためのファイルオブジェクトを作成する
with open("execution_times.csv", "w", newline='') as csvfile:
    # CSVファイルを書き込むためのwriterオブジェクトを作成する
    writer = csv.writer(csvfile)
    
    # ヘッダー行を書き込む
    writer.writerow(["File", "Time (sec)"])
    
    # 各Pythonファイルを順番に実行して実行時間を計測する
    for file_name in file_names:
        for i in range(1,10):
            start_time = time.time()
            
            # Pythonファイルを実行する
            subprocess.run(['/', file_name, "--num",f"{i}"])
            
            end_time = time.time()
            
            # 実行時間を計算する
            execution_time = round(end_time - start_time,3)
            
            # 実行時間をCSVファイルに書き込む
            writer.writerow([f"{file_name}{i}", execution_time])
    print("Done!")