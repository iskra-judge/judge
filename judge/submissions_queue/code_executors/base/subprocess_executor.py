import io
import subprocess

from judge.submissions_queue.code_executors.base.base_executor import BaseExecutor
from judge.submissions_queue.common.test_results import TestResult, TestResultType


class SubprocessExecutor(BaseExecutor):
    def execute_test(self, code_path, input):
        process = subprocess.Popen(
            ['python', code_path],
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        stdout = process.communicate(input=input.encode())[0]
        process.kill()
        process.terminate()
        if process.returncode:
            raise RuntimeError(stdout.strip())
        print(stdout.strip())
        return subprocess.CompletedProcess(
            '',
            process.returncode,
            stdout=stdout,
            stderr=stdout,
        )

    def build_test_result(self, execution_result, expected_output):
        if execution_result.returncode:
            return TestResult(
                False,
                TestResultType.RuntimeError,
                execution_result.stderr.decode()
            )
        is_successful = execution_result.stdout.decode().strip() == expected_output.strip()
        return TestResult(
            is_successful,
            TestResultType.CorrectAnswer
            if is_successful
            else TestResultType.WrongAnswer,
            execution_result.stdout.decode().strip()
        )
