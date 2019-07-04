# -*- coding: UTF-8 -*-

"""
递推公式：
    f(2m+1) = f(2m)
    f(2m) = f(m)
"""


def process(num):
    dp = [1 for i in range(num + 1)]
    for i in range(1, num + 1):
        if i % 2 == 1:
            dp[i] = dp[i - 1]
        else:
            dp[i] = dp[i - 1] + dp[i // 2]
    return dp[-1]


if __name__ == '__main__':
    while True:
        num = raw_input("输入需要分解的数：")
        if num == "end":
            print ("Bye-bye")
            break
        else:
            try:
                num = int(num)
                print (process(num))
            except Exception as e:
                print ("输入错误")