import uuid

from judge.submissions.code_executors.base.docker_executor import DockerExecutor


class PythonDockerExecutor(DockerExecutor):
    code_file_path = f'/tmp/code_file-{uuid.uuid4()}.py'
    image_name = 'iskralumbeva/judge-python'

    def get_compile_command(self, *args, **kwargs):
        return None

    def get_run_command_params(self):
        return f'["python", "{self.code_file_path}"]'
