import radio

class RadioProtocol:
    def __init__(self, address):
        self.addr = address
        return None

    def calculateChecksum(self, message):
        nleft = len(message)
        sum = 0
        pos = 0
        while nleft > 1:
            sum = ord(message[pos]) * 256 + (ord(message[pos + 1]) + sum)
            pos = pos + 2
            nleft = nleft - 2
        if nleft == 1:
            sum = sum + ord(message[pos]) * 256

        sum = (sum >> 16) + (sum & 0xFFFF)
        sum += (sum >> 16)
        sum = (~sum & 0xFFFF)

        return sum
    
    def sendPacket(self, message, addrDest):
        if len(message)<251:
            radio.send_bytes("" + str(self.addr) + "|" + str(len(message)) + "|" + str(addrDest) + "|" + message + "|" + str(self.calculateChecksum(message)))

    def receivePacket(self, packet):
        if packet is None:
            return 0
        else:
            tabRes = packet.format(1).split("|")
            stuff = dict()
            stuff['addrInc'] = tabRes[0]
            stuff['lenMess'] = tabRes[1]
            stuff['addrDest'] = tabRes[2]
            stuff['message'] = tabRes[3]
            stuff['receivedCheckSum'] = tabRes[4]
            if self.verifyCheckSum(stuff['receivedCheckSum'], self.calculateChecksum(stuff['message'])):
                if self.addr == int(stuff['addrDest']):
                    return stuff['message']
            return -1
    
    def verifyCheckSum(self, checkSum, receivedCheckSum):
        if int(checkSum) == receivedCheckSum:
            return True
        else:
            return False

