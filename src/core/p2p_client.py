# External
from random import randint
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

# Internal
import json

broadcast_type = {
    'BLOCK': 'BLOCK',
    'TX': 'TX',
    'NODE': 'NODE'
}

# Algorithm:
# 1. node connects to pool server
# 2. node broadcasts txs and blocks to other nodes
# 3. node receives broadcasted txs and blocks


class P2PClient (DatagramProtocol):
    def __init__(self, host, port) -> None:
        self.id = host, port
        self.address = None
        self.msg_started = False
        self.nodes = []
        self.server = '127.0.0.1', 9999

        def a(msg):
            print('Received block:', msg)

        def b(msg):
            print('Received tx:', msg)

        self.receive_blocks = a
        self.receive_txs = b
        print('Working on id:', self.id)


    def startProtocol(self):
        self.transport.write('ready'.encode('utf-8'), self.server)

    def stopProtocol(self):
        pass
        # self.transport.write('stop'.encode('utf-8'), self.server)

    def datagramReceived(self, datagram: bytes, addr):
        datagram = datagram.decode('utf-8')
        msg = json.loads(datagram)
        self.__receive(msg['type'], msg['data'])
        

    def __receive(self, type, msg):
        if type == broadcast_type['BLOCK']:
            self.receive_blocks(msg)
        elif type == broadcast_type['TX']:
            self.receive_txs(msg)
        elif type == broadcast_type['NODE']:
            self.receive_nodes(msg)
        else:
            print('Error at __receive. Invalid broadcast message type.')

    def receive_nodes(self, nodes):
        print('Received nodes:', nodes)
        self.nodes = nodes
        if not self.msg_started:
            self.msg_started = True
            reactor.callInThread(self.send_message)

    def __broadcast(self, type, data):
        # prepare data
        print('sending',type,data)

        msg = json.dumps({ 'type': type, 'data': data })
        for node in self.nodes:
            self.transport.write(msg.encode('utf-8'), tuple(node))

    # This function should broadcast blocks to other nodes
    def broadcast_blocks(self, blocks):
        self.__broadcast(broadcast_type['BLOCK'], blocks)

    # This function should broadcast txs to other nodes
    def broadcast_txs(self, txs):
        self.__broadcast(broadcast_type['TX'], txs)

    def send_message(self):
        while True:
            type, msg = input('Type: '), input('Data:')
            if type == 'BLOCK':
                self.broadcast_blocks(msg)
            elif type == 'TX':
                self.broadcast_txs(msg)
            else:
                break

if __name__ == '__main__':
    port = randint(1023, 4999)
    cl = P2PClient('127.0.0.1', port)
    reactor.listenUDP(port, cl)
    reactor.callInThread(reactor.run)

    print('GOT here')
    cl.broadcast_blocks('auto')