from __future__ import print_function
from docopt import docopt
from itertools import chain, combinations
import ast
import functools
import operator
import sys

__doc__ ="""
Private Marginals.

Usage:
    main.py accu  --db=<db> --query=<query>
    main.py priv --epsilon=<epsilon> --delta=<delta> --db=<db> --query_dist=<query_dist>
"""
class ConvexSet(object):
    def __init__(self, d, k):
        self.d = d
        self.k = k

    def __repr__(self):
        return "d^k = {}^{}".format(self.d, self.k)

def accu_compute(records, query):
    count = 0
    for rec in records:
        if all([rec[col] == val for col, val in query.iteritems()]):
            count += 1
    return count

def translate(i, forward=True):
    if i == 1:
        return 1
    elif forward and i == 0:
        return -1
    elif not forward and i == -1:
        return 0
    else:
        print("Internal translation error: {}".format(i), sys.stderr)
        exit(1)

def db_read(filename):
    with open(filename, 'r') as fp:
        records = []
        for line in fp:
            records.append(map(int, line.strip().split()))
    return records, len(records[0]), len(records)

def query_parse(query_string):
    return ast.literal_eval(query_string)

def prod(iterable):
    return reduce(operator.mul, iterable, 1)

def parity(records, indices):
    return sum(prod([rec[i] for i in indices]))

def alpha(k, beta, T):
    return 2 ** -k * prod([beta[i] for i in T])

def marg_query_to_parity_query(query):
    def powerset(S):
        xs = list(S)
        return chain.from_iterable(combinations(xs, n) for n in range(len(xs) + 1))
    k = len(subset)
    return 1 #lambda records sum([alpha(k, query, T) for T in powerset(subsets)])


def read(filename):
    with open(filename, 'r') as fp:
        records = []
        for line in fp:
            records.append(map(int, line.strip().split()))
    return records, len(records[0]), len(records)

def priv_compute(db, dist, epsilon=20, delta=0.8):
    def c(eps, delt):
        from math import sqrt, log    
        return (1 + sqrt(2 * log(1 / delt))) / eps
    k = len(dist)
    T = 4 * len(db) / c(epsilon, delta) / d ** (3k / 4.0)
    print(db, dist, epsilon, delta, sep='/')

def noise(epsilon, delta, sigma, m):
    pass

if __name__ == '__main__':
    argd = docopt(__doc__)
    records, dim, num_records = db_read(argd['--db'])
    clean_records = [[translate(num, forward=True) for num in rec]
                                                   for rec in records]
    if argd['accu']:
        query = query_parse(argd['--query'])
        if not query:
            print("invalid query distribution", file=sys.stderr)
            sys.exit(1)
        clean_query = {index:translate(num, forward=True)
                       for index, num in query.iteritems()}
        count = accu_compute(clean_records, clean_query)
    elif argd['priv']:
        q_dist = query_parse(argd['--query_dist'])
        count = priv_compute(clean_records,
                            dim,
                            num_records,
                            q_dist,
                            epsilon=argd['--epsilon'], delta=argd['--delta'])
    print("Count is {}".format(count))
