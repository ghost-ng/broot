#ADAPTED AND TAKEN FROM: https://pastebin.com/YCR3vp9B
import sys, os
import requires
sys.path.append(os.path.join(os.getcwd(), "..", "misc"))
from printlib import *

try:
    from scapy.all import *    #HERE
except ModuleNotFoundError:
    print_warn("Unable to find 'scapy', install?")   #HERE
    ans = input("[Y/N] ")
    if ans.lower() == "y":
        requires.install('scapy')   #HERE
        from scapy.all import *
    else:
        print_fail("'scapy' is a dependency!")   #HERE
        input()

SYNACK = 0x12 # Set flag values for later reference
RSTACK = 0x14

def scan_port(port, target): # Function to scan a given port
        try:
                srcport = RandShort() # Generate Port Number
                conf.verb = 0 # Hide output
                SYNACKpkt = sr1(IP(dst = target)/TCP(sport = srcport, dport = port, flags = "S"), timeout=3) # Send SYN and recieve RST-ACK or SYN-ACK
                try:
                    pktflags = SYNACKpkt.getlayer(TCP).flags # Extract flags of recived packet
                except:
                    pktflags = None
                if pktflags == SYNACK: # Cross reference Flags
                        return True # If open, return true
                else:
                        return False # If closed, return false
                RSTpkt = IP(dst = target)/TCP(sport = srcport, dport = port, flags = "R") # Construct RST packet
                send(RSTpkt) # Send RST packet

        except KeyboardInterrupt: # In case the user needs to quit
                RSTpkt = IP(dst = target)/TCP(sport = srcport, dport = port, flags = "R") # Built RST packet
                send(RSTpkt) # Send RST packet to whatever port is currently being scanned
                print_info("Detected CTRL-C...")
                sys.exit(1)