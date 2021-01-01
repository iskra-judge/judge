from judge.submissions_queue.code_executors.base.docker_executor import DockerExecutor


class CppDockerExecutor(DockerExecutor):
    code_file_path = f'/tmp/code_file.cpp'
    image_name = 'gcc'
    executable_file_path = f'/tmp/executable'

    def get_compile_command(self):
        return f'g++ {self.code_file_path} -o {self.executable_file_path}'

    def get_run_command_params(self):
        return f'["{self.executable_file_path}"]'