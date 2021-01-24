from django.db import transaction

from judge.submissions.code_executors.cpp_docker_executor import CppDockerExecutor
from judge.submissions.code_executors.java_docker_executor import JavaDockerExecutor
from judge.submissions.code_executors.python_docker_executor import PythonDockerExecutor
from judge.submissions.models import Submission, SubmissionResult
from judge.submissions.models import SubmissionTestResultType
from judge.submissions.services.temp_io import TempIoService


class SubmissionsService:
    def __init__(self):
        self.temp_io_service = TempIoService()

    def __calculate_total_score(self, test_results):
        max_points = 100
        correct_answer_type_id = SubmissionTestResultType.correct_answer().id
        non_zero_tests = [test_result for test_result in test_results if not test_result.is_zero_test]
        correct_tests = len(
            [
                test_result
                for test_result in non_zero_tests
                if test_result.test_result_type_id == correct_answer_type_id
            ])
        total_tests = len(non_zero_tests)
        return int(correct_tests * max_points / total_tests)

    def __get_executor(self, submission_type):
        name_to_executor = {
            'python': PythonDockerExecutor(),
            'c++': CppDockerExecutor(),
            'java': JavaDockerExecutor(),
        }

        return name_to_executor[submission_type.name.lower()]

    def __get_tests(self, submission):
        return [
            {
                'in': test.input,
                'out': test.expected_output,
                'id': test.id,
                'is_zero_test': test.is_zero_test,
            }
            for test in submission.code_task.tasktest_set.all()
        ]

    @transaction.atomic
    def __save_submission_result(self, submission, test_results, is_retest):
        submission_result = SubmissionResult(
            code_submission=submission,
            is_retest=is_retest,
            total_score=self.__calculate_total_score(test_results),
        )
        submission_result.save()
        for test_result in test_results:
            test_result.submission_result = submission_result
            test_result.save()

    def __update_processing_state(self, submission, state):
        submission.processing_state = state
        submission.save()

    def judge_submission(self, submission_id, is_retest):
        submission = Submission.objects.filter(pk=submission_id).first()
        self.__update_processing_state(submission, Submission.PROCESSING_STATE_JUDGING_IN_PROGRESS)

        file_path = self.temp_io_service.get_temp_file()
        with open(file_path, 'w') as code_file:
            code_file.write(submission.code)

        executor = self.__get_executor(submission.type)
        tests = self.__get_tests(submission)
        (time_limit, memory_limit) = self.__get_limits(submission)
        try:
            test_results = executor.execute(file_path, tests, time_limit, memory_limit)

            self.__save_submission_result(submission, test_results, is_retest)
        except Exception as err:
            pass

        self.__update_processing_state(submission, Submission.PROCESSING_STATE_JUDGED)

    def __get_limits(self, submission):
        code_task = submission.code_task
        return (code_task.time_limit_in_ms, code_task.memory_limit_in_bytes)
