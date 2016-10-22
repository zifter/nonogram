import os
import sys

def abs_path(rel):
    return os.path.realpath(os.path.join(os.path.dirname(__file__), rel))


scripts_folder = abs_path('./../../src/')
if scripts_folder not in sys.path:
    sys.path.append(scripts_folder)

tests_folder = abs_path('./../../tests/')
if tests_folder not in sys.path:
    sys.path.append(tests_folder)
