from judge.submissions_queue.common.submissions_common import get_tests
from judge.submissions_queue.code_executors.python_docker_executor import PythonDockerExecutor


def solve():
    file_path = "E:\\repos\\personal\\tasks\\sum\\sample_task.py"
    tests_dir_path = "E:\\repos\\personal\\tasks\\sum"
    tests = get_tests(tests_dir_path)
    executor = PythonDockerExecutor()
    test_results = executor.execute(file_path, tests)

    [print(x) for x in test_results]


solve()
