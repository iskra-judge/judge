from judge.similarity.checkers.base.base_similarity_checker import BaseSimilarityChecker


class LongestCommonSubsequenceSimilarityChecker(BaseSimilarityChecker):
    def check_similarity(self, str1, str2):
        str1 = self.remove_blank(str1)
        if self.is_empty(str1):
            return 0

        str2 = self.remove_blank(str2)
        if self.is_empty(str2):
            return 0

        return 2.0 * self.get_lcs(str1, str2) / (len(str1) + len(str2))

    def get_lcs(self, str1, str2):
        dp = [[0] * (len(str2) + 1) for _ in range(len(str1) + 1)]
        for i in range(1, len(str1) + 1):
            for j in range(1, len(str2) + 1):
                if str1[i - 1] == str2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i][j - 1], dp[i - 1][j])
        return dp[-1][-1]
