import csv


with open('out.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:
        li = []
        for item in row:
            parts = item.split("/")
            li.append(parts[-1])

        with open('champ.csv', 'a') as f1:
            writer = csv.writer(f1, lineterminator='\n') # 改行コード（\n）を指定しておく
            writer.writerow(li)     # list（1次元配列）の場合
