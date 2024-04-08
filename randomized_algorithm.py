
def construct_naive_interval(V_1, V_2, g):
    interval = []
    for i in range(V_2):
        min = -1
        max = -1
        for j in range(V_1):
            if V_2[i] in g[V_1[j]]:
                if min > j or min == -1:
                    min = j
                if max < j or max == -1:
                    max = j
    interval.push_back((min, max))

def construct_complex_interval(V_1, V_2, g):
    interval = []

    max = [-1 for i in range(len(V_2))]
    min = [len(V_1) for i in range(len(V_2))]
    for i in range(V_1):
        p1 = []
        p2 = []
        p3 = []
        for a in g[V_1[i]]:
            if len(g[a]) == 1:
                p2.push_back((a, V_1[i], 0))
                p2.push_back((a, V_1[i], 1))
            elif g[a][len[g[a]] - 1] == V_1[i]:
                p1.push_back((a, V_1[i], 1))
            elif g[a][0] == V_1[i]:
                p3.push_back((a, V_1[i], 0))
        interval += p1 + p2 + p3


def dynamic_branching(interval, complex_interval, k, V_2, c):
    

