import subprocess, threading

def get_run_command_params():
    return f'["python", "{self.code_file_path}"]'

def get_test_input():
    pass

class Command(object):
    def __init__(self):
        self.process = None

    def run(self, timeout):
        def target():
            self.process = subprocess.Popen(
                get_run_command_params(),
                shell=False,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )

            stdout = self.process.communicate(input=get_test_input().encode())[0]
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
            raise RuntimeError("self.TIME_LIMIT_ERROR_MESSAGE")


Command().run(10000)
