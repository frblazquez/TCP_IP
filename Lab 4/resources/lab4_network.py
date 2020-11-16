#!/usr/bin/python
""" Lab 4 Topology """

"Importing Libraries"
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.term import cleanUpScreens, makeTerms
from mininet.node import Controller, OVSSwitch
from mininet.util import irange

import os

"Function definition:  This is called from the main function"
def Lab4_Network():
    os.system('mn -c')
    os.system('rm /home/lca2/Desktop/lab4/run/*')
    os.system('rm /home/lca2/Desktop/lab4/logs/*')

    "Create an empty network and add nodes to it."
    net = Mininet()
    
    info( '*** Adding controller\n' )
    net.addController( 'c0' )
 
    info( '*** Adding routers \n' )
    r1 = net.addHost( 'r1', ip='10.10.11.1/24' )
    r2 = net.addHost( 'r2', ip='10.10.12.2/24' )
    r3 = net.addHost( 'r3', ip='10.10.23.3/24' )
    r4 = net.addHost( 'r4', ip='10.10.14.4/24' )
    r5 = net.addHost( 'r5', ip='10.10.25.5/24' )
    routers=[r1,r2,r3,r4,r5]
    
    info( '*** Adding switches \n' )
    
    switches=[]
    for n in irange(1,8):
        switch = net.addSwitch('SW%s' % n)
        switch.cmd('ovs-vsctl set bridge SW%s protocols=OpenFlow13' % n)
        switches.append(switch)

    info( '*** Adding hosts \n' )
    
    h1 = net.addHost( 'h1', ip='10.10.11.10/24')
    h2 = net.addHost( 'h2', ip='10.10.35.20/24')
    h3 = net.addHost( 'h3', ip='10.10.35.30/24')
    hosts=[]
    for n in irange(4,8):
        host = net.addHost( 'h%s' % (n) , ip='10.10.24.%s0/24' % n)
        net.addLink( switches[7], host, intfName2='h%s-eth1' % n)
        hosts.append(host)

    info( '*** Creating links\n' )

    net.addLink( switches[0], h1, intfName2='h1-eth1'  )
    net.addLink( switches[0], r1, intfName2='r1-eth3'  )
    
    net.addLink( switches[1], r1, intfName2='r1-eth1'  )
    net.addLink( switches[1], r2, intfName2='r2-eth1'  )
        
    net.addLink( switches[2], r2, intfName2='r2-eth2'  )
    net.addLink( switches[2], r3, intfName2='r3-eth1'  )
        
    net.addLink( switches[3], r1, intfName2='r1-eth2'  )
    net.addLink( switches[3], r4, intfName2='r4-eth1'  )
        
    net.addLink( switches[4], r2, intfName2='r2-eth3'  )
    net.addLink( switches[4], r5, intfName2='r5-eth1'  )
        
    net.addLink( switches[5], r4, intfName2='r4-eth2'  )
    net.addLink( switches[5], r5, intfName2='r5-eth3'  )
        
    net.addLink( switches[6], r3, intfName2='r3-eth2'  )
    net.addLink( switches[6], r5, intfName2='r5-eth2'  )
    net.addLink( switches[6], h2, intfName2='h2-eth1'  )
    net.addLink( switches[6], h3, intfName2='h3-eth1'  )

    net.addLink( switches[7], r2, intfName2='r2-eth4'  )

    


    info( '*** Starting network\n')
    net.start()
    "This is used to run commands on the hosts and starting xterm on hosts"

    info( '*** Configuring hosts\n' )
    h1.cmd('ip route add default via 10.10.11.1')
    h1.cmd('ip -6 addr add 2001:1:0:11::10/64 dev h1-eth1')
    h1.cmd('ip -6 route add default via 2001:1:0:11::1')
    h1.cmd('xterm -xrm \'XTerm.vt100.allowTitleOps: false\' -T h1 &')

    h2.cmd('ip route add default via 10.10.35.5')
    h2.cmd('ip -6 addr add 2001:1:0:35::20/64 dev h2-eth1')
    h2.cmd('ip -6 route add default via 2001:1:0:35::5')
    h2.cmd('xterm -xrm \'XTerm.vt100.allowTitleOps: false\' -T h2 &')
    
    h3.cmd('ip route add default via 10.10.35.3')
    h3.cmd('ip -6 addr add 2001:1:0:35::30/64 dev h3-eth1')
    h3.cmd('ip -6 route add default via 2001:1:0:35::3')
    h3.cmd('xterm -xrm \'XTerm.vt100.allowTitleOps: false\' -T h3 &')

    index=3
    for host in hosts:
        index+=1
        host.cmd('ip route add default via 10.10.24.2')
        host.cmd('ip -6 addr add 2001:1:0:24::%s0/64 dev h%s-eth1' % (index, index))
        host.cmd('ip -6 route add default via 2001:1:0:24::2')
        host.cmd('xterm -xrm \'XTerm.vt100.allowTitleOps: false\' -T h%s &' % index)


    index=0
    for router in routers:
        index+=1
        router.cmd('xterm -xrm \'XTerm.vt100.allowTitleOps: false\' -T r%s &' % index)
        router.cmd('sysctl -w net.ipv4.conf.all.rp_filter=0')

    r1.cmd('sysctl -w net.ipv4.conf.r1-eth1.rp_filter=0')
    r1.cmd('sysctl -w net.ipv4.conf.r1-eth2.rp_filter=0')
    r1.cmd('sysctl -w net.ipv4.conf.r1-eth3.rp_filter=0')

    r2.cmd('ip addr add 10.10.24.2/24 dev r2-eth4')
    r2.cmd('sysctl -w net.ipv4.conf.r2-eth1.rp_filter=0')
    r2.cmd('sysctl -w net.ipv4.conf.r2-eth2.rp_filter=0')
    r2.cmd('sysctl -w net.ipv4.conf.r2-eth3.rp_filter=0')
    r2.cmd('sysctl -w net.ipv4.conf.r2-eth4.rp_filter=0')

    r3.cmd('sysctl -w net.ipv4.conf.r3-eth1.rp_filter=0')
    r3.cmd('sysctl -w net.ipv4.conf.r3-eth2.rp_filter=0')

    r4.cmd('sysctl -w net.ipv4.conf.r4-eth1.rp_filter=0')
    r4.cmd('sysctl -w net.ipv4.conf.r4-eth2.rp_filter=0')

    r5.cmd('sysctl -w net.ipv4.conf.r5-eth1.rp_filter=0')
    r5.cmd('sysctl -w net.ipv4.conf.r5-eth2.rp_filter=0')
    r5.cmd('sysctl -w net.ipv4.conf.r5-eth3.rp_filter=0')



    os.system("chown lca2 /home/lca2/Desktop/lab4/logs/*")
    info( '*** Running the command line interface\n' )
    CLI( net )
    
    info( '*** Closing the terminals on the hosts\n' )
    h1.cmd("killall xterm")
    h2.cmd("killall xterm")
    h3.cmd("killall xterm")

    for host in hosts:
        host.cmd("killall xterm")

    for router in routers:
        router.cmd("killall xterm")


    info( '*** Stopping network' )
    net.stop()

"main Function: This is called when the Python file is run"
if __name__ == '__main__':
    setLogLevel( 'info' )
    Lab4_Network()
