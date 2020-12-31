import uuid

from judge.submissions_queue.code_executors.base.docker_executor import DockerExecutor


class PythonDockerExecutor(DockerExecutor):
    code_file_path = f'/tmp/code_file-{uuid.uuid4()}.py'
    image_name = 'python:slim'

    def apply_template(self, code):
        return f'''import sys
fd = open('{self.test_file_path}')
sys.stdin = fd
{code}'''

    def build_command(self):
        return f'python {self.code_file_path}'
