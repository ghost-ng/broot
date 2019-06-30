BLUE = '\033[94m'
GREY = '\033[90m'
GREEN = '\033[92m'
RED = '\033[31m'
YELLOW = '\033[93m'
FAIL = '\033[91m'
BOLD = '\033[1m'
BGRED = '\033[41m'
WHITE = '\033[37m'
UNDERLINE = '\033[4m'
RSTCOLORS = '\033[0m'


def PrintColor(status, msg):
    '''
    Prints out the message in a pre-formatted string of text
    Possible values for 'status': WARN,SUCCESS,FAIL,INFO
    '''
    if status == "WARN":
        text = YELLOW + "[!] " + msg + RSTCOLORS
    elif status == "SUCCESS":
        text = GREEN + "[+] " + msg + RSTCOLORS
    elif status == "INFO":
        text = WHITE + "[*] " + msg + RSTCOLORS
    elif status == "FAILED":
        text = RED + "[-] " + msg + RSTCOLORS
    elif status == "DEBUG":
        text = GREY + "[DEBUG] " + msg + RSTCOLORS
    else:
        text = "[*] " + msg + RSTCOLORS
    print(text)