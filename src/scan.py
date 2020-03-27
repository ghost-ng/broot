#ADAPTED AND TAKEN FROM: https://pastebin.com/YCR3vp9B
import sys, os
import requires
from printlib import *
import var

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
try:
    import socks    #HERE
except ModuleNotFoundError:
    print_warn("Unable to find 'socks', install?")   #HERE
    ans = input("[Y/N] ")
    if ans.lower() == "y":
        requires.install('socks')   #HERE
        from scapy.all import *
    else:
        print_fail("'scapy' is a dependency!")   #HERE
        input()

SYNACK = 0x12 # Set flag values for later reference
RSTACK = 0x14

def send_syn_probe(port, target): # Function to scan a given port
    verbose = var.global_vars['verbose']['Value']
    attempt = "Target:{}:{}".format(target, port)
    try:
        srcport = RandShort() # Generate Port Number
        conf.verb = 0 # Hide output
        if verbose:
            print_info("Sending SYN Probe --> {}".format(attempt))
        SYNACKpkt = sr1(IP(dst = target)/TCP(sport = srcport, dport = port, flags = "S"), timeout=3) # Send SYN and recieve RST-ACK or SYN-ACK
        try:
            pktflags = SYNACKpkt.getlayer(TCP).flags # Extract flags of recived packet
        except:
            pktflags = None
        if pktflags == SYNACK: # Cross reference Flags
            if verbose:
                print_info("Received SYN-ACK, target service appears up")
            return True # If open, return true
        else:
            print_warn("It's too quiet, target service appears down ({})".format(target))
            return False # If closed, return false

    except KeyboardInterrupt: # In case the user needs to quit
            RSTpkt = IP(dst = target)/TCP(sport = srcport, dport = port, flags = "R") # Built RST packet
            send(RSTpkt) # Send RST packet to whatever port is currently being scanned
            print_info("Detected CTRL-C...")
            return

def send_tcp_probe(target_port, target_host):
    verbose = var.global_vars['verbose']['Value']
    attempt = "Target:{}:{}".format(target_host, target_port)
    
    if var.global_vars['proxy-probe']['Value'] is not None:
        proxy = var.parse_proxy_settings("probe")
        proxy_proto = {
            "http": socks.HTTP,
            "socks4": socks.SOCKS4,
            "socks5": socks.SOCKS5
        }
    
        proxy_host = proxy['host']
        proxy_port = proxy['port']
        proxy_type = proxy_proto[proxy['protocol']]
        s = socks.socksocket()
        s.set_proxy(proxy_type, proxy_host, int(proxy_port))
    else:
        s = socket.socket()
   
    s.settimeout(3)
    
    try:
        if verbose:
            print_info("Sending TCP Probe --> {}".format(attempt))
        addr = (target_host,target_port)
        s.connect(addr)
        s.close()
        return True
    except:
        return False
    