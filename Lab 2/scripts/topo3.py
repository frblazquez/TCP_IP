#!/usr/bin/python
""" This example shows how to create a Mininet object and add nodes to
it manually.  """

"Importing Libraries"
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info

"Function definition:  This is called from the main function"
def firstNetwork():

	"Create an empty network and add nodes to it."
	net = Mininet()

	info( '*** Adding controller\n' ) 
	net.addController( 'c0' )

	info( '*** Adding hosts \n' )

	h1 = net.addHost( 'h1') 
	h2 = net.addHost( 'h2')
	h3 = net.addHost( 'h3') 
	h4 = net.addHost( 'h4')



	info( '*** Adding router \n' )
	r1 = net.addHost( 'r1' ) 
	r2 = net.addHost( 'r2' )
	r3 = net.addHost( 'r3')

	info( '*** Creating links\n' ) 
	net.addLink( r1, h1, intfName1='r1-eth0',intfName2='h1-eth0')
	net.addLink( r1, h2, intfName1='r1-eth1',intfName2='h2-eth0')
	net.addLink( r1, r2, intfName1='r1-eth2' ,intfName2='r2-eth1')
	net.addLink( r1, r3, intfName1='r1-eth3',intfName2='r3-eth2')
	net.addLink( r2, h3, intfName1='r2-eth0',intfName2='h3-eth0')
	net.addLink( r2, r3, intfName1='r2-eth2',intfName2='r3-eth1' )
	net.addLink( r3, h4, intfName1='r3-eth0',intfName2='h4-eth0' )



	info( '*** Starting network\n') 
	net.start()
	"This is used to run commands on the hosts"

	info( '*** Configuring hosts\n' )
	h1.cmd('ip -4 addr flush dev h1-eth0')
	h1.cmd('ip addr add 10.0.1.2/24 dev h1-eth0')
	h1.cmd('ip route add default via 10.0.1.1')
    #ipv6 
	h1.cmd('ip -6 addr add 2020::1:2/112 dev h1-eth0')
	h1.cmd('ip -6 route add default via 2020::1:1')
    
    
	h2.cmd('ip -4 addr flush dev h2-eth0')
	h2.cmd('ip addr add 10.0.2.2/24 dev h2-eth0')
	h2.cmd('ip route add default via 10.5.0.100')
    #ipv6
	h2.cmd('ip -6 addr add 2020::2:2/112 dev h2-eth0')
	h2.cmd('ip -6 route add default via 2020::10:2')
    
    
	h3.cmd('ip -4 addr flush dev h3-eth0')
	h3.cmd('ip addr add 10.0.3.2/24 dev h3-eth0')
	h3.cmd('ip route add default via 10.0.3.1')
    #ipv6
	h3.cmd('ip -6 addr add 2020::3:2/112 dev h3-eth0')
	h3.cmd('ip -6 route add default via 2020::3:1')
    
    
	h4.cmd('ip -4 addr flush dev h4-eth0')
	h4.cmd('ip addr add 10.0.4.2/24 dev h4-eth0')
	h4.cmd('ip route add default via 10.0.4.1')
    #ipv6
	h4.cmd('ip -6 addr add 2020::4:2/112 dev h4-eth0')
	h4.cmd('ip -6 route add default via 2020::4:1')

	info( '*** Configuring routers\n' )
	r1.cmd('ip -4 addr flush dev r1-eth0')
	r1.cmd('ip -4 addr flush dev r1-eth1')
	r1.cmd('ip -4 addr flush dev r1-eth2')
	r1.cmd('ip -4 addr flush dev r1-eth3')
	r1.cmd('ip addr add 10.0.1.1/24 dev r1-eth0')
	r1.cmd('ip addr add 10.0.2.1/24 dev r1-eth1')
	r1.cmd('ip addr add 10.0.5.1/24 dev r1-eth2')
	r1.cmd('ip addr add 10.0.7.1/24 dev r1-eth3')
    #ipv6
	r1.cmd('ip -6 addr add 2020::1:1/112 dev r1-eth0')
	r1.cmd('ip -6 addr add 2020::2:1/112 dev r1-eth1')
	r1.cmd('ip -6 addr add 2020::5:1/112 dev r1-eth2')
	r1.cmd('ip -6 addr add 2020::7:1/112 dev r1-eth3')

	r2.cmd('ip -4 addr flush dev r2-eth0')
	r2.cmd('ip -4 addr flush dev r2-eth1')
	r2.cmd('ip -4 addr flush dev r2-eth2')
	r2.cmd('ip addr add 10.0.3.1/24 dev r2-eth0')
	r2.cmd('ip addr add 10.0.5.2/24 dev r2-eth1')
	r2.cmd('ip addr add 10.0.6.1/24 dev r2-eth2')
    #ipv6
	r2.cmd('ip -6 addr add 2020::3:1/112 dev r2-eth0')
	r2.cmd('ip -6 addr add 2020::5:2/112 dev r2-eth1')
	r2.cmd('ip -6 addr add 2020::6:1/112 dev r2-eth2')

	r3.cmd('ip -4 addr flush dev r3-eth0')
	r3.cmd('ip -4 addr flush dev r3-eth1')
	r3.cmd('ip -4 addr flush dev r3-eth2')
	r3.cmd('ip addr add 10.0.4.1/24 dev r3-eth0')
	r3.cmd('ip addr add 10.0.6.2/24 dev r3-eth1')
	r3.cmd('ip addr add 10.0.7.2/24 dev r3-eth2')
    #ipv6
	r3.cmd('ip -6 addr add 2020::4:1/112 dev r3-eth0')
	r3.cmd('ip -6 addr add 2020::6:2/112 dev r3-eth1')
	r3.cmd('ip -6 addr add 2020::7:2/112 dev r3-eth2')


	r2.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
	r3.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
    #ipv6
	r2.cmd('echo 1 > /proc/sys/net/ipv6/conf/all/forwarding')
	r3.cmd('echo 1 > /proc/sys/net/ipv6/conf/all/forwarding')

    
	r1.cmd('ip route add 10.0.3.0/24 via 10.0.5.2')
	r1.cmd('ip route add 10.0.4.0/24 via 10.0.7.2')
	r1.cmd('ip route add 10.0.6.0/24 via 10.0.7.2')
    
    
	r3.cmd('ip route add 10.0.1.0/24 via 10.0.7.1')
	r3.cmd('ip route add 10.0.2.0/24 via 10.0.7.1')
	r3.cmd('ip route add 10.0.3.0/24 via 10.0.6.1')
	r3.cmd('ip route add 10.0.5.0/24 via 10.0.7.1')
    
    
    #ipv6 route
	r1.cmd('ip -6 route add 2020::3:0/112 via 2020::5:2')
	r1.cmd('ip -6 route add 2020::4:0/112 via 2020::7:2')
	r1.cmd('ip -6 route add 2020::6:0/112 via 2020::7:2')
    

	r3.cmd('ip -6 route add 2020::1:0/112 via 2020::7:1')
	r3.cmd('ip -6 route add 2020::2:0/112 via 2020::7:1')
	r3.cmd('ip -6 route add 2020::3:0/112 via 2020::6:1')
	r3.cmd('ip -6 route add 2020::5:0/112 via 2020::7:1')


	info( '*** Starting xterm on hosts\n' )
	h1.cmd('xterm -xrm \'XTerm.vt100.allowTitleOps: false\' -T h1 &') 
	h2.cmd('xterm -xrm \'XTerm.vt100.allowTitleOps: false\' -T h2 &')
	h3.cmd('xterm -xrm \'XTerm.vt100.allowTitleOps: false\' -T h3 &')
	h4.cmd('xterm -xrm \'XTerm.vt100.allowTitleOps: false\' -T h4 &')
	r1.cmd('xterm -xrm \'XTerm.vt100.allowTitleOps: false\' -T r1 &')
	r2.cmd('xterm -xrm \'XTerm.vt100.allowTitleOps: false\' -T r2 &')
	r3.cmd('xterm -xrm \'XTerm.vt100.allowTitleOps: false\' -T r3 &')
	

	info( '*** Running the command line interface\n' ) 
	CLI( net )

	info( '*** Closing the terminals on the hosts\n' ) 
	h1.cmd("killall xterm")
	h2.cmd("killall xterm")
	h3.cmd("killall xterm")
	h4.cmd("killall xterm")
	r1.cmd("killall xterm")
	r2.cmd("killall xterm")
	r3.cmd("killall xterm")

	info( '*** Stopping network' )
	net.stop()

"main Function: This is called when the Python file is run" 
if __name__ == '__main__':
	setLogLevel( 'info' )
	firstNetwork()