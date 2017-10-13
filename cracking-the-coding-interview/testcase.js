var fs = require('fs');
var path = require('path');

var tc = {
    list: function(folder){
        var files = fs.readdirSync(folder);
        var inputs = files.filter(filename => filename.startsWith("input"));
        var outputs = files.filter(filename => filename.startsWith("output"));
        var testcases = inputs.map(function (item, i) { 
            return {
                input: path.join(folder, item), 
                output: path.join(folder, outputs[i])
            } 
        });
        return testcases;
    },
    run: function(testcase, runFn){
        var input = fs.readFileSync(testcase.input, "utf8");
        var begin = Date.now();
        var result = runFn(input.split("\n"));
        var end = Date.now();
        var expected = fs.readFileSync(testcase.output, "utf8");
        return {
             success: (expected === result),
             runtime: (end-begin) + " msec",
              result: result,
            expected: expected
        }
    },
    suite: function(testcases, fn){
        var that = this;
        return testcases.map(
            function(testcase, i) {
                var tc = that.run(testcase, fn);
                return {
                    testcase: "#" + i,
                     success: tc.success,
                     runtime: tc.runtime
                };
            });
    },
    results: function(tests){
        var titles = ["Test case", "Success", "Runtime"];
        var results = tests.map(
            function(test){
                return [test.testcase, test.success, test.runtime]
            }
        );
        results.unshift(titles);
        return results;
    }
}

module.exports = tc
