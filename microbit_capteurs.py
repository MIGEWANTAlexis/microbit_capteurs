from microbit import *
import radio
import protocol
from ssd1306 import initialize, clear_oled
from ssd1306_text import add_text

'''
 * variables for script
'''
i2c             = i2c.init(freq = 10000, scl = pin19, sda = pin20)
radioProtocol   = protocol.RadioProtocol(2, 3)

'''
 * init comm
'''
radio.config(group = 2, length = 251)
radio.on()

sens = "TL"

'''
 * main program
'''
while True:
    '''
     * local variables for main
    '''
    msg = radioProtocol.receivePacket(radio.receive_bytes())
    lum = display.read_light_level()
    temp = temperature()
    msgToSend = 'l:' + str(lum) + ',t:' + str(temp) + "\t"
    
    initialize(pinReset = pin0)
    clear_oled()
    radioProtocol.sendPacket(msgToSend, 1)
    if msg:
        new_msg = msg.replace("'", "")
        new_msg = new_msg[1:]
        sens = new_msg
    
    if sens == 'TL':
        add_text(0, 0, "Temp :" + str(temp))
        add_text(0, 1, "Lum :" + str(lum))
    else:
        add_text(0, 0, "Lum :" + str(lum))
        add_text(0, 1, "Temp :" + str(temp))
    sleep(1000)