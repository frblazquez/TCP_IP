#!/usr/bin/python

"""
This script creates the network environment for Lab5:
- Starts all routers, switches and hosts
- You need to choose either Topo1 or Topo2
- XTerm window launched for all devices.
"""
# Needed to check for display status 
import inspect
import os

# Needed to patch Mininet's isShellBuiltin module
import sys

# Run commands when you exit the python script
import atexit

# patch isShellBuiltin (suggested by MiniNExT's authors)
import mininet.util

sys.modules['mininet.util'] = mininet.util

# Loads the default controller for the switches

from mininet.node import Controller

# Needed to set logging level and show useful information during script execution.
from mininet.log import setLogLevel, info

# To launch xterm for each node
from mininet.term import cleanUpScreens, makeTerms # for supporting copy/paste 

# Provides the mininet> prompt
from mininet.cli import CLI

# Primary constructor for the virtual environment.
from mininet.net import Mininet

# We import the TC-enabled link
from mininet.link import Intf, TCIntf, TCLink


# Variable initialization
net = None
hosts = None


def run():
    " Creates the virtual environment, by starting the network and configuring debug information "
    info('** Creating an instance of Lab5 network topology\n')
    global net
    global hosts
    # We specify the OVSSwitch for better IPv6 performance
    # We use mininext constructor with the instance of the network, the default controller and the customized openvswitch
    net = Mininet(intf=TCIntf)
   
    
    info('\n** Adding Controller\n')
    net.addController( 'c0' )
    
    info('\n** Adding Hosts\n')
    h1 = net.addHost('h1', ip='10.0.0.1/24', hostname='h1',  privateLogDir=True, privateRunDir=True, inMountNamespace=True, inPIDNamespace=True, inUTSNamespace=True)
    h2 = net.addHost('h2', ip='10.0.0.2/24', hostname='h2',  privateLogDir=True, privateRunDir=True, inMountNamespace=True, inPIDNamespace=True, inUTSNamespace=True)
    h3 = net.addHost('h3', ip='10.0.3.3/24', hostname='h3',  privateLogDir=True, privateRunDir=True, inMountNamespace=True, inPIDNamespace=True, inUTSNamespace=True)
    h4 = net.addHost('h4', ip='10.0.2.4/24', hostname='h4',  privateLogDir=True, privateRunDir=True, inMountNamespace=True, inPIDNamespace=True, inUTSNamespace=True)
    r1 = net.addHost('r1', hostname='r1',  privateLogDir=True, privateRunDir=True, inMountNamespace=True, inPIDNamespace=True, inUTSNamespace=True)
    r2 = net.addHost('r2', hostname='r2',  privateLogDir=True, privateRunDir=True, inMountNamespace=True, inPIDNamespace=True, inUTSNamespace=True)
    
    info('\n** Adding Switches\n')
    # Adding switches to the network
    sw1 = net.addSwitch('sw1')
    #sw2 = net.addSwitch('sw2')
    #sw3 = net.addSwitch('sw3')
    
    info('\n** Creating Links \n')
    link_h1sw1 = net.addLink( h1, sw1)
    link_h2sw1 = net.addLink( h2, sw1)
    link_r2h4 = net.addLink( r2, h4, intfName1='r2-eth2')
    link_r2h3 = net.addLink( r2, h3, intfName1='r2-eth1')
    link_r1sw1= net.addLink( r1, sw1, intfName1='r1-eth0')
    link_r1r2 = net.addLink( r1, r2, intfName1='r1-eth1',intfName2='r2-eth0')
    # link_r2sw2 = net.addLink( r2, sw2, intfName1='r2-eth0')
    #link_r2sw3 = net.addLink( r2, sw3, intfName1='r2-eth1')

    
    info('\n** Modifying Link Parameters \n')
    """
        Default parameters for links:
        bw = None,
 		delay = None,
 		jitter = None,
 		loss = None,
 		disable_gro = True,
 		speedup = 0,
 		use_hfsc = False,
 		use_tbf = False,
 		latency_ms = None,
 		enable_ecn = False,
 		enable_red = False,
 		max_queue_size = None 
    """
    link_h1sw1.intf1.config( bw=1, enable_ecn=True,enable_red=True)
    link_h2sw1.intf1.config( bw=10, enable_ecn=True, enable_red=True)
    link_r1r2.intf1.config( bw=1.5, enable_ecn=True, enable_red=True)
    link_r2h4.intf1.config( bw=10, enable_ecn=True, enable_red=True)
    link_r2h3.intf1.config( bw=0.5, enable_ecn=True, enable_red=True)

    net.start()
    r1.cmd('ip addr add 10.0.0.10/24 dev r1-eth0')
    r1.cmd('ip addr add 10.0.1.10/24 dev r1-eth1')
    r2.cmd('ip addr add 10.0.2.20/24 dev r2-eth2')
    r1.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
    r2.cmd('ip addr add 10.0.3.20/24 dev r2-eth1')
    r2.cmd('ip addr add 10.0.1.20/24 dev r2-eth0')
    r2.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')


    h1.cmd('ip route add default via 10.0.0.10')
    h2.cmd('ip route add default via 10.0.0.10')
    h3.cmd('ip route add default via 10.0.3.20')
    h4.cmd('ip route add default via 10.0.2.20')
    r2.cmd('route add -net 10.0.0.0/24 gw 10.0.1.10')
    r1.cmd('route add -net 10.0.3.0/24 gw 10.0.1.20')
    r1.cmd('route add -net 10.0.2.0/24 gw 10.0.1.20')

    info('** Executing custom commands\n')
    output = net.nameToNode.keys
    # Space to add any customize command before prompting command line
    # You can add any extra logic to it
	#
	#
	#
    info( '*** Configuring hosts\n' )
   
    #r1.cmd('tc qdisc del dev r1-eth1 root')
    #r1.cmd('tc qdisc add dev r1-eth1 root handle 1: cbq avpkt 1000 bandwith 60mbit')
    #r1.cmd('tc class add dev r1-eth1 parent 1: class 1:1 cbq rate 100mbit allot 1500 prio 5 bounded isolated')
    #r1.cmd('tc filter add dev r1-eth1 protocol ip parent 1: prio 16 u32 match ip src 0/0 flowid 1:1')


    
    
	#Enable Xterm window for every host
    info('** Enabling xterm for hosts only\n')
    # We check if the display is available
    hosts = [ h1, h2, h3, h4, r1, r2]
    if 'DISPLAY' not in os.environ:
        error( "Error starting terms: Cannot connect to display\n" )
        return
    # Remove previous (and possible non-used) socat X11 tunnels
    cleanUpScreens()
    # Mininet's function to create Xterms in hosts
    makeTerms( hosts, 'host' )

	# Enable the mininet> prompt 
    info('** Running CLI\n')
    CLI(net)
    h1.cmd("killall xterm")
    h2.cmd("killall xterm")
    h3.cmd("killall xterm")
    h4.cmd("killall xterm")
    r1.cmd("killall xterm")
    r2.cmd("killall xterm")    #r2.cmd("killall xterm")
    # This command stops the simulation
    net.stop()
    cleanUpScreens()


if __name__ == '__main__':
    # Set the log level on terminal
    setLogLevel('info')
    
    # Execute the script
    run()
