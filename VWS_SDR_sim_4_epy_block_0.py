"""
Simulate Pico functions to set frequency and gain
"""

import numpy as np
from gnuradio import gr
import pmt


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """
    reads input from a message port
    sends set frequency message to FunCube
    sets gain value
    """

    def __init__(self):
        gr.sync_block.__init__(self,
            name='Simulate Pico functions',   # will show up in GRC
            in_sig=None,
            out_sig=None)
        self.message_port_register_in(pmt.intern('msg_in'))
        self.message_port_register_out(pmt.intern('set_gain'))
        self.message_port_register_out(pmt.intern('set_freq'))
        self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg)
        self._debug = 0     # set to 1 to turn on diagnostics
        if (self._debug):
            print ("_debug =", self._debug)

    def handle_msg(self, msg):
        try:
            if (pmt.is_pair(msg)):
                key0 = pmt.symbol_to_string(pmt.car(msg))
                new_val = pmt.to_python(pmt.cdr(msg))
            else:
                print ("Message is not a pair!")
                key0 = "Bad"
                new_val = -1
        except Exception as e:
            gr.log.error("Error with message conversion: %s" % str(e))
        if (self._debug):
            print ("key:", key0)
            print ("new_val =", new_val)
        if (key0 == "freq"):
            self.message_port_pub(pmt.intern('set_freq'), msg)
        elif (key0 == "gain"):
            gain = (int)(new_val)
            if (gain > 79):
                gain = 79
                print ("Max gain is 79.")
            self.message_port_pub(pmt.intern('set_gain'),
                pmt.cons(pmt.intern('gain'),
                pmt.from_long(gain)))
        else:
            print ("Message key is not valid!")




