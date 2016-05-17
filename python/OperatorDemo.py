#!/usr/bin/env python
# coding=utf-8

if __name__ == "__main__":
    print 1 + (2 * 3) / 2.0 + 2 ** 3 + 5 / 2.0 + 10 % 3

    print [1, 2, 3] + [4, 5]
    print ['hello'] * 3
    print 3 in [1, 2, 5]
    for i in [1, 3, 5]:
        print i

    a = set('abracadabra')
    b = set('alacede')
    print (a - b)  # 属于a 不属于 b
    print (a | b)  # 属于a 或者 b
    print (a & b)  # 属于 a和b
    print (a ^ b)  # 属于a或者b，但不能同时属于a和b

    print 0 == True
    print 12 > 115
    print '12' <> '12'
