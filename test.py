import sys
import os
import shutil
import jinja2
import pickle
import random
import mcmp

def append_random(subjects):
    random_numbers = random.sample(range(len(subjects)), len(subjects))
    subjects = map(lambda x : mcmp.Subject(x['name']), subjects)
    for i in range(len(subjects)):
        subjects[i].random = random_numbers[i]
    return subjects

def loadData(filename):
    fp = open('subjects.pickle', 'r')
    subjects = pickle.load(fp)
    fp.close()
    return subjects

if __name__ == '__main__':
    # Setup the template
    env = jinja2.Environment(loader=jinja2.PackageLoader('app', 'templates'))
    template = env.get_template('base.html')
    protocol = 'miccai-op'
    target = '1-119_082399_L'
    if len(sys.argv) > 3:
        subjects = mcmp.LoadSubjects(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) > 2:
        subjects = mcmp.LoadSubjects(sys.argv[1], sys.argv[2], target)
    elif len(sys.argv) > 1:
        subjects = mcmp.LoadSubjects(sys.argv[1], protocol, target)
    else:
        subjects = loadData('subjects.pickle')
        subjects = append_random(subjects)
    templateVars = {
        'username' : 'atsui',
        'subjects' : subjects
    }
    content = template.render(templateVars)

    # Write the report to output/index.html
    if os.path.exists('output'):
        shutil.rmtree('output')
    os.mkdir('output')
    fp = open('output' + os.sep + 'index.html', 'w')
    fp.write(content)
    fp.close()

    # Copy the assets to output
    shutil.copytree('app' + os.sep + 'assets', 'output' + os.sep + 'assets')
