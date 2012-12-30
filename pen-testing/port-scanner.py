#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import optparse
import socket


def connection_scan(target_host, target_port):
    """Try and open a connection with a host and port"""
    try:    
        connection = socket.socket()
        connection.connect((target_host, target_port))
        connection.send('Violent Python\r\n')
        results = connection.recv(100)
        print '[+] %d/tcp open' % target_port
        print '[+] %s' % results
        connection.close()
    except Exception, e:
        print e

def port_scan(target_host, target_ports):
    try:
        target_ip = socket.gethostbyname(target_host)
    except:
        print "[-] Cannot resolve '%s': Unknown host" % target_host
        return

    try:
        target_name = socket.gethostbyaddr(target_ip)
        print '\n[+] Scan Results for: ' + target_name[0]
    except:
        print '\n[+] Scan Results for: ' + target_ip
    socket.setdefaulttimeout(1)
    for target_port in target_ports:
        print 'Scanning port ' + target_port
        connection_scan(target_host, int(target_port))
    

if __name__ == '__main__':
    """
    Example usage on localhost (to fire up a server on port 80:  python -m SimpleHTTPServer 80):
        python port-scanner.py -H 127.0.0.1 -p 21,22,80
    """
    parser = optparse.OptionParser('usage %prog –H'+\
        '<target host> -p <target port>')
    parser.add_option('-H', dest='target_host', type='string', \
        help='specify target host')
    parser.add_option('-p', dest='target_ports', type='string', \
        help='specify target ports comma separated')
    options, args = parser.parse_args()
    target_host = options.target_host
    target_ports = options.target_ports.strip().split(',')

    if (target_host == None) | (target_ports == None):
        print parser.usage
        exit(0)
    
    port_scan(target_host, target_ports)