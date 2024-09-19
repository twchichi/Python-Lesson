import random

# 定義常量
MIN_NUMBER = 1
MAX_NUMBER = 49
TOTAL_NUMBERS = 7

# 生成樂透號碼
lottery_numbers = random.sample(range(MIN_NUMBER, MAX_NUMBER + 1), TOTAL_NUMBERS)
special_number = lottery_numbers.pop()
lottery_numbers.sort()

# 輸出結果
print(f"本期大樂透號碼為 {lottery_numbers}")
print(f"本期大樂透特別號為 {special_number}")

# 修改建議
# 1. 常量使用：對於不變的值，我們可以使用常量來增加代碼的可讀性和可維護性。
# 2. 格式化輸出：我們可以使用f-string來簡化輸出語句，使其更加清晰。