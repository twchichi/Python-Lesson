scores = []  # 設定原始分數的列表

while True:
    try:
        inscore = int(input("請輸入學生的成績（輸入-1結束）："))
        if inscore == -1:
            break
        if 0 <= inscore <= 100:
            scores.append(inscore)
        else:
            print("請輸入0到100之間的有效分數。")
    except ValueError:
        print("請輸入有效的整數。")

if scores:
    total = sum(scores)
    average = total / len(scores)
    print(f"共有 {len(scores)} 位學生")
    print(f"本班總成績: {total} 分，平均成績: {average:.2f} 分")
else:
    print("沒有輸入任何有效的分數。")

# 修改建議
# 1. 使用 while True 和 break 來控制循環，使結構更清晰。
# 2. 加入了錯誤處理，確保輸入的是有效的整數和有效的分數範圍。
# 3. 使用 sum() 函數來計算總分，更加簡潔。
# 4. 使用 f-string 來格式化輸出，更加現代和易讀。
# 5. 增加了對沒有輸入任何分數的情況的處理。