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
    h1 = net.addHost('h1', ip='10.20.0.1/24', hostname='h1',  privateLogDir=True, privateRunDir=True, inMountNamespace=True, inPIDNamespace=True, inUTSNamespace=True)
    # Space to add any commands for configuring the IP addresses
    #
    #
    #
    #

    info('\n** Adding Switches\n')
    # Adding switches to the network
    sw1 = net.addSwitch('sw1')

    
    info('\n** Creating Links \n')
    link_h1sw1 = net.addLink( h1, sw1)
    link_h2sw1 = net.addLink( h2, sw1)
    link_r1sw1 = net.addLink( r1, sw1, intfName1='r1-eth0')
    link_h3r1 = net.addLink( r1, h3, intfName1='r1-eth1')

    
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
    link_h3r1.intf1.config( bw=10, enable_red=True ,  enable_ecn=True)

    
    net.start()
    info('** Executing custom commands\n')
    output = net.nameToNode.keys
    info( '*** Configuring hosts\n' )
    r1.cmd('ip addr add 10.20.0.10/24 dev r1-eth0')
    # Space to add commands for configuring routing tables and default gateways
    #
	#
	#
	#

	#Enable Xterm window for every host
    info('** Enabling xterm for hosts only\n')
    # We check if the display is available
    hosts = [ h1, h2, h3, r1 ]
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
    r1.cmd("killall xterm")
    h1.cmd("killall xterm")
    h2.cmd("killall xterm")
    h3.cmd("killall xterm")
    # This command stops the simulation
    net.stop()
    cleanUpScreens()




if __name__ == '__main__':
    # Set the log level on terminal
    setLogLevel('info')
    
    # Execute the script
    run()
