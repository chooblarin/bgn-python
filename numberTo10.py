#!/usr/bin/python
# -*- coding utf-8 -*-

from itertools import permutations, product
from fractions import Fraction
import re

# 入力
p = [1,1,5,8]

# オペレーター
operators = {
    '+': lambda a,b: a+b,
    '-': lambda a,b: a-b,
    '*': lambda a,b: a*b,
    '/': lambda a,b: Fraction(a,b)
}

# 数字の順列
nums_ = list(permutations(p))
nums = sorted(set(nums_), key=nums_.index)

# 演算子の順列（重複あり）
ops = list(product(operators.keys(),repeat=3))

# 演算子の正規表現
opr = re.compile('^[\+\-\*\/]$')

# 数字と演算子の組み合わせ
def create_expr(n, o):
    rtn = []
    rtn.append(list(n)+list(o))
    rtn.append([n[0],n[1],o[0],n[2],n[3],o[1],o[2]])
    rtn.append([n[0],n[1],o[0],n[2],o[1],n[3],o[2]])
    return rtn

# 逆ポーランド記法計算
def calc_rpn(exp):
    stck = []
    expr = list(exp)[:]
    expr.reverse()

    for x in exp:
        if(type(x) is int):
            stck.append(x)

        elif(opr.match(x)):
            try:
                n1 = stck.pop()
                n2 = stck.pop()
                n3 = operators[x](n2, n1)
                stck.append(n3)
            except(IndexError, ZeroDivisionError):
                return None

    return stck.pop()


if __name__ == '__main__':
    cs = [create_expr(n,o) for n,o in product(nums,ops)]
    exprs = reduce(lambda x,y: x+y, cs)
    result = [(expr, calc_rpn(expr)) for expr in exprs]
    print filter(lambda n: n[1] == 10, result)
