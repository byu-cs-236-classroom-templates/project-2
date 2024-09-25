# Project 2

This project uses the `lexer` function from Project 1. That function takes as input a Datalog program as a string, and it returns an iterator to a `Token`. Each token generated by the iterator is a syntactic element of the Datalog program input. Project 2 implements a parser that consumes the tokens from the iterator to accomplish two things:

  1. Determine if the input Datalog program is syntactically correct -- the sequence of tokens, e.g. syntactic elements of the input, represents a valid Datalog program.
  2. Build an instance of a `DatalogProgram` object from the observed sequence of tokens if that sequence is valid.

So the input to the `parser.parse` function is the token iterator from the `lexer` function on some input, and the output from the `parser.parse` function is an instance of the `DatalogProgram` class iff the input is syntactically correct; otherwise it raises an `UnexpectedTokenException`. The `parser.parse` function must implement a predictive top-down parsing algorithm that is recursive.

The predictive top-down parsing algorithm is derived from the Datalog grammar using _FIRST_ and _FOLLOW_ sets for each of the rules in the grammar. The mathematical definition of a grammar, grammar, rules, FIRST, FOLLOW, etc. are in the lecture notes on [learningsuite.byu.edu](https://learningsuite.byu.edu) in the _Content_ section. Creating a top-down predictive parsing algorithm from those things is also in the lecture notes content. Further, we provide an extensive Jupyter notebook that walks through implementing the `parse` function on a simple example.
**Before proceeding further, please review the Project 2 project description, lecture slides, and all of the associated Jupyter notebooks. You can thank us later for the suggestion.**

## Developer Setup

Be sure to read the [Copy Files](#Copy-Files) section.

As in Project 1, the first step is to clone the repository created by GitHub Classroom when the assignment was accepted in a sensible directory. In the vscode terminal, `git clone <URL>` where `<URL>` is the one from GitHub Classroom after accepting the assignment. Or open a new vscode window, select _Clone Git Repository_, and paste the link they get when they hover over the "<> Code ▼" and copy the url

There is no need to install any vscode extensions. These should all still be present and active from the previous project. You do need to create the virtual environment, install the package, and install pre-commit. For a reminder to how that is done, see on [learningsuite.byu.edu](https://learningsuite.byu.edu) _Content_ &rarr; _Projects_ &rarr; _Projects Cheat Sheet_

  * Create a virtual environment: **be sure to create it in the `project-2` folder.**
  * Install the package in edit mode: `pip install --editable ".[dev]"`
  * Install pre-commit: `pre-commit install`

The above should result in a `project2` executable that is run from the command line in an integrated terminal. As before, be sure the integrated terminal is in the virtual environment

## Files

  * `README.md`: overview and directions
  * `config_test.sh`: support for auto-grading -- **please do not edit**
  * `images`: folder for images referenced in `README.md`
  * `pyproject.toml`: package definition and project configuration -- **please do not edit**
  * `src`: folder for the package source files
  * `tests`: folder for the package test files

### Copy Files {#Copy-Files}

Copy the below files from your solution to Project 1 into the `src/project2/` folder:

  * `fsm.py`
  * `lexer.py`

The `token.py` file is unchanged here and should not be copied over. None of test files from Project 1 should be copied over either.

### Reminder

Please do not edit any of the following files or directories as they are related to _auto-grading_ and _pass-off_:

  * `config_test.sh`
  * `./tests/passoff_utils.py`
  * `./tests/test_passoff_80.py`
  * `./tests/test_passoff_100.py`
  * `./tests/resources/project2-passoff/*`

## Overview

The project is divided into the following modules each representing a key component:

  * `src/project2/datalogprogram.py`: defines the `Parameter`, `Predicate`, `Rule`, and `DatalogProgram` classes.
  * `src/project2/parser.py`: defines `UnexpectedTokenException`, `TokenStream`, and the `parse` function entry point used by `project2.py`.
  * `src/project2/project2.py`: defines the entry point for auto-grading and the command line entry point.

Each of the above files are specified with Python _docstrings_ and they also have examples defined with python _doctests_. A _docstring_ is a way to document Python code so that the command `help(project2.parser)` in the Python interpreter outputs information about the module with it's functions and classes. For functions, the docstrings give documentation when the mouse hovers over the function in vscode.

### datalogprogram.py

The `parser.parse` function needs to build, and return, an instance of a `DatalogProgram`. The program consists of `Predicates`. A predicate has an `name` and a list of `Parameter` objects. A `Parameter` is a `STRING` type or an `ID` type. Both types have a `value` attribute that is taken from the token when the `Parameter` is created, so it's either the value from the `ID` token or the value from the `STRING` token.

A `DatalogProgram` consists of `schemes`, `facts`, `rules`, and `queries`. The `schemes`, `facts`, and `queries` are of `List[Predicate]` type. The predicates in `schemes` can only have `ID` types for parameters. The predicates in `facts` can only have `STRING` types for parameters. The predicates `queries` can have `ID` or `STRING` parameter types.

A rule consists of a _head_ predicate with a list of predicates. The head predicate only has `ID` parameter types while the predicates in the list can have either `ID` or `STRING` in the parameters. These attributes are accessed directly as in `rule.head` and `rule.predicates` where `rule` is an instance of the `Rule` class.

The `Parameter` and `Predicate` classes both have an implemented the `__str__` function for pretty printing. The implementation `DatalogProgram.__str__` is **not given and must be implemented by you.** The are tests in `./tests/test_datalogprogram.py` to test the `DatalogProgram.__str__` function. The tests should pass when the function is implemented correctly.

### parser.py

The bulk of the coding for the project is in the `parser.py` module. See the project description, lecture notes, and Jupiter notebooks on [learningsuite.byu.edu](https://learningsuite.byu.edu) in the _Content_ section in both _Lectures_ and _Projects_.

Provided for your convenience is the `TokenStream` class that is able to  `match` and `advance` the token iterator from the lexer. It raises an `UnexpectedTokenException` when `TokenStream.match` fails. These are fully implemented and should be used by your parser.

### project2.py

The entry point for the auto-grader and the `project2` command. See the docstrings for details.

## Where to start

Here is the suggested order for Project 1:

1. Run the tests in `test_datalogprogram.py` -- any tests associated with `DatalogProgram.__str__` should fail
1. Implement the `DatalogProgram.__str__` function so that the tests pass -- what it should output is described in the project description on [learningsuite.byu.edu](https://learningsuite.byu.edu) in the _Content_ section.
1. Write the grammar for a Datalog program.
1. For each production in the Datalog program grammar:

    1. Write two tests for the production in `./tests/test_parser.py` -- a test for bad input that checks for the `UnexpectedTokenException` exception and a test that returns the result of the production on a correct parse.
    1. Run the new tests -- they should fail
    1. Implement the production from the grammar-- done when the new tests pass

1. Run the pass-off tests -- debug as needed

## Pass-off and Submission

The minimum standard for this project is **bucket 80**. That means that if all the tests pass in all buckets up to and including bucket 80, then the next project can be started safely.

The Project 2 submission follows that the other projects:

  * Commit your solution on the master branch
  * Push the commit to GitHub -- that should trigger the auto-grader
  * Goto [learningsuite.byu.edu](https://learningsuite.byu.edu) at _Assignments_ &rarr; _Projects_ &rarr; _Project 2_ to submit your GitHub ID and Project 2 URL for grading.
  * Goto the Project 2 URL, find the green checkmark or red x, and click it to confirm the auto-grader score matches the pass-off results from your system.

### Branches

Consider using a branch as you work on your submission so that you can `commit` your work from time to time. Once everything is working, and the auto-grader tests are passing, then you can `merge` your work into your master branch and push it to your GitHub repository. Ask your favorite search engine or generative AI for help learning how to use Git branches.
