import re
from os.path import dirname, basename

from judge.submissions.code_executors.base.docker_executor import DockerExecutor


class JavaDockerExecutor(DockerExecutor):
    image_name = 'iskralumbeva/judge-java'
    class_name_regex = 'public class (.*?){'
    class_name = None

    def get_compile_command(self):
        return f'javac {self.code_file_path}'

    def get_run_command_params(self):
        return f'["java", "-cp", "{dirname(self.executable_file_path)}", "{basename(self.executable_file_path)}"]'

    def preprocess_code(self, code_path):
        with open(code_path, 'r') as code_file:
            content = code_file.read()
        result = re.search(self.class_name_regex, content)
        self.class_name = result.groups(1)[0].strip()

    @property
    def code_file_path(self):
        return f'/tmp/{self.class_name}.java'

    @property
    def executable_file_path(self):
        return f'/tmp/{self.class_name}'




