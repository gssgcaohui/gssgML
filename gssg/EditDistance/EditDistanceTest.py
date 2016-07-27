#!/usr/bin/ env python
# coding=utf-8

# 动态规划 之 编辑距离

import numpy as np


class LevenshteinDistance:
    def edit(self, input_x, input_y):
        xlen = len(input_x) + 1  # 此处需要多开辟一个元素存储最后一轮的计算结果
        ylen = len(input_y) + 1
        dp = np.zeros(shape=(xlen, ylen), dtype=int)
        for i in range(0, xlen):
            dp[i][0] = i
        for j in range(0, ylen):
            dp[0][j] = j
        for i in range(1, xlen):
            for j in range(1, ylen):
                if input_x[i-1] == input_y[j-1]:
                    cost = 0
                else:
                    cost = 1
                dp[i][j] = min(dp[i - 1][j]+1, dp[i][j - 1]+1, dp[i - 1][j - 1]+cost)
        return dp[xlen - 1][ylen - 1]

        # print dp


def edit_dist(txt1,txt2):
    first_len = len(txt1)
    second_len = len(txt2)

    ed = [[0]*(second_len+1) for _ in range(first_len+1)]
    for i in range(0,first_len+1):
        ed[i][0] = i

    for j in range(0,second_len+1):
        ed[0][j] = j


    for i in range(0,first_len+1):
        for j in range(0,second_len+1):
            if txt1[i-1] == txt2[j-1]:
                ed[i][j] = ed[i-1][j-1]
            else:
                ed[i][j] = min(ed[i][j-1],ed[i-1][j],ed[i-1][j-1]) + 1
    return ed[i][j]


def levenshtein( first, second):
    if len(first) > len(second):
        first, second = second, first
    if len(first) == 0:
        return len(second)
    if len(second) == 0:
        return len(first)
    first_length = len(first) + 1
    second_length = len(second) + 1
    distance_matrix = [range(second_length) for x in range(first_length)]
    # print distance_matrix
    for i in range(1, first_length):
        for j in range(1, second_length):
            deletion = distance_matrix[i - 1][j] + 1
            insertion = distance_matrix[i][j - 1] + 1
            substitution = distance_matrix[i - 1][j - 1]
            if first[i - 1] != second[j - 1]:
                substitution += 1
            distance_matrix[i][j] = min(insertion, deletion, substitution)
    print distance_matrix
    return distance_matrix[first_length - 1][second_length - 1]

if __name__ == "__main__":
    ld = LevenshteinDistance()
    print(ld.edit('瓦罐蹄膀饭', '瓦罐焖蹄饭'))  # Prints 2
    print(ld.edit('', 'a'))  # Prints 1
    print(ld.edit('b', ''))  # Prints 1
    print(ld.edit('', ''))  # Prints 0
    print(ld.edit('杭椒小炒肉面', '外婆小肉面'))  # Prints 3
    print(ld.edit('外婆小肉面', '杭椒小炒肉面'))
    # Example:
    print(edit_dist('杭椒小炒肉面', '外婆小肉面'))  # Prints 3
    print(edit_dist('123', '234'))
    print(levenshtein('123', '234'))



