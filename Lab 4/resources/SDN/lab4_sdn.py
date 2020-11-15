#!/usr/bin/python

"""
Script used for the SDN section of Lab4
"""
import time
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info
# We use the OVSSwitch
# We import RemoteController class to use the RYU controller
from mininet.node import OVSSwitch, RemoteController



net = None

def run():
    # Creating the network according to Fig. 2 of Lab4
    info( 'Creating the network' )
    net = Mininet( controller=RemoteController, switch=OVSSwitch) # Controller

    info( '*** Adding controller\n' )
    # Without any additional parameters, by default Mininet will look into 127.0.0.1:6633 for the controller
    # This is consistent with RYU controller's default settings
    c0 = RemoteController('c0')
    net.addController(c0)

    info( '*** Adding hosts, switches and host-switch links\n' )
    switches = []
    for h in range(5):
        n = h + 1
        # We assigned distinguishable dpid (datapath ID) to each switch for easy management  mac='%s0:%s1:1c:a2:1a:b4'
        switch = net.addSwitch('SW%s' % n, dpid='0%s0%s1ca21ab40%s0%s' % (n, n, n, n) )
        switches.append(switch)
        messg = 'Adding switch %s\n' % switches[h]
        info(messg)
        # We assigned distinguishable mac-addresses to each host
        host = net.addHost( 'h%s' % n, ip='10.10.%s.%s/16' % (n, n), mac='1c:a2:1a:b4:0%s:0%s' % (n, n) )
        messg = 'Adding host %s\n' % host.name
        info(messg)
        net.addLink(switch, host)

    info( '*** Creating Additional Links\n' )
    
    net.addLink( switches[0], switches[1])
    net.addLink( switches[0], switches[2])
    net.addLink( switches[1], switches[2])
    net.addLink( switches[1], switches[3])
    net.addLink( switches[2], switches[4])
    net.addLink( switches[3], switches[4])

    info( '*** Starting network\n')
    net.start()

    # for i, switch in enumerate(switches):
    #     switch.cmd("ovs-vsctl set Bridge SW%s protocols=OpenFlow13"%(i+1))

    info( '*** Running CLI\n' )
    CLI( net )
    
    info( '*** Stopping network' )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
