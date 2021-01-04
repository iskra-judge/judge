from abc import ABC, abstractmethod


class BaseSimilarityChecker(ABC):
    @abstractmethod
    def check_similarity(self, str1, str2):
        pass

    def is_empty(self, a):
        return not bool(a)

    def remove_blank(self, before):
        if self.is_empty(before):
            return before

        return ''.join(x for x in before if x)
