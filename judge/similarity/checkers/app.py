from judge.similarity.checkers.cosine_similarity_checker import CosineSimilarityChecker
from judge.similarity.checkers.jaccard_similarity_checker import JaccardSimilarityChecker
from judge.similarity.checkers.longest_common_subsequence_similarity_checker import \
    LongestCommonSubsequenceSimilarityChecker


def get_str_from_file(filename):
    with open(filename, 'r') as file:
        return file.read()


def get_str1():
    # filename = 'sample_task.cpp'
    # filename = 'sample_task_wrong.py'
    # filename = 'test_tasks/task1.py'
    filename = 'test_tasks/task1.py'
    return get_str_from_file(f'/mnt/repos/personal/tasks/sum/{filename}')


def get_str2():
    # filename = 'sample_task2.cpp'
    # filename = 'sample_task.py'
    # filename = 'test_tasks/task2.py'
    filename = 'test_tasks/task2.py'
    return get_str_from_file(f'/mnt/repos/personal/tasks/sum/{filename}')


str1 = get_str1()
str2 = get_str2()

lcs_checker = LongestCommonSubsequenceSimilarityChecker()
jaccard_checker = JaccardSimilarityChecker()
cosine_checker = CosineSimilarityChecker()

print(f'{lcs_checker.check_similarity(str1, str2):.2f} LCS')
print(f'{jaccard_checker.check_similarity(str1, str2):.2f} Jaccard')
print(f'{cosine_checker.check_similarity(str1, str2):.2f} Cosine')
