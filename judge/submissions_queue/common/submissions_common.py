from os.path import join

import yaml


def read_yaml(file_path):
    with open(file_path) as stream:
        return yaml.safe_load(stream)


def read_file(file_path):
    with open(file_path) as stream:
        return stream.read()


def get_tests(task_path):
    config_path = join(task_path, "task.yml")
    config = read_yaml(config_path)
    return [
        {
            'in': read_file(join(task_path, test['in'])),
            'out': read_file(join(task_path, test['out']))
        }
        for test in config['tests']
    ]
