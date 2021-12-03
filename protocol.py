import radio

class RadioProtocol:
    def __init__(self, address, shiftPattern):
        self.addr = address
        self.shiftPattern = shiftPattern
        return None

    # Sends a packet following a specific format
    def sendPacket(self, message, addrDest):
        if len(message)<251:
            radio.send_bytes("" + str(self.addr) + "|" + str(len(message)) + "|" + str(addrDest) + "|" + self.encrypt(message))

    # Receives a packet, checks if has the number of values it should, and if it does returns the message (according the addrDest matches the address of the device receiving the message)
    def receivePacket(self, packet):
        if packet is None:
            return 0
        else:
            tabRes = packet.format(1).split("|")
            if len(tabRes) != 4 :
                return -1
            data = dict()
            data['addrInc'] = tabRes[0]
            data['lenMess'] = tabRes[1]
            data['addrDest'] = tabRes[2]
            if self.addr == int(data['addrDest']):
                data['message'] = self.decrypt(tabRes[3])
                return data['message']
            return -1

    def encrypt(self, msg):
        res = ""
        for i in range(len(msg)):
            res += chr(ord(msg[i])+self.shiftPattern)
        return res

    def decrypt(self, msg):
        res = ""
        for i in range(len(msg)):
            res += chr(ord(msg[i])-self.shiftPattern)
        return res