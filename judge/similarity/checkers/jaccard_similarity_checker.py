from judge.similarity.checkers.base.base_similarity_checker import BaseSimilarityChecker


class JaccardSimilarityChecker(BaseSimilarityChecker):
    def check_similarity(self, str1, str2):
        str1_set = set(str1.split())
        str2_set = set(str2.split())
        result_set = str1_set.intersection(str2_set)
        return float(len(result_set)) / (len(str1_set) + len(str2_set) - len(result_set))
