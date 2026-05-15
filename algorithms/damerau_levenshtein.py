def damerau_levenshtein_distance(
    str1: str, str2: str, best_distance_found: int
) -> int | None:
    """
    Calculate the Damerau-Levenshtein distance between two words.

    Technique: Tabulation.
    """

    table = [[0 for _ in range(len(str1) + 1)] for _ in range(len(str2) + 1)]

    for i in range(len(str1) + 1):
        table[0][i] = i

    for j in range(len(str2) + 1):
        table[j][0] = j

    for j in range(1, len(str2) + 1):
        row_min = table[j][0]
        for i in range(1, len(str1) + 1):
            if str2[j - 1] == str1[i - 1]:
                table[j][i] = table[j - 1][i - 1]

            else:
                cost = 1 + min(
                    table[j][i - 1],
                    table[j - 1][i - 1],
                    table[j - 1][i],
                )

                if (
                    (i > 1 and j > 1)
                    and str2[j - 2] == str1[i - 1]
                    and str1[i - 2] == str2[j - 1]
                ):
                    cost = min(1 + table[j - 2][i - 2], cost)

                table[j][i] = cost

            if table[j][i] < row_min:
                row_min = table[j][i]

        if row_min > best_distance_found:
            return None

    return table[-1][-1]


