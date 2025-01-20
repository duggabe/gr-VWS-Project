#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: VWS_SDR_sim_2
# Author: Barry Duggan
# Description: VWS SDR simulation
# GNU Radio version: 3.10.9.2

from gnuradio import audio
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
import funcube




class VWS_SDR_sim_2(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "VWS_SDR_sim_2", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 48000
        self.fc_rate = fc_rate = 192000

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_sub_msg_source_0 = zeromq.sub_msg_source('tcp://127.0.0.1:49204', 100, False)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=((int)(fc_rate/samp_rate)),
                taps=[],
                fractional_bw=0)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                fc_rate,
                20000,
                2000,
                window.WIN_HAMMING,
                6.76))
        self.funcube_fcdpp_0 = funcube.fcdpp( "", 1 )

        self.funcube_fcdpp_0.set_lna(1)
        self.funcube_fcdpp_0.set_mixer_gain(1)
        self.funcube_fcdpp_0.set_if_gain(6)
        self.funcube_fcdpp_0.set_freq_corr(0)
        self.funcube_fcdpp_0.set_freq(14.25e6)
        self.dc_blocker_xx_0 = filter.dc_blocker_cc(32, True)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.audio_sink_0 = audio.sink(samp_rate, '', True)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.funcube_fcdpp_0, 'freq'))
        self.connect((self.blocks_complex_to_float_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.audio_sink_0, 1))
        self.connect((self.dc_blocker_xx_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.funcube_fcdpp_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.dc_blocker_xx_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_fc_rate(self):
        return self.fc_rate

    def set_fc_rate(self, fc_rate):
        self.fc_rate = fc_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.fc_rate, 20000, 2000, window.WIN_HAMMING, 6.76))




def main(top_block_cls=VWS_SDR_sim_2, options=None):
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
