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

def MapsDir(base, source, target, protocol):
    return os.path.join(base, source, 'protocols', protocol, 'maps', target)

def StatsDir(base, source, target, protocol):
    return MapsDir(base, source, target, protocol) + os.sep + 'stats'

def ReadFloatFromFile(filename):
    fp = open(filename, 'r')
    val = float(fp.readline().strip())
    fp.close()
    return val

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
            initial_map_name = MapsDir(path, target, res[i].name, protocol) +\
                os.sep + 'initial.map'
            res[i].state.has_initial_map = os.path.exists(initial_map_name)
            final_map_name = MapsDir(path, target, res[i].name, protocol) +\
                os.sep + 'final.map'
            res[i].state.has_final_map = os.path.exists(final_map_name)

            harmonic_energy_name =\
                StatsDir(path, target, res[i].name, protocol) + os.sep + 'final.energy'
            res[i].state.harmonic_energy = '-1'
            if os.path.exists(harmonic_energy_name):
                res[i].state.harmonic_energy = ReadFloatFromFile(harmonic_energy_name)
            
            elastic_energy_name =\
                StatsDir(path, target, res[i].name, protocol) + os.sep + 'elastic_energy'\
                    + os.sep + 'total_energy.txt'
            res[i].state.elastic_energy = '-1'
            if os.path.exists(elastic_energy_name):
                res[i].state.elastic_energy = ReadFloatFromFile(elastic_energy_name)

    return res
