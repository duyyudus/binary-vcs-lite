# Development Guide

Before doing implementation, please look at `docs/design.png` carefully.

All attributes, properties ( public attributes ) methods signature must be implemented exactly as designed.

Public method parameters must be type-checked explicitly using `common.util.check_type()`

For business logic, please try to do the same as in design first. If there is a design fault, just feel free to contact me to discuss.

About testing, testcase may be not good enough, just make sure you understand the logic first, then discuss with me before modifying the test.

All tests must pass on both Python 2 and 3.

Finally, to run the test properly, your Python environment must have following packages

* pathlib2 ( for Python2 )
* pathlib ( for Python3 )
* ruamel.yaml
* tree_util_lite
