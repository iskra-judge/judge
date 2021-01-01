from judge.submissions_queue.code_executors.cpp_docker_executor import CppDockerExecutor
from judge.submissions_queue.common.submissions_common import get_tests
from judge.submissions_queue.code_executors.python_docker_executor import PythonDockerExecutor


def solve():
    tests_dir_path = "E:\\repos\\personal\\tasks\\sum"
    tests = get_tests(tests_dir_path)

    executors = [
        # ('PY', PythonDockerExecutor(), "E:\\repos\\personal\\tasks\\sum\\sample_task.py"),
        ('CPP', CppDockerExecutor(), "E:\\repos\\personal\\tasks\\sum\\sample_task.cpp"),
    ]

    for (name, executor, file_path) in executors:
        print(f'Running {name} executor')
        test_results = executor.execute(file_path, tests)
        [print(x) for x in test_results]


solve()
