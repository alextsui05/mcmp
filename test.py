import sys
import os
import jinja2
import pickle
import random
import mcmp

def append_random(subjects):
    random_numbers = random.sample(range(len(subjects)), len(subjects))
    subs = map(lambda x : mcmp.Subject(x['name']), subjects)
    for i in range(len(subs)):
        subs[i].random = random_numbers[i]
    return subs

def loadData(filename):
    fp = open('subjects.pickle', 'r')
    subjects = pickle.load(fp)
    fp.close()
    return subjects

env = jinja2.Environment(loader=jinja2.PackageLoader('app', 'templates'))
template = env.get_template('base.html')
if len(sys.argv) > 3:
    subjects = mcmp.LoadSubjects(sys.argv[1], sys.argv[2], sys.argv[3])
elif len(sys.argv) > 2:
    subjects = mcmp.LoadSubjects(sys.argv[1], sys.argv[2])
elif len(sys.argv) > 1:
    subjects = mcmp.LoadSubjects(sys.argv[1])
else: 
    subjects = loadData('subjects.pickle')
    subjects = append_random(subjects)
templateVars = {
    'username' : 'atsui',
    'subjects' : subjects
}
print template.render(templateVars)
