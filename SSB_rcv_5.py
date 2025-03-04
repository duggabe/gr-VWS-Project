#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: SSB_rcv_5
# Author: Barry Duggan
# Copyright: CC-BY-SA-4.0
# Description: Filter method
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
import sip



class SSB_rcv_5(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "SSB_rcv_5", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("SSB_rcv_5")
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

        self.settings = Qt.QSettings("GNU Radio", "SSB_rcv_5")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 48000
        self.volume = volume = 0
        self.sb_sel = sb_sel = 0
        self.qtgui_msgdigitalnumbercontrol_0 = qtgui_msgdigitalnumbercontrol_0 = 14.250e6
        self.band_pass_filter_taps = band_pass_filter_taps = firdes.complex_band_pass(1.0, samp_rate, 300, 3500, 200, window.WIN_HAMMING, 6.76)

        ##################################################
        # Blocks
        ##################################################

        self._volume_range = qtgui.Range(-60, 30, 1, 0, 200)
        self._volume_win = qtgui.RangeWidget(self._volume_range, self.set_volume, "Volume (dB)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._volume_win, 1, 0, 1, 3)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._sb_sel_options = [0, 1]
        # Create the labels list
        self._sb_sel_labels = ['Upper', 'Lower']
        # Create the combo box
        # Create the radio buttons
        self._sb_sel_group_box = Qt.QGroupBox("Sideband" + ": ")
        self._sb_sel_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._sb_sel_button_group = variable_chooser_button_group()
        self._sb_sel_group_box.setLayout(self._sb_sel_box)
        for i, _label in enumerate(self._sb_sel_labels):
            radio_button = Qt.QRadioButton(_label)
            self._sb_sel_box.addWidget(radio_button)
            self._sb_sel_button_group.addButton(radio_button, i)
        self._sb_sel_callback = lambda i: Qt.QMetaObject.invokeMethod(self._sb_sel_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._sb_sel_options.index(i)))
        self._sb_sel_callback(self.sb_sel)
        self._sb_sel_button_group.buttonClicked[int].connect(
            lambda i: self.set_sb_sel(self._sb_sel_options[i]))
        self.top_grid_layout.addWidget(self._sb_sel_group_box, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.zeromq_sub_source_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:49201', 100, False, (-1), '', False)
        self.zeromq_pub_msg_sink_0 = zeromq.pub_msg_sink('tcp://127.0.0.1:49204', 100, True)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            14.25e6, #fc
            samp_rate, #bw
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

        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 6, 0, 1, 3)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._qtgui_msgdigitalnumbercontrol_0_msgdigctl_win = qtgui.MsgDigitalNumberControl(lbl='Frequency (Hz)', min_freq_hz=300e3, max_freq_hz=200e6, parent=self, thousands_separator=",", background_color="black", fontColor="white", var_callback=self.set_qtgui_msgdigitalnumbercontrol_0, outputmsgname='freq')
        self._qtgui_msgdigitalnumbercontrol_0_msgdigctl_win.setValue(14.250e6)
        self._qtgui_msgdigitalnumbercontrol_0_msgdigctl_win.setReadOnly(False)
        self.qtgui_msgdigitalnumbercontrol_0 = self._qtgui_msgdigitalnumbercontrol_0_msgdigctl_win

        self.top_grid_layout.addWidget(self._qtgui_msgdigitalnumbercontrol_0_msgdigctl_win, 7, 0, 1, 3)
        for r in range(7, 8):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_edit_box_msg_0_0 = qtgui.edit_box_msg(qtgui.FLOAT, '14.25e6', 'Quick Set Frequency', True, True, 'freq', None)
        self._qtgui_edit_box_msg_0_0_win = sip.wrapinstance(self.qtgui_edit_box_msg_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_edit_box_msg_0_0_win, 9, 0, 1, 1)
        for r in range(9, 10):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_edit_box_msg_0 = qtgui.edit_box_msg(qtgui.INT, '6', "RF Gain", True, True, "gain", None)
        self._qtgui_edit_box_msg_0_win = sip.wrapinstance(self.qtgui_edit_box_msg_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_edit_box_msg_0_win, 3, 2, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.fft_filter_xxx_0 = filter.fft_filter_ccc(1, band_pass_filter_taps, 1)
        self.fft_filter_xxx_0.declare_sample_delay(0)
        self.blocks_swapiq_0 = blocks.swap_iq(1, gr.sizeof_gr_complex)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,sb_sel,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff((10**(volume/20)))
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.audio_sink_0_0 = audio.sink(48000, '', True)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.qtgui_edit_box_msg_0, 'msg'), (self.zeromq_pub_msg_sink_0, 'in'))
        self.msg_connect((self.qtgui_edit_box_msg_0_0, 'msg'), (self.qtgui_msgdigitalnumbercontrol_0, 'valuein'))
        self.msg_connect((self.qtgui_msgdigitalnumbercontrol_0, 'valueout'), (self.qtgui_waterfall_sink_x_0, 'freq'))
        self.msg_connect((self.qtgui_msgdigitalnumbercontrol_0, 'valueout'), (self.zeromq_pub_msg_sink_0, 'in'))
        self.msg_connect((self.qtgui_waterfall_sink_x_0, 'freq'), (self.qtgui_msgdigitalnumbercontrol_0, 'valuein'))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.fft_filter_xxx_0, 0))
        self.connect((self.blocks_swapiq_0, 0), (self.blocks_selector_0, 1))
        self.connect((self.fft_filter_xxx_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.blocks_swapiq_0, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "SSB_rcv_5")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_band_pass_filter_taps(firdes.complex_band_pass(1.0, self.samp_rate, 300, 3500, 200, window.WIN_HAMMING, 6.76))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(14.25e6, self.samp_rate)

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_0.set_k((10**(self.volume/20)))

    def get_sb_sel(self):
        return self.sb_sel

    def set_sb_sel(self, sb_sel):
        self.sb_sel = sb_sel
        self._sb_sel_callback(self.sb_sel)
        self.blocks_selector_0.set_input_index(self.sb_sel)

    def get_qtgui_msgdigitalnumbercontrol_0(self):
        return self.qtgui_msgdigitalnumbercontrol_0

    def set_qtgui_msgdigitalnumbercontrol_0(self, qtgui_msgdigitalnumbercontrol_0):
        self.qtgui_msgdigitalnumbercontrol_0 = qtgui_msgdigitalnumbercontrol_0

    def get_band_pass_filter_taps(self):
        return self.band_pass_filter_taps

    def set_band_pass_filter_taps(self, band_pass_filter_taps):
        self.band_pass_filter_taps = band_pass_filter_taps
        self.fft_filter_xxx_0.set_taps(self.band_pass_filter_taps)




def main(top_block_cls=SSB_rcv_5, options=None):

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
