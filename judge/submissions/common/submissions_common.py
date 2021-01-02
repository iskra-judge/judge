from os.path import join
from os import linesep

import yaml


def read_yaml(file_path):
    with open(file_path) as stream:
        return yaml.safe_load(stream)


def read_file(file_path):
    with open(file_path) as stream:
        return stream.read()


def fix_text(text):
    lines = text.split('\n')
    lines = [l.strip() for l in lines]
    result = '\n'.join(lines)
    return result


def get_tests(task_path):
    config_path = join(task_path, "task.yml")
    config = read_yaml(config_path)
    return [
        {
            'in': fix_text(read_file(join(task_path, test['in']))),
            'out': fix_text(read_file(join(task_path, test['out']))),
        }
        for test in config['tests']
    ]
