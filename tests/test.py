import os
import unittest
import importlib
loader = unittest.TestLoader()
runner = unittest.runner.TextTestRunner()
suite = unittest.TestSuite() 
for fn in os.listdir():
    if fn[-3::] == ".py" and fn != "test.py":
        suite.addTests(
                loader.loadTestsFromModule(
                    importlib.import_module(fn[:-3])
                    )
                )
runner.run(suite)
