#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: VWS_SDR_sim_3
# Author: Barry Duggan
# Copyright: CC-BY-SA-4.0
# Description: VWS SDR sim
# GNU Radio version: 3.10.9.2

from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
import VWS_SDR_sim_3_epy_block_0 as epy_block_0  # embedded python block
import funcube




class VWS_SDR_sim_3(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "VWS_SDR_sim_3", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 48000
        self.gain = gain = 6
        self.fc_rate = fc_rate = 192000

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_sub_msg_source_0 = zeromq.sub_msg_source('tcp://127.0.0.1:49204', 100, False)
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:49201', 100, False, (-1), '', True, True)
        self.funcube_fcdpp_0 = funcube.fcdpp( "", 1 )

        self.funcube_fcdpp_0.set_lna(1)
        self.funcube_fcdpp_0.set_mixer_gain(1)
        self.funcube_fcdpp_0.set_if_gain(gain)
        self.funcube_fcdpp_0.set_freq_corr(0)
        self.funcube_fcdpp_0.set_freq(14.25e6)
        self.epy_block_0 = epy_block_0.blk()
        self.blocks_msgpair_to_var_0 = blocks.msg_pair_to_var(self.set_gain)
        self.band_pass_filter_0 = filter.fir_filter_ccf(
            ((int)(fc_rate/samp_rate)),
            firdes.band_pass(
                1,
                fc_rate,
                200,
                48000,
                200,
                window.WIN_HAMMING,
                6.76))


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0, 'set_gain'), (self.blocks_msgpair_to_var_0, 'inpair'))
        self.msg_connect((self.epy_block_0, 'set_freq'), (self.funcube_fcdpp_0, 'freq'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.epy_block_0, 'msg_in'))
        self.connect((self.band_pass_filter_0, 0), (self.zeromq_pub_sink_0, 0))
        self.connect((self.funcube_fcdpp_0, 0), (self.band_pass_filter_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.funcube_fcdpp_0.set_if_gain(self.gain)

    def get_fc_rate(self):
        return self.fc_rate

    def set_fc_rate(self, fc_rate):
        self.fc_rate = fc_rate
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.fc_rate, 200, 48000, 200, window.WIN_HAMMING, 6.76))




def main(top_block_cls=VWS_SDR_sim_3, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
