from judge.submissions_queue.code_executors.docker_executor import DockerExecutor
from judge.submissions_queue.common.submissions_common import get_tests


def solve():
    file_path = "E:\\repos\\personal\\tasks\\sum\\sample_task.py"
    tests_dir_path = "E:\\repos\\personal\\tasks\\sum"
    tests = get_tests(tests_dir_path)
    executor = DockerExecutor()
    test_results = executor.execute(file_path, tests)

    [print(x) for x in test_results]


solve()
