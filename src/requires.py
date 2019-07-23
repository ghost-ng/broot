import os
import sys
from pip._internal import main as pipmain
sys.path.append(os.path.join(os.getcwd(), "..", "misc"))
import colors

def install(package):
    try:
        pipmain(['install', package])
        color.PrintColor("SUCCESS", "Installed Successfully")
    except Exception as e:
        colors.PrintColor("FAIL", "Unable to install")
        print(e)
        input()