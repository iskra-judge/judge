from judge.submissions.code_executors.cpp_docker_executor import CppDockerExecutor
from judge.submissions.code_executors.java_docker_executor import JavaDockerExecutor
from judge.submissions.common.submissions_common import get_tests
from judge.submissions.code_executors.python_docker_executor import PythonDockerExecutor


def solve():
    tests_dir_path = 'E:\\repos\\personal\\tasks\\sum'
    # tests_dir_path = '/mnt/e/repos/personal/tasks/sum'
    tests = get_tests(tests_dir_path)

    # Windows
    executors = [
        # ('PY', PythonDockerExecutor(), 'E:\\repos\\personal\\tasks\\sum\\sample_task.py'),
        # ('CPP', CppDockerExecutor(), 'E:\\repos\\personal\\tasks\\sum\\sample_task.cpp'),
        ('Java', JavaDockerExecutor(), 'E:\\repos\\personal\\tasks\\sum\\sample_task.java'),
    ]
    # Linux
    # executors = [
    #     ('PY', PythonDockerExecutor(), '/mnt/e/repos/personal/tasks/sum/sample_task.py'),
    #     ('CPP', CppDockerExecutor(), '/mnt/e/repos/personal/tasks/sum/sample_task.cpp'),
    # ]

    for (name, executor, file_path) in executors:
        print(f'Running {name} executor')
        test_results = executor.execute(file_path, tests)
        [print(x) for x in test_results]

