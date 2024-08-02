import json
import os
from utils import *


class Options:
    def __init__(self, file_name, default_options):
        self.file_name = file_name
        self.default_options = Utils.copy(default_options)
        self.options = default_options
        self._read_options()
        self.write_options()

    def _read_options(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as fr:
                self.options = json.loads(fr.read())

    def write_options(self):
        with open(self.file_name, 'w') as fw:
            fw.write(json.dumps(self.options))

    def get(self, path, default=None):
        return Utils.get(self.options, path, default=default)

    def set(self, path, value):
        Utils.set(self.options, path, value)
        self.write_options()