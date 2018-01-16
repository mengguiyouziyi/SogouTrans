#!/bin/env python
import os
import re
import time
import redis
import json
import time
import sys
import argparse
import socket
import urllib
from urllib.request import urlopen
from lxml import etree

# set html header
head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"}


def test_interface():
    try:
        rslt = urlopen("http://members.3322.org/dyndns/getip")
        html = rslt.read()
        ret_ip = html.rstrip()
        print("return ip=%s" % (ret_ip))
    except Exception as FF:
        print >> sys.stderr, "Test interface error, exit ... \n"
        sys.exit(1)


# set interface
def set_interface(ip):
    true_socket = socket.socket

    def bind_socket(*arg1, **arg2):
        sock = true_socket(*arg1, **arg2)
        sock.bind((ip, 0))
        return sock

    socket.socket = bind_socket
    print("vitual ip: %s" % (ip))
    test_interface()


if __name__ == "__main__":
    # parse args
    set_interface(sys.argv[1])
