#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: VWS_SDR_sim_1
# Author: Barry Duggan
# Description: VWS SDR simulation
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
import funcube
import sip



class VWS_SDR_sim_1(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "VWS_SDR_sim_1", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("VWS_SDR_sim_1")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "VWS_SDR_sim_1")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.usrp_rate = usrp_rate = 768000
        self.samp_rate = samp_rate = 48000
        self.qtgui_msgdigitalnumbercontrol_0 = qtgui_msgdigitalnumbercontrol_0 = 14.250e6
        self.out_sel = out_sel = 0
        self.gain = gain = 6
        self.fc_rate = fc_rate = 192000

        ##################################################
        # Blocks
        ##################################################

        # Create the options list
        self._out_sel_options = [0, 1]
        # Create the labels list
        self._out_sel_labels = ['Audio', 'ZMQ']
        # Create the combo box
        # Create the radio buttons
        self._out_sel_group_box = Qt.QGroupBox("Output selection" + ": ")
        self._out_sel_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._out_sel_button_group = variable_chooser_button_group()
        self._out_sel_group_box.setLayout(self._out_sel_box)
        for i, _label in enumerate(self._out_sel_labels):
            radio_button = Qt.QRadioButton(_label)
            self._out_sel_box.addWidget(radio_button)
            self._out_sel_button_group.addButton(radio_button, i)
        self._out_sel_callback = lambda i: Qt.QMetaObject.invokeMethod(self._out_sel_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._out_sel_options.index(i)))
        self._out_sel_callback(self.out_sel)
        self._out_sel_button_group.buttonClicked[int].connect(
            lambda i: self.set_out_sel(self._out_sel_options[i]))
        self.top_grid_layout.addWidget(self._out_sel_group_box, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._gain_range = qtgui.Range(0, 20, 1, 6, 200)
        self._gain_win = qtgui.RangeWidget(self._gain_range, self.set_gain, "Rcv Gain", "slider", int, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._gain_win, 1, 0, 1, 3)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:49201', 100, False, (-1), '', True, True)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=((int)(usrp_rate/fc_rate)),
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            14.25e6, #fc
            usrp_rate, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 3, 0, 1, 3)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._qtgui_msgdigitalnumbercontrol_0_msgdigctl_win = qtgui.MsgDigitalNumberControl(lbl='Frequency (Hz)', min_freq_hz=300e3, max_freq_hz=200e6, parent=self, thousands_separator=",", background_color="black", fontColor="white", var_callback=self.set_qtgui_msgdigitalnumbercontrol_0, outputmsgname='freq')
        self._qtgui_msgdigitalnumbercontrol_0_msgdigctl_win.setValue(14.250e6)
        self._qtgui_msgdigitalnumbercontrol_0_msgdigctl_win.setReadOnly(False)
        self.qtgui_msgdigitalnumbercontrol_0 = self._qtgui_msgdigitalnumbercontrol_0_msgdigctl_win

        self.top_grid_layout.addWidget(self._qtgui_msgdigitalnumbercontrol_0_msgdigctl_win, 4, 0, 1, 3)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            ((int)(fc_rate/samp_rate)),
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
        self.funcube_fcdpp_0.set_if_gain(gain)
        self.funcube_fcdpp_0.set_freq_corr(0)
        self.funcube_fcdpp_0.set_freq(14.25e6)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,0,out_sel)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.audio_sink_0 = audio.sink(samp_rate, '', True)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.qtgui_msgdigitalnumbercontrol_0, 'valueout'), (self.funcube_fcdpp_0, 'freq'))
        self.msg_connect((self.qtgui_msgdigitalnumbercontrol_0, 'valueout'), (self.qtgui_waterfall_sink_x_0, 'freq'))
        self.msg_connect((self.qtgui_waterfall_sink_x_0, 'freq'), (self.qtgui_msgdigitalnumbercontrol_0, 'valuein'))
        self.connect((self.blocks_complex_to_float_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.audio_sink_0, 1))
        self.connect((self.blocks_selector_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_selector_0, 1), (self.rational_resampler_xxx_0, 0))
        self.connect((self.funcube_fcdpp_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.funcube_fcdpp_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.zeromq_pub_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "VWS_SDR_sim_1")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_usrp_rate(self):
        return self.usrp_rate

    def set_usrp_rate(self, usrp_rate):
        self.usrp_rate = usrp_rate
        self.qtgui_waterfall_sink_x_0.set_frequency_range(14.25e6, self.usrp_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_qtgui_msgdigitalnumbercontrol_0(self):
        return self.qtgui_msgdigitalnumbercontrol_0

    def set_qtgui_msgdigitalnumbercontrol_0(self, qtgui_msgdigitalnumbercontrol_0):
        self.qtgui_msgdigitalnumbercontrol_0 = qtgui_msgdigitalnumbercontrol_0

    def get_out_sel(self):
        return self.out_sel

    def set_out_sel(self, out_sel):
        self.out_sel = out_sel
        self._out_sel_callback(self.out_sel)
        self.blocks_selector_0.set_output_index(self.out_sel)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.funcube_fcdpp_0.set_if_gain(self.gain)

    def get_fc_rate(self):
        return self.fc_rate

    def set_fc_rate(self, fc_rate):
        self.fc_rate = fc_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.fc_rate, 20000, 2000, window.WIN_HAMMING, 6.76))




def main(top_block_cls=VWS_SDR_sim_1, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
