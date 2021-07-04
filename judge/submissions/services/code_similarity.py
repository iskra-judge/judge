from judge.similarity.checkers.cosine_similarity_checker import CosineSimilarityChecker
from judge.similarity.checkers.jaccard_similarity_checker import JaccardSimilarityChecker
from judge.similarity.checkers.levenshtein_distance_checker import LevenshteinDistanceChecker
from judge.similarity.checkers.longest_common_subsequence_similarity_checker import \
    LongestCommonSubsequenceSimilarityChecker
from judge.submissions.models import Submission, SubmissionSimilarity


class CodeSimilarityService:
    MINIMAL_SUSPICIOUS_COSINE_RESULT = 0.6
    MINIMAL_SUSPICIOUS_JACCARD_RESULT = 0.6
    MINIMAL_SUSPICIOUS_LCS_RESULT = 0.6
    MINIMAL_SUSPICIOUS_LEVENSHTEIN_DISTANCE_RESULT = 0.6

    def __init__(self):
        self.cosine_similarity_checker = CosineSimilarityChecker()
        self.jaccard_similarity_checker = JaccardSimilarityChecker()
        self.lcs_similarity_checker = LongestCommonSubsequenceSimilarityChecker()

    def check_similarity(self, submission_id):
        submission = Submission.objects.get(pk=submission_id)
        submissions_to_check = Submission.objects \
            .filter(code_task_id=submission.code_task_id, type_id=submission.type_id) \
            .exclude(user_id=submission.user_id)

        for submission_to_check in submissions_to_check:
            cosine_result = self.cosine_similarity_checker.check_similarity(submission.code, submission_to_check.code)
            jaccard_result = self.jaccard_similarity_checker.check_similarity(submission.code, submission_to_check.code)
            lcs_result = self.lcs_similarity_checker.check_similarity(submission.code, submission_to_check.code)

            if self.MINIMAL_SUSPICIOUS_LCS_RESULT <= lcs_result \
                    or self.MINIMAL_SUSPICIOUS_JACCARD_RESULT <= jaccard_result \
                    or self.MINIMAL_SUSPICIOUS_COSINE_RESULT <= cosine_result:
                submission_similarity = SubmissionSimilarity(
                    submission1_id=submission.id,
                    submission2_id=submission_to_check.id,
                    cosine_similarity=cosine_result * 100,
                    lcs_similarity=lcs_result * 100,
                    jaccard_similarity=jaccard_result * 100,
                )
                submission_similarity.save()
