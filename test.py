import subprocess

# コマンドを実行して、出力を取得する
result = subprocess.check_output(["/usr/bin/python3", "model1.py"])

# 出力を表示する
result_txt = result.decode('utf-8')

start_line = '************Result************'

found = False
for line in result_txt.split('\n'):
    if found:
        print(line)
    if start_line in line:
        found = True
        