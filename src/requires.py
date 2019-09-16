import os
import sys
from pip._internal import main as pipmain
sys.path.append(os.path.join(os.getcwd(), "..", "misc"))
from printlib import *

def install(package):
    try:
        pipmain(['install', package, '--user'])
        print_good("Installed Successfully")
    except Exception as e:
        print_fail("Unable to install")
        print(e)
        input()