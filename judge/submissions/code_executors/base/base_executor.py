import tempfile
from abc import ABC, abstractmethod
from os.path import join, basename


class BaseExecutor(ABC):
    def before_execute(self, *args, **kwargs):
        pass

    def after_execute(self, *args, **kwargs):
        pass

    def before_test_execute(self, *args, **kwargs):
        pass

    def execute(self, code_path, tests, time_limit, memory_limit):
        fixed_code_path = self.prepare_code(code_path)
        self.before_execute(fixed_code_path, tests)

        test_results = []
        try:
            for test in tests:
                self.before_test_execute(fixed_code_path, test)
                execution_result = self.execute_test(fixed_code_path, test['in'], time_limit, memory_limit)
                test_results.append(self.build_test_result(execution_result, test['out'], test['id']))
        except:
            pass

        self.after_execute(fixed_code_path, tests)
        return test_results

    @abstractmethod
    def build_test_result(self, execution_result, expected_output, test_id):
        pass

    @abstractmethod
    def execute_test(self, code_path, input, time_limit, memory_limit):
        pass

    def apply_template(self, code):
        return code

    def prepare_code(self, code_path):
        with open(code_path, 'r') as code_file:
            contents = code_file.read()

        contents = self.apply_template(contents)
        fixed_code_path = join(
            tempfile.gettempdir(),
            f'{basename(code_path)}-fixed')
        with open(fixed_code_path, 'w') as fixed_code_file:
            fixed_code_file.write(contents)
        return fixed_code_path
