import shutil
import tarfile
from abc import abstractmethod
from os import chdir, remove
from os.path import basename, join, dirname

import docker

from judge.submissions.code_executors.base.base_executor import BaseExecutor
from judge.submissions.models import SubmissionTestResult, SubmissionTestResultType
from judge.submissions.services.temp_io import TempIoService


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
    TIME_LIMIT_ERROR_MESSAGE = 'TIME LIMIT EXCEEDED'

    def __init__(self):
        self.client = None
        self.container = None
        self.temp_io_service = TempIoService()

    def before_execute(self, code_path, *args, **kwargs):
        self.__init_container()
        self.preprocess_code(code_path)
        self.container.start()
        copy_to_container(self.container, code_path, self.code_file_path)
        return super().before_test_execute(code_path, *args, **kwargs)

    def after_execute(self, *args, **kwargs):
        self.container.stop()
        self.container.wait()
        self.container.remove()

    def get_run_file_content(self, test_input, time_limit, *args, **kwargs):
        return f'''import subprocess, threading

class Command(object):
    def __init__(self):
        self.process = None
    def run(self, timeout):
        def target():
            self.process = subprocess.Popen(
                    {self.get_run_command_params()},
                    shell=False,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
        
            stdout = self.process.communicate(input="""{test_input}""".encode())[0]
            try:
                stdout = stdout.decode()
            except:
                pass
            
            if self.process.returncode:
                exception_message = stdout.strip() if stdout else "Unknown error"
                raise RuntimeError(exception_message)
            print(stdout.strip())

        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            self.process.terminate()
            thread.join()
            raise RuntimeError("{self.TIME_LIMIT_ERROR_MESSAGE}")
Command().run({time_limit/1000})
'''

    def prepare_run_file(self, test_input, *args, **kwargs):
        content = self.get_run_file_content(test_input, *args, **kwargs)
        file_path = self.temp_io_service.get_temp_file()

        with open(file_path, 'w') as file:
            file.write(content)
        copy_to_container(self.container, file_path, self.run_file_path)

    def execute_test(self, code_path, test_input, time_limit, memory_limit):
        try:
            self.prepare_run_file(test_input, memory_limit=memory_limit, time_limit=time_limit)
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
        except Exception as err:
            print(err)
            return None

    def build_test_result(self, execution_result, expected_output, test_id):
        actual_output = execution_result.output.decode().strip() \
            if execution_result \
            else 'No output'

        if not execution_result:
            return SubmissionTestResult(
                expected_output=expected_output,
                actual_output=actual_output,
                task_test_id=test_id,
                test_result_type_id=SubmissionTestResultType.execution_error().id,
            )

        (test_result_type, actual_output) = self.__resolve_test_result_type(execution_result, expected_output, actual_output)

        return SubmissionTestResult(
            expected_output=expected_output,
            actual_output=actual_output,
            task_test_id=test_id,
            test_result_type_id=test_result_type.id,
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

    def __init_container(self):
        self.client = docker.from_env()
        self.container = self.client.containers.create(
            image=self.image_name,
            command=f'sh -c "tail -f /dev/null"',
        )

    def __resolve_test_result_type(self, execution_result, expected_output, actual_output):
        is_runtime_error = execution_result.exit_code != 0
        is_correct_answer = actual_output == expected_output

        if is_runtime_error:
            if self.TIME_LIMIT_ERROR_MESSAGE in actual_output:
                return (SubmissionTestResultType.time_limit_error(), '')
            else:
                return (SubmissionTestResultType.execution_error(), actual_output)
        elif is_correct_answer:
            return (SubmissionTestResultType.correct_answer(), actual_output)
        else:
            return (SubmissionTestResultType.wrong_answer(), actual_output)
