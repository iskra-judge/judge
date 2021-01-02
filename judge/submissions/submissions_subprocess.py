from judge.submissions.code_executors.base.subprocess_executor import SubprocessExecutor
from judge.submissions.common.submissions_common import get_tests


def solve():
    file_path = "E:\\repos\\personal\\tasks\\sum\\sample_task.py"
    tests_dir_path = "E:\\repos\\personal\\tasks\\sum"
    tests = get_tests(tests_dir_path)
    executor = SubprocessExecutor()
    test_results = executor.execute(file_path, tests)

    [print(x) for x in test_results]


solve()
