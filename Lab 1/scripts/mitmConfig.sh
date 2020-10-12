#!/usr/bin/bash

# Reverse path filtering disable !!  (https://www.slashroot.in/linux-kernel-rpfilter-settings-reverse-path-filtering)
PC4 echo 0 > /proc/sys/net/ipv4/conf/all/rp_filter 
PC4 echo 0 > /proc/sys/net/ipv4/conf/PC4-eth0/rp_filter
PC4 echo 0 > /proc/sys/net/ipv4/conf/PC4-eth1/rp_filter
PC4 echo 0 > /proc/sys/net/ipv4/conf/PC4-eth2/rp_filter

# IPv4 and IPv6 forwarding enable
PC4 echo 1 > /proc/sys/net/ipv4/ip_forward
PC4 echo 1 > /proc/sys/net/ipv6/conf/all/forwarding

# Make sure network interfaces are up
PC1 ip link set PC1-eth0 up
PC2 ip link set PC2-eth0 up
PC3 ip link set PC3-eth0 up
PC4 ip link set PC4-eth0 up
PC4 ip link set PC4-eth1 up
PC4 ip link set PC4-eth2 up

# IP address removements (replace with assigned IP addresses)
# PCX ip addr del <IPv4 addr> dev PCX-ethY
# PCX ip -6 addr del <IPv6 addr> dev PCX-ethY
#
#PC1 ip addr del 10.0.0.1/8 dev PC1-eth0
#PC1 ip -6 addr del fe80::ac35:95ff:fefd:19f0/64 dev PC1-eth0
#PC2 ip addr del 10.0.0.2/8 dev PC2-eth0
#PC2 ip -6 addr del fe80::ac35:95ff:fefd:19f0/64 dev PC2-eth0
#PC3 ip addr del 10.0.0.3/8 dev PC3-eth0
#PC3 ip -6 addr del fe80::ac35:95ff:fefd:19f0/64 dev PC3-eth0
#PC4 ip addr del 10.0.0.4/8 dev PC4-eth0
#PC4 ip -6 addr del fe80::ac35:95ff:fefd:19f0/64 dev PC4-eth0
#PC4 ip addr del 10.0.0.5/8 dev PC4-eth1
#PC4 ip -6 addr del fe80::ac35:95ff:fefd:19f0/64 dev PC4-eth1
#PC1 ip addr del 10.0.0.6/8 dev PC4-eth2
#PC1 ip -6 addr del fe80::ac35:95ff:fefd:19f0/64 dev PC4-eth2
#
# PCX ip addr flush dev <device>
PC1 ip addr flush dev PC1-eth0
PC2 ip addr flush dev PC2-eth0
PC3 ip addr flush dev PC3-eth0
PC4 ip addr flush dev PC4-eth0
PC4 ip addr flush dev PC4-eth1
PC4 ip addr flush dev PC4-eth2

# IP address assignements
PC1 ip addr add 10.10.10.1/24 dev PC1-eth0
PC1 ip -6 addr add fd24:ec43:12ca:c001:10::1/80 dev PC1-eth0
PC2 ip addr add 10.10.20.1/24 dev PC2-eth0
PC2 ip -6 addr add fd24:ec43:12ca:c001:20::1/80 dev PC2-eth0
PC3 ip addr add 10.10.30.1/24 dev PC3-eth0
PC3 ip -6 addr add fd24:ec43:12ca:c001:30::1/80 dev PC3-eth0
PC4 ip addr add 10.10.10.4/24 dev PC4-eth0
PC4 ip -6 addr add fd24:ec43:12ca:c001:10::4/80 dev PC4-eth0
PC4 ip addr add 10.10.20.4/24 dev PC4-eth1
PC4 ip -6 addr add fd24:ec43:12ca:c001:20::4/80 dev PC4-eth1
PC4 ip addr add 10.10.30.4/24 dev PC4-eth2
PC4 ip -6 addr add fd24:ec43:12ca:c001:30::4/80 dev PC4-eth2

# IP default route configuration
PC1 ip route add default via 10.10.10.4 dev PC1-eth0
PC1 ip -6 route add default via fd24:ec43:12ca:c001:10::4 dev PC1-eth0
PC2 ip route add default via 10.10.20.4 dev PC2-eth0
PC2 ip -6 route add default via fd24:ec43:12ca:c001:20::4 dev PC2-eth0
PC3 ip route add default via 10.10.30.4 dev PC3-eth0
PC3 ip -6 route add default via fd24:ec43:12ca:c001:30::4 dev PC3-eth0

# Conectivity testing (IPv4)
PC1 ping -c 1 PC4
PC1 ping -c 1 PC2
PC1 ping -c 1 PC3
PC2 ping -c 1 PC4
PC2 ping -c 1 PC1
PC2 ping -c 1 PC3
PC3 ping -c 1 PC4
PC3 ping -c 1 PC1
PC3 ping -c 1 PC2
PC4 ping -c 1 PC1
PC4 ping -c 1 PC2
PC4 ping -c 1 PC3

# Conectivity testing (IPv6)
PC1 ping6 -c 1 fd24:ec43:12ca:c001:10::4
PC1 ping6 -c 1 fd24:ec43:12ca:c001:20::4
PC1 ping6 -c 1 fd24:ec43:12ca:c001:30::4
PC1 ping6 -c 1 fd24:ec43:12ca:c001:10::1
PC1 ping6 -c 1 fd24:ec43:12ca:c001:20::1
PC1 ping6 -c 1 fd24:ec43:12ca:c001:30::1

PC2 ping6 -c 1 fd24:ec43:12ca:c001:10::4
PC2 ping6 -c 1 fd24:ec43:12ca:c001:20::4
PC2 ping6 -c 1 fd24:ec43:12ca:c001:30::4
PC2 ping6 -c 1 fd24:ec43:12ca:c001:10::1
PC2 ping6 -c 1 fd24:ec43:12ca:c001:20::1
PC2 ping6 -c 1 fd24:ec43:12ca:c001:30::1

PC3 ping6 -c 1 fd24:ec43:12ca:c001:10::4
PC3 ping6 -c 1 fd24:ec43:12ca:c001:20::4
PC3 ping6 -c 1 fd24:ec43:12ca:c001:30::4
PC3 ping6 -c 1 fd24:ec43:12ca:c001:10::1
PC3 ping6 -c 1 fd24:ec43:12ca:c001:20::1
PC3 ping6 -c 1 fd24:ec43:12ca:c001:30::1

PC4 ping6 -c 1 fd24:ec43:12ca:c001:10::4
PC4 ping6 -c 1 fd24:ec43:12ca:c001:20::4
PC4 ping6 -c 1 fd24:ec43:12ca:c001:30::4
PC4 ping6 -c 1 fd24:ec43:12ca:c001:10::1
PC4 ping6 -c 1 fd24:ec43:12ca:c001:20::1
PC4 ping6 -c 1 fd24:ec43:12ca:c001:30::1

