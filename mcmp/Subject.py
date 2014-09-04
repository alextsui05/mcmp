import os
import random

class Subject:
    def __init__(self, name):
        self.name = name
        self.state = PipelineState()

class PipelineState:
    def __init__(self):
        self.has_metric = False
        self.has_initial_map = False
        self.has_final_map = False

def LoadSubjects(path, protocol=None, target=None):
    path = os.path.expanduser(path)
    names = os.listdir(path)
    res = map(lambda x : Subject(x), names)
    random_numbers = random.sample(range(len(res)), len(res))
    for i in range(len(res)):
        res[i].random = random_numbers[i]
    if protocol is not None:
        for i in range(len(res)):
            metric_filename = os.path.join(
                path, res[i].name, 'protocols', protocol, 'metric.u'
            )
            res[i].state.has_metric = os.path.exists(metric_filename)
    if target is not None:
         for i in range(len(res)):
            initial_map_name = os.path.join(
                path, target,
                'protocols', protocol,
                'maps', res[i].name,
                'initial.map'
            )
            res[i].state.has_initial_map = os.path.exists(initial_map_name)
            final_map_name = os.path.join(
                path, target,
                'protocols', protocol,
                'maps', res[i].name,
                'initial.map'
            )
            res[i].state.has_final_map = os.path.exists(final_map_name)
    return res
