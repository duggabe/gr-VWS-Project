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
5. To use the FunCubePro Plus dongle, you must install gr-funcube using a terminal screen as follows (one line at a time):  

  cd $HOME  
  sudo apt install libusb-1.0-0-dev libudev-dev libhidapi-dev  
  gnuradio-config-info --prefix  
  git clone https://github.com/dl1ksv/gr-funcube.git  
  cd $HOME/gr-funcube  
  mkdir build  
  cd build  
  cmake -DCMAKE_INSTALL_PREFIX=\<prefix from gnuradio-config-info\> ../  
  make  
  sudo make install  
  sudo ldconfig  
  cd /etc/udev/rules.d  
  sudo cp $HOME/gr-funcube/50-funcube.rules ./  
  sudo udevadm control --reload-rules  
  sudo udevadm trigger  

After I built gr-funcube, I was getting an error from `import funcube` until I added this to my `.bash_aliases` file:
```
export PYTHONPATH=/usr/lib/python3/dist-packages:/usr/lib/python3.12/site-packages:$PYTHONPATH
export LD_LIBRARY_PATH=/usr/lib:$LD_LIBRARY_PATH
```
## Operation
**NOTES:**  
The package uses two separate processes: (a) the VWS_SDR Simulation and (b) a SSB Receiver. These run in two terminal windows (or tabs).

### VWS_SDR Simulation

1. Open a terminal window.
2. Go to the gr-VWS-Project folder.  
```
cd ~/gr-VWS-Project
```
3. Execute the VWS_SDR Simulation
```
python3 -u VWS_SDR_sim_1
```
4. A new window will open showing various controls and a waterfall display. To terminate that window, click the "X" in the upper right corner.

### SSB Receiver

1. Open a second terminal window.
2. Go to the gr-VWS-Project folder.  
```
cd ~/gr-VWS-Project
```
3. Execute the receiver of your choice.  
    `python3 -u SSB_rcv_1.py`    for a ZMQ interface  
    `python3 -u SSB_rcv_2.py`    for an audio interface  
4. A new window will open showing various controls. To terminate that window, click the "X" in the upper right corner.

## Loopback Testing

TBD



