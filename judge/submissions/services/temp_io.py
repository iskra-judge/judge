import uuid
from os import mkdir
from os.path import join
from tempfile import gettempdir


class TempIoService:
    def __init__(self):
        self.root_dir = join(gettempdir(), "judge_strategies")
        self.__ensure_root_dir_exists()

    def get_temp_file(self):
        return join(self.root_dir, str(uuid.uuid4()))

    def __ensure_root_dir_exists(self):
        try:
            mkdir(self.root_dir)
        except FileExistsError:
            pass
