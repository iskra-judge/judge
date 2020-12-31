import tarfile
import tempfile
import uuid
from os import chdir, remove
from os.path import basename, join, dirname

import docker
import shutil

from judge.submissions_queue.code_executors.base_executor import BaseExecutor
from judge.submissions_queue.common.test_results import TestResult, TestResultType


class DockerExecutor(BaseExecutor):
    code_file_path = f'/tmp/code_file-{uuid.uuid4()}.py'
    test_file_path = f'/tmp/test.txt'

    def __init__(self):
        self.client = docker.from_env()
        self.container = self.client.containers.create(
            'python:slim',
            command='sh -c "tail -f /dev/null"')

    def copy_to(self, source, destination):
        chdir(dirname(source))
        local_dest_name = join(dirname(source), basename(destination))
        if local_dest_name != source:
            shutil.copy2(source, local_dest_name)
        dst_name = basename(destination)
        tar_path = local_dest_name + '.tar'

        tar = tarfile.open(tar_path, mode='w')
        try:
            tar.add(dst_name)
        finally:
            tar.close()

        data = open(tar_path, 'rb').read()
        self.container.put_archive(dirname(destination), data)

        remove(tar_path)
        remove(local_dest_name)

    def apply_template(self, code):
        return f'''
import sys
fd = open('{self.test_file_path}')
sys.stdin = fd
{code}
'''

    def before_execute(self, code_path, *args, **kwargs):
        self.container.start()
        self.copy_to(code_path, self.code_file_path)
        return super().before_test_execute(code_path, *args, **kwargs)

    def after_execute(self, *args, **kwargs):
        self.container.stop()
        self.container.wait()
        self.container.remove()

    def prepare_test_input(self, test_input):
        file_path = join(tempfile.gettempdir(), 'test.txt')
        with open(file_path, 'w') as file:
            file.write(test_input)
        self.copy_to(file_path, self.test_file_path)

    def execute_test(self, code_path, test_input):
        self.prepare_test_input(test_input)
        cmd = f'python {self.code_file_path}'
        return self.container.exec_run(cmd)

    def build_test_result(self, execution_result, expected_output):
        if execution_result.exit_code:
            return TestResult(
                False,
                TestResultType.RuntimeError,
                execution_result.output.decode()
            )
        is_successful = execution_result.output.decode().strip() == expected_output.strip()
        return TestResult(
            is_successful,
            TestResultType.CorrectAnswer
            if is_successful
            else TestResultType.WrongAnswer,
            execution_result.output.decode().strip()
        )
