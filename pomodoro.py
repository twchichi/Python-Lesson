# 導入時間模組
import time

# 定義蕃茄鐘計時器函數
def pomodoro_timer():
    # 初始化循環次數
    循環次數 = 0
    # 開始無限循環
    while True:
        # 增加循環次數
        循環次數 += 1
        # 顯示開始工作信息
        print("開始專注工作 (25分鐘)")
        # 暫停25分鐘
        time.sleep(25 * 60)  # 25分鐘工作時間
        
        # 判斷是否需要長休息
        if 循環次數 % 4 == 0:
            # 顯示長休息信息
            print("開始長休息 (20分鐘)")
            # 暫停20分鐘
            time.sleep(20 * 60)  # 20分鐘長休息
        else:
            # 顯示短休息信息
            print("開始短休息 (5分鐘)")
            # 暫停5分鐘
            time.sleep(5 * 60)  # 5分鐘短休息
        
        # 詢問用戶是否繼續
        選擇 = input("是否繼續下一個循環？(y/n): ")
        # 如果用戶不想繼續，跳出循環
        if 選擇.lower() != 'y':
            break

    # 顯示結束信息
    print("蕃茄鐘結束")

# 導入tkinter模組
import tkinter as tk

# 定義開始蕃茄鐘函數
def 開始蕃茄鐘():
    # 關閉主窗口
    root.destroy()
    # 調用蕃茄鐘計時器函數
    pomodoro_timer()

# 創建主窗口
root = tk.Tk()
# 設置窗口標題
root.title("蕃茄鐘")

# 創建開始按鈕
開始按鈕 = tk.Button(root, text="開始", command=開始蕃茄鐘)
# 將按鈕放置在窗口中
開始按鈕.pack(pady=20)

# 開始主循環
root.mainloop()

pomodoro_timer()
