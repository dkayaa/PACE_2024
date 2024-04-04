
from algorithm import getCrossings

def RRLO1(po, k, V_2):
    size = len(V_2)
    for a in range(size):
        comparable = True
        for b in range(size):
            if a == b:
                continue
            if b not in po[a] and a not in po[b]:
                comparable = False
                break
        if comparable:
            V_2.pop(a)
            po.pop(a, None)
            for c in range(V_2):
                if a == c:
                    continue
                po[c].remove(a)

def RRLO2(po, k, V_2):
    size = len(V_2)
    for a in range(size):
        for b in range(a, size):
            if incomparable(po, a, b) and not isDependent(po, a, b, V_2):
                i = getCrossings(V_2[a], V_2[b])
                j = getCrossings(V_2[b], V_2[a])
                if (i < j):
                    po[a].append(b)
                    k -= i
                else:
                    po[b].append(a)
                    k -= j

def RRlarge(po, k, V_2):
    size = len(V_2)
    for a in range(size):
        for b in range(a, size):
            i = getCrossings(V_2[a], V_2[b])
            j = getCrossings(V_2[b], V_2[a])
            if i > k and j > k:
                return False
            elif i > k:
                k -= j
                po[b].append(a)
            elif j > k:
                k -= i
                po[a].append(b)



def branching_algorithm(po, k, V_2):
    prevK = -1
    prevSize = -1
    while prevK != k or prevSize != len(V_2):
        
        prevK = k
        prevSize = len(V_2)
       
        # RRLO1
        size = len(V_2)
        for a in range(size):
            comparable = True
            for b in range(size):
                if a == b:
                    continue
                if b not in po[a] and a not in po[b]:
                    comparable = False
                    break
            if comparable:
                V_2.pop(a)
                po.pop(a, None)
                for c in range(V_2):
                    if a == c:
                        continue
                    po[c].remove(a)
        
        # RRL02
        size = len(V_2)
        for a in range(size):
            for b in range(a, size):
                if incomparable(po, a, b) and not isDependent(po, a, b, V_2):
                    i = getCrossings(V_2[a], V_2[b])
                    j = getCrossings(V_2[b], V_2[a])
                    if (i < j):
                        po[a].append(b)
                        k -= i
                    else:
                        po[b].append(a)
                        k -= j

        # RRlarge
        size = len(V_2)
        for a in range(size):
            for b in range(a, size):
                i = getCrossings(V_2[a], V_2[b])
                j = getCrossings(V_2[b], V_2[a])
                if i > k and j > k:
                    return False
                elif i > k:
                    k -= j
                    po[b].append(a)
                elif j > k:
                    k -= i
                    po[a].append(b)
    
    if (k < 0):
        return False
    size = len(V_2)
    for v_1 in range(size):
        for v_2 in range(v_1, size):
            i = getCrossings(V_2[v_1], V_2[v_2])
            j = getCrossings(V_2[v_2], V_2[v_1])
            isIncomparable = incomparable(po, v_1, v_2)
            if isIncomparable and i + j >= 4:
                po1 = po.copy()
                po1[v_1].append(v_2)
                po[v_2].append(v_1)
                return branching_algorithm(po, k - i,V_2) or branching_algorithm(po1, k-j,V_2)
            elif isIncomparable and (i == 1 and j == 2) or (i == 2 and j == 1) and isDependent(po,v_1,v_2):
                po1 = po.copy()
                po1[v_1].append(v_2)
                po[v_2].append(v_1)
                return branching_algorithm(po, k-i, V_2) or branching_algorithm(po1, k-j, V_2)
            elif i == 1 and j == 1:
                po[v_1].append(v_2)
                return branching_algorithm(po, k-1, V_2)
            else:
                return True


def incomparable(po, v_1, v_2):
    if v_2 not in po[v_1] and v_1 not in po[v_1]:
        return True
    return False

def isDependent(po, v_1, v_2, V_2):
    for vertex in range(len(V_2)):
        if (v_1 not in po[vertex] and vertex not in po[v_1]) or (v_2 not in po[vertex] and vertex not in po[v_2]):
            return True
    return False

    
    


