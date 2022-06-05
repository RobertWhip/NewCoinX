from random import randint
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import json
import copy

# Pool server
class P2PServer (DatagramProtocol):
    def __init__(self) -> None:
        self.nodes = set()

    def datagramReceived(self, datagram: bytes, addr):
        datagram = datagram.decode('utf-8')
        if datagram == 'ready':
            # Save client to memory
            self.nodes.add(addr)

            # Send already connected clients to client
            type = 'NODE'

            for node in self.nodes:
                nodes_copy = copy.deepcopy(self.nodes)
                nodes_copy = list(nodes_copy - set([ node ]))

                msg = json.dumps({ 'type': type, 'data': nodes_copy })

                self.transport.write(
                    msg.encode('utf-8'),
                    node
                )


if __name__ == '__main__':
    port = 9999
    reactor.listenUDP(port, P2PServer())
    reactor.run()