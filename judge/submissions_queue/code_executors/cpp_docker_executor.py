from judge.submissions_queue.code_executors.base.docker_executor import DockerExecutor


class CppDockerExecutor(DockerExecutor):
    code_file_path = f'/tmp/code_file.cpp'
    image_name = 'gcc'
    executable_file_path = f'/tmp/executable'

    def get_compile_command(self):
        return f'g++ {self.code_file_path} -o {self.executable_file_path}'

    def get_run_command(self, test_input):
        # return f'{self.executable_file_path} < <(echo "{test_input}")'
        return f'''{self.executable_file_path} <<EOF
{test_input}
EOF'''
        # return f'cat {self.test_file_path} | {self.executable_file_path}'
        # return f'{self.executable_file_path} < {self.test_file_path} > /tmp/output'
