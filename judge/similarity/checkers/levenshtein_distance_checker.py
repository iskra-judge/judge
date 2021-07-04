import re
from math import sqrt

from judge.similarity.checkers.base.base_similarity_checker import BaseSimilarityChecker


class LevenshteinDistanceChecker(BaseSimilarityChecker):
    def check_similarity(self, str1, str2):
        str1 = self.remove_blank(str1)
        if self.is_empty(str1):
            return 0

        str2 = self.remove_blank(str2)
        if self.is_empty(str2):
            return 0

        max_len = float(max(len(str1),  len(str2)))
        return (max_len - self.get_levenshtein_distance(str1, str2)) / max_len

    @staticmethod
    def get_levenshtein_distance(str1, str2):
        dp = [[0] * (len(str2) + 1) for _ in range(len(str1) + 1)]
        n = len(str1)
        m = len(str2)

        for i in range(n):
            dp[i][0] = i
        for i in range(m):
            dp[0][i] = i

        for i in range(1, n):
            for j in range(1, m):
                if str1[i - 1] == str2[j - 1]:
                    dp[i][j] = min(
                        dp[i - 1][j - 1],
                        dp[i - 1][j] + 1,
                        dp[i][j - 1] + 1,
                    )
                else:
                    dp[i][j] = 1 + min(
                        dp[i - 1][j],
                        dp[i][j - 1],
                        dp[i - 1][j - 1],
                    )
        return dp[-1][-1]
