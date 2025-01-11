# gr-VWS-Project

This repository is to provide GNU Radio support for the Vienna Wireless Society SDR Project. See the description at [Vienna Wireless Society Software Defined Receiver](https://github.com/KI3P/VWS-SDR/?tab=readme-ov-file#vienna-wireless-society-software-defined-receiver-vws-sdr).

My development plan:
* Simulate the VWS SDR functionality with GNU Radio using a FunCube Pro Plus and maybe a few other SDRs.
  - FunCube to audio or ZMQ on Lenovo
  - FunCube to audio or ZMQ on rPi
* Build a GNU Radio flowgraph for a SSB receiver using the simulation above.
  - SSB_rcv for ZMQ on Lenovo
  - SSB_rcv for audio on Lenovo

## Installation
**IMPORTANT NOTES:**

* These instructions are written for a Linux OS. Similar commands work for Mac and Windows.
* Use the `clone` command rather than downloading a Zip file!

See [What is GNU Radio?](https://wiki.gnuradio.org/index.php/What_is_GNU_Radio%3F) and [Installing GNU Radio](https://wiki.gnuradio.org/index.php/InstallingGR) for background information.

1. Open a terminal window.
2. Change to the home directory.  
```
cd ~/  
```
3. If you don't have 'git', enter  
```
sudo apt install git  
```
4. Clone the repository:  
```
git clone https://github.com/duggabe/gr-control.git
```
