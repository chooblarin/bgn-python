# -*- coding: utf-8 -*-
from random import randint, random
import numpy as np
from itertools import combinations

NUM_NODE = 10000 # ノード数
MINI_DEG = 3 # 最小の次数
MAX_DEG = 90 # 最大の次数
GAMMA = 4 # 次数分布のベキ指数

class Node(object):
    """ ノードクラス
    """
    @staticmethod
    def connect(a, b):
        a.adj_list.add(b.n_id)
        b.adj_list.add(a.n_id)
        a.degree += 1
        b.degree += 1

    def __init__(self, n_id, k=0):
        self.n_id = n_id
        self.degree = k
        self.adj_list = set()

    def connect_to(self, to):
        Node.connect(self, to)

    def isconnected(self, x):
        return x.n_id in self.adj_list

class Graph(object):
    """ グラフクラス
    """
    def __init__(self):
        self.nodes = []

    def add_node(n):
        self.nodes.append(n)

def get_pow_deg(gamm, dmin, dmax):
    """ 境界つきのベキ分布次数をランダムに返す
    """
    pow_seq = [x ** -gamm for x in range(dmin, dmax)]
    h = sum(pow_seq)
    r = random()
    p = 0
    d = dmin
    while True:
        p += d ** -gamm
        if r < p/h:
            return d
        else: 
            d += 1

def pow_degree(n, gamm, dmin, dmax):
    """ 境界付きのベキ分布をつくる
    """
    deg_l = []
    for i in range(n):
        elem = get_pow_deg(gamm, dmin, dmax)
        deg_l.append(elem)

    deg_l.sort(reverse=True)
    rslt = np.array(deg_l, dtype=np.int)
    return rslt

def someone_in_set(others):
    """ 集合から要素をランダムに返す
    """
    cp = others.copy()
    r = randint(1, len(cp))
    for i in range(r):
        e = cp.pop()
    return e

def calc_cn(z, li, ns):
    """ 普及率Cnを計算
    """
    cmb = list(combinations(li, 2)) # 加入者の組み合わせ
    lsum = 0
    for a,b in cmb:
        if ns[a].isconnected(ns[b]):
            lsum += 1

    return 2.0 * lsum / z


def create_social_g(n, gamm, dmin, dmax):
    """ 次数がベキ分布のグラフを生成する
    """
    deg = pow_degree(n, gamm, dmin, dmax)
    nodes_l = [Node(i) for i in range(n)]
    nodes = np.array(nodes_l)
    d_sum = 0 # グラフの全次数
    added_nl = [] # 加入者のidリスト
    yet_nl = set(range(n)) # 接続先の無いリンクを持つノードidのセット

    f1 = open('fn_cs.dat', 'w')

    for x in nodes:
        i = x.n_id
        if i % 100 == 0: print i
        added_nl.append(i)
        fn = float(i) / (n - 1)
        d = deg[i]
        d_sum += d
        for j in range(d):
            if d <= x.degree: 
                # リンクが全部繋がっていたら終了
                yet_nl.discard(i)
                break

            cnd = yet_nl.difference(x.adj_list)
            cnd -= set([i])
            if not cnd : break # 接続可能なノードがいなけなれば終了
            # ランダムに相手を選び接続
            num = someone_in_set(cnd)
            who = nodes[num]
            x.connect_to(nodes[num])
            
            if deg[who.n_id] <= who.degree: yet_nl.discard(who.n_id)

            cn = calc_cn(d_sum, added_nl, nodes)
            if cn >= fn: break
        f1.write("%d\t%f\t%f\n" % (i, fn, cn))

    return nodes


## 出力用の補助関数
def to_deg_dist(dlist):
    dst = np.zeros(max(dlist) + 1)
    for i in dlist:
        dst[i] += 1
    return dst

def print_vector(v):
    for i, x in enumerate(v):
        print i, x


def print_dist(dlist):
    dst = to_deg_dist(dlist)
    print_vector(dst)


if __name__ == "__main__":
    nodes = create_social_g(NUM_NODE, GAMMA, MINI_DEG, MAX_DEG)
    degs = [x.degree for x in nodes]
    distrubution = to_deg_dist(degs)
    f2 = open('dist.dat', 'w')
    for i,x in enumerate(distrubution):
        f2.write("%d\t%d\n" % (i, x))
