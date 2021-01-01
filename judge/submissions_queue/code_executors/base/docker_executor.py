import tarfile
import tempfile
import uuid
from abc import abstractmethod
from os import chdir, remove
from os.path import basename, join, dirname

import docker
import shutil

from judge.submissions_queue.code_executors.base.base_executor import BaseExecutor
from judge.submissions_queue.common.test_results import TestResult, TestResultType


def copy_to_container(container, source, destination):
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
    container.put_archive(dirname(destination), data)

    remove(tar_path)
    remove(local_dest_name)


class DockerExecutor(BaseExecutor):
    code_file_path = None
    image_name = None
    run_file_path = '/tmp/run.py'

    def __init__(self):
        self.client = docker.from_env()
        self.container = self.client.containers.create(
            image=self.image_name,
            command=f'sh -c "tail -f /dev/null"',
        )

    def before_execute(self, code_path, *args, **kwargs):
        self.preprocess_code(code_path)
        self.container.start()
        copy_to_container(self.container, code_path, self.code_file_path)
        return super().before_test_execute(code_path, *args, **kwargs)

    def after_execute(self, *args, **kwargs):
        self.container.stop()
        self.container.wait()
        self.container.remove()

    def get_run_file_content(self, test_input):
        return f'''
import subprocess
process = subprocess.Popen(
            {self.get_run_command_params()},
            shell=False,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

stdout = process.communicate(input="""{test_input}""".encode())[0]
try:
    stdout = stdout.decode()
except:
    pass

if process.returncode:
    raise RuntimeError(stdout.strip())
print(stdout.strip())
'''

    def prepare_run_file(self, test_input):
        content = self.get_run_file_content(test_input)
        file_path = join(tempfile.gettempdir(), f'run-{uuid.uuid4()}.py')
        with open(file_path, 'w') as file:
            file.write(content)
        copy_to_container(self.container, file_path, self.run_file_path)

    def execute_test(self, code_path, test_input):
        self.prepare_run_file(test_input)
        commands = [
            self.get_compile_command(),
            self.get_run_command(),
        ]
        command_results = []
        for command in commands:
            if not command:
                continue
            command_result = self.container.exec_run(command, stdin=True, stdout=True, stderr=True)
            if not command_result.exit_code:
                command_results.append(command_result)
                continue
            return command_result

        return command_results[-1] \
            if command_results \
            else None

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

    def get_run_command(self, *args, **kwargs):
        return f'python {self.run_file_path}'

    @abstractmethod
    def get_compile_command(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_run_command_params(self):
        pass

    def preprocess_code(self, code_path):
        pass
