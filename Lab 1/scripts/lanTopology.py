#!/usr/bin/python

"""
This example shows how to create a Mininet object and add nodes to it manually.
"""
"Importing Libraries"
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info

"Function definition: This is called from the main function"
def firstNetwork():

    "Create an empty network and add nodes to it."
    net = Mininet()
    info( '*** Adding controller\n' )
    net.addController( 'c0' )

    info( '*** Adding hosts\n' )
    PC1 = net.addHost( 'PC1')
    
    info( '*** Adding switch\n' )
    s14 = net.addSwitch( 's14' )
    
    info( '*** Creating links\n' )
    net.addLink( PC1, s14 )
    
    info( '*** Starting network\n')
    net.start()

    "This is used to run commands on the hosts"

    info( '*** Starting terminals on hosts\n' )
    PC1.cmd('xterm -xrm "XTerm.vt100.allowTitleOps: false" -T PC1 &')
    PC2.cmd('xterm -xrm "XTerm.vt100.allowTitleOps: false" -T PC2 &')
    PC3.cmd('xterm -xrm "XTerm.vt100.allowTitleOps: false" -T PC3 &')
    PC4.cmd('xterm -xrm "XTerm.vt100.allowTitleOps: false" -T PC4 &')

    info( '*** Running the command line interface\n' )
    CLI( net )
	
    info( '*** Closing the terminals on the hosts\n' )
    PC1.cmd("killall xterm")
    PC2.cmd("killall xterm")
    PC3.cmd("killall xterm")
    PC4.cmd("killall xterm")
	
    info( '*** Stopping network' )
    net.stop()

"main Function: This is called when the Python file is run"
if __name__ == '__main__':
    setLogLevel( 'info' )
    firstNetwork()
