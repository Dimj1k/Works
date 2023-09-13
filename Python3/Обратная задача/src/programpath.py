from pathlib import Path
from datetime import datetime


class ProgramPath:

    def __init__(self, program_path, num_dirs):
        self.main_dir = Path(program_path).parent / datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
        self.main_dir.mkdir(exist_ok=True)
        if type(num_dirs) is int:
            self.total_dirs = iter(range(1, num_dirs + 1))
            self.__begins = 1
        else:
            self.total_dirs = iter(range(num_dirs[0], num_dirs[1] + 1))
            self.__begins = num_dirs[0]

    def next_dir(self):
        i = next(self.total_dirs)
        if i != self.__begins:
            self.main_dir /= ".."
        self.main_dir /= f"{i}_эксперт"
        self.main_dir.mkdir(exist_ok=True)

    def __next__(self):
        return self.next_dir()
