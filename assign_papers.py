# Paper matching for 692C. Justin Payan Sept. 2021.

# Probabilistic Serial from Dominick Peters at https://gist.github.com/DominikPeters/943e102c6d633e4adb024b086b5b5042
# Birkhoff from Jeffrey Finkelstein at https://github.com/jfinkels/birkhoff
from fractions import Fraction
import numpy as np
from birkhoff import birkhoff_von_neumann_decomposition
import random


def probabilistic_serial(profile):
    "input is a list of preference lists"
    N = range(len(profile))  # agents
    O = range(len(profile[0]))  # items
    supply = {o: Fraction(1, 1) for o in O}
    allocation = {(i, o): Fraction(0, 1) for i in N for o in O}
    while any(supply.values()):
        # in each iteration, at least one remaining item is fully depleted
        eating = {}
        eaters = {o: 0 for o in O}  # number of agents eating each item
        for i in N:
            o_ = next((o for o in profile[i] if supply[o]))
            eating[i] = o_
            eaters[o_] += 1
        # how much time until the first remaining item is depleted
        time = min(supply[o] / eaters[o] for o in O if supply[o] and eaters[o])
        for i in N:
            allocation[i, eating[i]] += time
            supply[eating[i]] -= time

        float_alloc = []
        for i in range(len(profile)):
            float_alloc.append([float(allocation[i, o]) for o in range(len(profile[0]))])
    return float_alloc


def sample_allocation(birkhoff_von_neumann_decomp):
    coeffs, perm = zip(*birkhoff_von_neumann_decomp)
    print(sum(coeffs))
    # assert sum(coeffs) == 1
    idx = np.where(np.random.multinomial(1, coeffs))[0][0]
    return perm[idx]


def convert_to_rankings(scores):
    n = len(scores)
    x = []
    for i in range(n):
        x.append([int(i) for i in scores[i]])
    x = np.array(x)
    total_value_per_paper = np.sum(x, axis=0)

    # Sort first on inverse of the score (so from highest to lowest) and second on how much other people want
    # each paper
    final_rankings = []
    for i in range(n):
        sort_keys = [(idx, -1*score, total_value_per_paper[idx] - score) for idx, score in enumerate(x[i].tolist())]
        sorted_elts = sorted(sort_keys, key=lambda x: (x[1], x[2]))
        print(sorted_elts)
        final_rankings.append([x[0] for x in sorted_elts])
    return final_rankings


def load_prefs(fname):
    names_map = {}
    original_scores = []
    with open(fname, 'r') as f:
        for idx, l in enumerate(f):
            line = l.strip().split(",")
            names_map[idx] = line[0]
            original_scores.append(line[1:])
    prefs = convert_to_rankings(original_scores)
    return prefs, original_scores, names_map


def load_goods(fname):
    goods_map = {}
    with open(fname, 'r') as f:
        for idx, l in enumerate(f):
            goods_map[idx] = l.strip()
    return goods_map


if __name__ == '__main__':
    prefs, original_scores, names_map = load_prefs('prefs.csv')
    goods_map = load_goods('goods.txt')

    print(prefs)

    allocation = probabilistic_serial(prefs)
    # print("Randomized allocation from serial eating procedure: ", allocation)
    bvn = birkhoff_von_neumann_decomposition(np.array(allocation))
    # print("\nBirkhoff von Neumann decomposition: ")
    # for coefficient, permutation_matrix in bvn:
    #     print('coefficient:', coefficient)
    #     print('permutation matrix:', permutation_matrix)

    # alloc = sample_allocation(bvn)
    # print("\nSampled allocation: ")
    # for i in range(len(names_map)):
    #     which_good_assigned = np.where(alloc[i, :])[0][0]
    #     print("{} is assigned {}, which they scored {}".format(names_map[i], goods_map[which_good_assigned],
    #                                                            original_scores[i][which_good_assigned]))

    k = 5
    print("\nTop {} allocations".format(k))
    top_k = sorted(bvn, key=lambda x: x[0], reverse=True)[:k]
    for coeff, alloc in top_k:
        print()
        print("Probability: %.3f" % coeff)
        for i in range(len(names_map)):
            which_good_assigned = np.where(alloc[i, :])[0][0]
            print("{} is assigned {}, which they scored {}".format(names_map[i], goods_map[which_good_assigned],
                                                                   original_scores[i][which_good_assigned]))
        print()



