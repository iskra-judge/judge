import re
from math import sqrt

from judge.similarity.checkers.base.base_similarity_checker import BaseSimilarityChecker


class CosineSimilarityChecker(BaseSimilarityChecker):
    FEATURE_PATTERN = '[a-zA-Z0-9$_]+'

    def check_similarity(self, str1, str2):
        str1_terms = self.get_terms(str1)
        if not str1_terms:
            return 0

        str2_terms = self.get_terms(str2)
        if not str2_terms:
            return 0

        if not str2_terms:
            return 0

        return self.get_cosine(self.get_frequency(str1_terms), self.get_frequency(str2_terms))

    def get_cosine(self, fregs1, freqs2):
        up = sum(fregs1[key] * freqs2[key] for key in fregs1.keys() if key in freqs2)
        a = self.get_quadratic_sum(fregs1.values())
        b = self.get_quadratic_sum(freqs2.values())
        return up / sqrt(a * b)

    def get_frequency(self, terms):
        frequencies_map = {}
        for term in terms:
            if term not in frequencies_map:
                frequencies_map[term] = 0
            frequencies_map[term] += 1
        return frequencies_map

    def get_terms(self, text):
        return re.findall(self.FEATURE_PATTERN, text)

    def get_quadratic_sum(self, values):
        result = 0
        for x in values:
            result += x * x
        return result
