import re
from argparse import ArgumentParser

import zmq

import morse
import pi

default_port = "5556"
default_ip = "127.0.0.1"


def ip_checker(ip_address):
    pattern = re.compile(
        "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.)"
        "{3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    )
    if pattern.match(ip_address):
        return True
    return False


def domain_checker(domain):
    pattern = re.compile(
        "^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$"
        )
    if pattern.match(domain):
        return True
    return False


def parse_address(address_, port_):
    try:
        address_ = address_.replace('tcp://', '')
        if domain_checker(address_) or ip_checker(address_):
            server_url_ = 'tcp://{}'.format(address_)
        else:
            server_url_ = 'tcp://{}'.format(default_ip)
    except AttributeError:
        server_url_ = 'tcp://{}'.format(default_ip)
    try:
        server_port = int(port_)
    except (ValueError, TypeError):
        server_port = default_port
    server_url_ = '{}:{}'.format(server_url_, server_port)
    return server_url_


parser = ArgumentParser(
    description='Gets strings trough zmq, '
                'translates it to morse code '
                'and sends impulses trough GPIO',
)
parser.add_argument('address', nargs='?')
parser.add_argument('port', nargs='?')
args = parser.parse_args()
address = args.address
port = args.port
server_url = parse_address(address, port)

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, 'Morse')
socket.connect(server_url)
while True:
    payload = socket.recv()
    topic, message = payload.split()
    print(morse.encode(message))
    pi.send_morse_to_pi(morse.encode(message))
