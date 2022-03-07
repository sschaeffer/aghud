#!/usr/bin/env python3
from sys import path
path.append("/home/integ/Code/aghud")

from ag.common.aghudconfig import AGHUDConfig

import socket
import struct
from time import sleep
from pathlib import Path

class ServerQuery:
    id = 0
    retries = 0
    max_retries = 0
    timeout = 0.1
    _port = 0
    _host = "localhost"
    _connected = False
    _num_players = 0
    
    def __init__(self, **kargs):

        self.addr = (self._host, self._port)
        if 'max_retries' in kargs:
            self.max_retries = kargs['max_retries']
        if 'timeout' in kargs:
            self.timeout = kargs['timeout']

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(self.timeout)

    def initialize_connection(self, minecraftdir, servername):
        serverproperties_path=Path(f"{minecraftdir}/server/{servername}/server.properties")
        if serverproperties_path.is_file():
            with open(serverproperties_path) as f:
                line  = f.readline()
                while line and self._port == 0:
                    if line[0] != '#':
                        key, value = line.split('=')
                        if key == "query.port":
                            self._port = int(value)
                    line  = f.readline()
                if self._port != 0:
                    print(f"Port: {self._port}")
                    self.addr = (self._host, self._port)
                    self.handshake()
                    if self.is_connected():
                        self.basic_stats()
                    else:
                        self.clear_stats()

    def test_connection(self, minecraftdir, servername):
        if self.is_connected():
            self.handshake()
            if self.is_connected():
                self.basic_stats()
            else:
                self.clear_stats()
        else:
            self.initialize_connection(minecraftdir, servername)

    def is_connected(self):
        return self._connected

    def write_packet(self, type, payload):
        o = b'\xFE\xFD' + struct.pack('>B', type) + struct.pack('>l', self.id) + payload
        self.socket.sendto(o, self.addr)
    
    def read_packet(self):
        buff = self.socket.recvfrom(2048)[0]
        type = buff[0]
#        type = struct.unpack('>B', buff[0])[0]
        id   = struct.unpack('>l', buff[1:5])[0]
        return type, id, buff[5:]
    
    def handshake(self):

        self.id += 1
        self.retries=0
        self.write_packet(9, b'')
        try:
            type, id, buff = self.read_packet()
        except:
            self.retries += 1
            if self.retries >= self.max_retries:
                self._connected = False
                return 0 
            return self.handshake()
        
        self.retries = 0
        self.challenge = struct.pack('>l', int(buff[:-1]))
        self._connected = True

    def basic_stats(self):
        self.write_packet(0, self.challenge)
        try:
            type, id, buff = self.read_packet()
        except:
            self.handshake()
            return self.basic_stat()

        data = {}
        data['motd'], data['gametype'], data['map'], data['numplayers'], data['maxplayers'], buff = buff.split(b'\x00', 5)

        self._num_players = int(data['numplayers'].decode())
        print(f"Number Players: {self._num_players}")

    def clear_stats(self):
        self._num_players = 0

    def number_players(self):
        return(self._num_players)

#    def basic_stat(self):
#        self.write_packet(0, self.challenge)
#        try:
#            type, id, buff = self.read_packet()
#        except:
#            self.test_connection()
#            return self.basic_stat()
#        
#        data = {}
#        
#        #I don't seem to be receiving this field...
#        #data['ip'] = socket.inet_ntoa(buff[:4])[0]
#        #buff = buff[4:]
#        
#        #Grab the first 5 string fields
#        data['motd'], data['gametype'], data['map'], data['numplayers'], data['maxplayers'], buff = buff.split('\x00', 5)
#        
#        #Unpack a big-endian short for the port
#        data['hostport'] = struct.unpack('<h', buff[:2])[0]
#        
#        #Grab final string component: host name
#        data['hostname'] = buff[2:-1]
#        
#        #Encode integer fields
#        for k in ('numplayers', 'maxplayers'):
#            data[k] = int(data[k])
#
#        return data
#    
#    def full_stat(self):
#        #Pad request to 8 bytes
#        self.write_packet(0, self.challenge + '\x00\x00\x00\x00')
#        try:
#            type, id, buff = self.read_packet()
#        except:
#            self.test_connection()
#            return self.full_stat()    
#        
#        #Chop off useless stuff at beginning
#        buff = buff[11:]
#        
#        #Split around notch's silly token
#        items, players = buff.split('\x00\x00\x01player_\x00\x00')
#        
#        #Notch wrote "hostname" where he meant to write "motd"
#        items = 'motd' + items[8:] 
#        
#        #Encode (k1, v1, k2, v2 ..) into a dict
#        items = items.split('\x00')
#        data = dict(zip(items[::2], items[1::2])) 
#
#        #Remove final two null bytes
#        players = players[:-2]
#        
#        #Split player list
#        if players: data['players'] = players.split('\x00')
#        else:       data['players'] = []
#        
#        #Encode ints
#        for k in ('numplayers', 'maxplayers', 'hostport'):
#            data[k] = int(data[k])
#        
#        #Parse 'plugins'
#        s = data['plugins']
#        s = s.split(': ', 1)
#        data['server_mod'] = s[0]
#        if len(s) == 1:
#            data['plugins'] = []
#        elif len(s) == 2:
#            data['plugins'] = s[1].split('; ')
#
#        return data
#
#
# ----
# UNIT TESTING ROUTINES - REMOVE BEFORE DEPLOYING RELEASE
# ----
def main(aghudconfig):

    print()
    print("Server Query:    Unit Testing")

    server_query = ServerQuery()

    if not server_query.is_connected():
        server_query.test_connection(aghudconfig.minecraftdir(), aghudconfig.servername())
        print(f"Result: {server_query.is_connected()}")

#    while not server_query.is_connected():
#        server_query.test_connection(minecraftdir, worldname)
#        print(f"Result: {server_query.is_connected()}")


if __name__ == "__main__":
    aghudconfig = AGHUDConfig("/home/integ/Code/aghud/config.json")
    main(aghudconfig)