import os
import tarfile
from io import BytesIO

import docker

from judge.submissions_queue.code_executors.base_executor import BaseExecutor


class DockerExecutor(BaseExecutor):
    def __init__(self):
        self.client = docker.APIClient()
        self.container = None

    def copy_to(self, src, dst):
        os.chdir(os.path.dirname(src))
        srcname = os.path.basename(src)
        tar = tarfile.open(src + '.tar', mode='w')
        try:
            tar.add(srcname)
        finally:
            tar.close()

        data = open(src + '.tar', 'rb').read()
        self.client.put_archive(self.container, os.path.dirname(dst), data)

    def apply_template(self, code_path):
        with open(code_path, 'r') as code_file:
            code = code_file.read()
        with open(code_path, 'w') as template_file:
            template_file.write(f'''
fd = open('/tmp/test.txt')
sys.stdin = fd
{code}
''')
        return code_path

    def before_execute(self, code_path, *args, **kwargs):
        self.container = self.client.create_container(
            'python',
            stdin_open=True,
            command='sh -c "tail -f /dev/null"',
            name='docker_judge',
        )
        self.client.start(self.container)
        code_path = self.apply_template(code_path)
        self.copy_to(code_path, '/tmp')
        return super().before_test_execute(code_path, *args, **kwargs)

    def after_execute(self, *args, **kwargs):
        self.client.stop(self.container)
        self.client.wait(self.container)
        self.client.remove_container(self.container)

    def prepare_test_input(self, test_input):
        pass

    def get_contents(self, file_path):
        raw_stream, status = self.client.get_archive(self.container, file_path)
        tar_archive = BytesIO(b"".join((i for i in raw_stream)))
        t = tarfile.open(mode='r:', fileobj=tar_archive)
        return t.extractfile(os.path.basename(file_path)).read().decode('utf-8')

    def execute_test(self, code_path, test_input):
        cmd = 'python /tmp/sample_task.py'

        instance = self.client.exec_create(self.container, cmd)
        exec_id = instance['Id']
        self.prepare_test_input(test_input)
        result = self.client.exec_start(exec_id, stream=True)

        print('----------------------------')
        print(result)
        for x in result:
            print(x)

    def build_test_result(self, execution_result, expected_output):
        pass
