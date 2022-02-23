from subprocess import Popen, PIPE
from random import random, seed
from tqdm import tqdm
from pprint import pprint
import json
import time

SMALL_TEST_COUNT = 0
MEDIUM_TEST_COUNT = 0
LARGE_TEST_COUNT = 3
SEED = 1234
TEST_FILE = 'timeout.json'

seed(SEED)

class Timer():
    # context manager to capture stdout
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.t0 = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print(f'{self.name}: {time.time() - self.t0:.2f}')

def generate_random_input(multiplier=1, max_instances=20, max_pages=100, max_cache=10):
    '''returns a string that is valid input'''
    instances = int(random() * (max_instances)) + 1
    test = f'{instances}'

    for _ in range(instances):
        cache_size = int(random() * (max_cache * multiplier)) + 2
        page_count = int(random() * (max_pages * multiplier)) + 1

        test += f'\n{cache_size}'
        test += f'\n{page_count}'

        test += f'\n{" ".join(str(int(random() * (multiplier * page_count)) + 1) for _ in range(page_count))}'

    return test + '\n'

def generate_fixed_input(multiplier=1, instances=20, pages=100, cache=10):
    '''returns a string that is valid input'''
    test = f'{instances}'

    for _ in range(instances):
        test += f'\n{cache}'
        test += f'\n{pages}'

        test += f'\n{" ".join(str(int(random() * (multiplier * pages)) + 1) for _ in range(pages))}'

    return test + '\n'

def shell(cmd, stdin=None):
    out, err = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE).communicate(input=stdin.encode())
    return out.decode('utf8'), err.decode('utf8')

get_python_1 = lambda testCase: shell('python3 cache.py', stdin=testCase)
get_python_2 = lambda testCase: shell('python3 cache4.py', stdin=testCase)
get_cpp = lambda testCase: shell('./Cache', stdin=testCase)

tests = dict()

# manual tests
tests['given-test-0'] = {'input':"3\n2\n7\n1 2 3 2 3 1 2\n4\n12\n12 3 33 14 12 20 12 3 14 33 12 20\n3\n15\n1 2 3 4 5 1 2 3 4 5 1 2 3 4 5\n", 'output':"4\n6\n9\n"}
tests['given-test-1'] = {'input':"3\n2\n7\n1 2 3 2 3 1 2\n4\n12\n12 3 33 14 12 20 12 3 14 33 12 20\n3\n20\n1 2 3 4 5 1 2 3 4 5 1 2 3 4 5 1 2 3 4 5\n", 'output':"4\n6\n12\n"}

tests['edge-test-0'] = {'input':"1\n1\n1\n1\n", 'output':"1\n"}
tests['edge-test-1'] = {'input':f"1\n1\n100\n{' '.join('0' for _ in range(100))}\n", 'output':"1\n"}
tests['edge-test-2'] = {'input':f"1\n1\n200\n{' '.join('0 1' for _ in range(100))}\n", 'output':"200\n"}

if TEST_FILE == 'timeout.json':
    tests = dict()
    for i, (instances, pages, cache) in enumerate([(1, 1000000, 1000), (10, 100000, 1000), (100, 10000, 1000), (1000, 1000, 1000)]):
        test = generate_fixed_input(instances=instances, pages=pages, cache=cache)
        print(len(test), f'{instances=} {pages=} {cache=}')
        with Timer('p1'):
            python1, p_err1 = get_python_1(test)
        with Timer('p2'):
            python2, p_err2 = get_python_2(test)
        with Timer('cpp'):
            # cpp, c_err1 = get_cpp(test)
            cpp, c_err1 = python1, python2
        # print(python1)
        if python1 != python2 != cpp or len(python1) < 1:
            print('error', python1 == python2)
            exit()
            print(f'Python1\n{python1}')
            print()
            print(f'Python1 error\n{p_err1}')
            print()
            print(f'Python2\n{python2}')
            print()
            print(f'Python2 error\n{p_err2}')
            print()
            print(f'C++\n{cpp}')
            print()
            print(f'C++ error\n{c_err1}')
            print()
            print(f'Input\n{test}')
            exit()
        tests[f'timeout-test-{i}'] = {'input':test, 'output':python1}
        with open(TEST_FILE, 'w+') as f:
            json.dump(tests, f, indent=4)
    exit()

# random tests

for i in tqdm(range(SMALL_TEST_COUNT)):
    test = generate_random_input(max_instances=3, max_pages=20, max_cache=4)
    python1, p_err1 = get_python_1(test)
    python2, p_err2 = get_python_2(test)
    cpp, c_err1 = get_cpp(test)
    # print(python1)
    if python1 != python2 != cpp or len(python1) < 1:
        print(f'Python1\n{python1}')
        print()
        print(f'Python1 error\n{p_err1}')
        print()
        print(f'Python2\n{python2}')
        print()
        print(f'Python2 error\n{p_err2}')
        print()
        print(f'C++\n{cpp}')
        print()
        print(f'C++ error\n{c_err1}')
        print()
        print(f'Input\n{test}')
        exit()
    tests[f'small-test-{i}'] = {'input':test, 'output':python1}

for i in tqdm(range(MEDIUM_TEST_COUNT)):
    test = generate_random_input()
    python1, p_err1 = get_python_1(test)
    python2, p_err2 = get_python_2(test)
    cpp, c_err1 = get_cpp(test)
    if python1 != python2 != cpp or len(python1) < 1:
        print(f'Python1\n{python1}')
        print()
        print(f'Python1 error\n{p_err1}')
        print()
        print(f'Python2\n{python2}')
        print()
        print(f'Python2 error\n{p_err2}')
        print()
        print(f'C++\n{cpp}')
        print()
        print(f'C++ error\n{c_err1}')
        print()
        print(f'Input\n{test}')
        exit()
    tests[f'medium-test-{i}'] = {'input':test, 'output':python1}

for i in tqdm(range(LARGE_TEST_COUNT)):
    test = generate_random_input(max_instances=100, max_pages=2000, max_cache=100)
    # print(test)
    python1, p_err1 = get_python_1(test)
    python2, p_err2 = get_python_2(test)
    cpp, c_err1 = get_cpp(test)
    if python1 != python2 != cpp or len(python1) < 1:
        print(f'Python1\n{python1}')
        print()
        print(f'Python1 error\n{p_err1}')
        print()
        print(f'Python2\n{python2}')
        print()
        print(f'Python2 error\n{p_err2}')
        print()
        print(f'C++\n{cpp}')
        print()
        print(f'C++ error\n{c_err1}')
        print()
        print(f'Input\n{test}')
        exit()
    tests[f'large-test-{i}'] = {'input':test, 'output':python1}

# pprint(tests)
with open(TEST_FILE, 'w+') as f:
    json.dump(tests, f, indent=4)
