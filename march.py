import itertools
def equal_sum_disjoint_subsets(values):
    n = len(values)
    if n < 2:
        return None

    sums = {}
    for mask in range(1, 1 << n):
        s = sum(values[i] for i in range(n) if mask >> i & 1)
        if s in sums:
            for prev in sums[s]:
                if prev & mask == 0:
                    a = [values[i] for i in range(n) if prev >> i & 1]
                    b = [values[i] for i in range(n) if mask >> i & 1]
                    return a, b
            sums[s].append(mask)
        else:
            sums[s] = [mask]
    return None


def find_impossible_10_element_list_pruned(max_calls=200000):
    """Find first 10-number list from [100..1] without equal-sum disjoint subsets."""
    calls = 0

    def dfs(next_value, chosen):
        nonlocal calls
        if calls >= max_calls:
            raise RuntimeError(f"Reached {max_calls} recursive checks; none found yet")

        

        if len(chosen) == 10:
            calls += 1
            if equal_sum_disjoint_subsets(chosen) is None:
                return list(chosen)
            return None

        # If a prefix already has a solution, its supersets will also have a solution => prune.
        if chosen and equal_sum_disjoint_subsets(chosen) is not None:
            return None


        for x in range(next_value, 0, -1):
            chosen.append(x)
            res = dfs(x - 1, chosen)
            chosen.pop()
            if res is not None:
                return res

        return None

    return dfs(100, [])


if __name__ == "__main__":
    try:
        impossible = find_impossible_10_element_list_pruned(max_calls=1)
        print("Impossible 10-element list:", impossible)
    except RuntimeError as err:
        print(err)