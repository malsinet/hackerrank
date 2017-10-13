import os
from timeit import default_timer as timer
from math import ceil

def merge(d1, d2):
    ''' Merge two dictionaries. '''
    merged = {}
    merged.update(d1)
    merged.update(d2)
    return merged

def filenames(prefix, folder):
    return [{prefix: os.path.join(folder, file)} 
        for file in os.listdir(folder) 
            if file.startswith(prefix)]

def elapsed_str(end, start):
    return str(int(round((end-start)*1000)))+" msec"

class TestCase:
    def __init__(self, folder):
        self.folder = folder

    def list(self):
        inputs  = filenames("input", self.folder)
        outputs = filenames("output", self.folder)
        return [merge(i,o) for i,o in list(zip(inputs, outputs))]

    def run(self, testcase, fn):
        with open(testcase["input"]) as inf, open(testcase["output"]) as outf:
            input_text = inf.read()
            start = timer()
            result = " ".join(str(x) for x in fn(input_text.split("\n")))
            end = timer()
            expected_text = outf.read()
            return {
                "success": (result == expected_text),
                "runtime": elapsed_str(end, start),
                "result": result,
                "expected": expected_text
            }

    def suite(self, testcases, fn):
        return [self.fields(self.run(test, fn)) for test in testcases]

    def results(self, tests):
        titles = [["Test case", "Success", "Runtime"]]
        results = [["#%s" % i, t["success"], t["runtime"]] for i, t in enumerate(tests)]
        return titles + results

    def fields(self, item):
        return {
            "success": item["success"],
            "runtime": item["runtime"]
        }
