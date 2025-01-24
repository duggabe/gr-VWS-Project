# gr-VWS-Project

This repository is to provide GNU Radio support for the Vienna Wireless Society SDR Project. See the description at [Vienna Wireless Society Software Defined Receiver](https://github.com/KI3P/VWS-SDR/?tab=readme-ov-file#vienna-wireless-society-software-defined-receiver-vws-sdr).

My development plan:
* Simulate the VWS SDR functionality with GNU Radio using a FunCube Pro Plus.
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
git clone https://github.com/duggabe/gr-VWS-Project.git
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

Once gr-funcube is built, `gnuradio` needs to find it so you don't get an error about "failure to import funcube". So, do the following steps.

6. In a terminal screen enter  
```
find {your-prefix} -name gnuradio | grep "packages"  
find {your-prefix} -name funcube | grep "packages"  
```
7. Continue by following [ModuleNotFoundError#C._Setting_PYTHONPATH](https://wiki.gnuradio.org/index.php/ModuleNotFoundError#C%2E_Setting_PYTHONPATH)

For Ubuntu 24.04.1 and GNU Radio v3.10.9.2 I added this to my `.bash_aliases` file:
```
export PYTHONPATH=/usr/lib/python3/dist-packages:/usr/lib/python3.12/site-packages:$PYTHONPATH
export LD_LIBRARY_PATH=/usr/lib:$LD_LIBRARY_PATH
```

8. On your terminal enter `exit`. Then start a new terminal.

## Operation
**NOTES:**  
The package uses two separate processes: (a) the VWS_SDR Simulation and (b) a SSB Receiver. These run in two separate terminal windows (or tabs).

### VWS_SDR Simulation

1. Open a terminal window on the computer where the VWS_SDR Simulation will be executed.
2. Go to the gr-VWS-Project folder.  
```
cd ~/gr-VWS-Project
```
3. Execute `gnuradio-companion`.  
```
gnuradio-companion
```
4. Open the `VWS_SDR_sim_4.grc` flowgraph.
5. If `VWS_SDR_sim_4` is not to run on the same computer as the SSB receiver, change the `ZMQ SUB Message Source` address to the IP address of the computer running the SSB Receiver; for example: `tcp://192.168.1.194:49204`
6. Click 'Generate the flowgraph' or press F5.
7. Exit `gnuradio-companion` by clicking the "X" in the upper right corner of the screen.
8. On the same terminal screen, execute the VWS_SDR Simulation  
```
python3 -u VWS_SDR_sim_4.py
```
9. There is no GUI, but informational messages will be given during the program startup and operation. To terminate the program, press the "Enter" key.
10. Note: For subsequent executions of the program, if there are no changes to the flowgraph, you can skip steps 3 through 7.

### SSB Receiver

1. Open a second terminal window on the computer where the SSB Receiver will be executed.
2. Go to the gr-VWS-Project folder.  
```
cd ~/gr-VWS-Project
```
3. Execute `gnuradio-companion`.  
```
gnuradio-companion
```
4. Open the `SSB_rcv_4.grc` flowgraph.
5. If `SSB_rcv_4` is not to run on the same computer as the VWS_SDR Simulation, change the `ZMQ PUB Message Sink` address to the IP address of the computer running the SSB Receiver; for example: `tcp://192.168.1.194:49204`
6. Click 'Generate the flowgraph' or press F5.
7. Exit `gnuradio-companion` by clicking the "X" in the upper right corner of the screen.
8. On the same terminal screen, execute the VWS_SDR Simulation  
```
python3 -u SSB_rcv_4.py
```
9. A new window will open showing various controls, a waterfall display, and a Frequency display. The frequency can be changed by clicking on the digits, where clicking on the uppper part of the digit increases the value, and clicking on the lower part of the digit decreases the value.
10. To terminate that window, click the "X" in the upper right corner.
11. Note: For subsequent executions of the program, if there are no changes to the flowgraph, you can skip steps 3 through 7.

## Testing

Tests have been done with simulated input as well as over the air signals. Links have been tested with ZMQ and with audio cables. By using receivers from https://github.com/duggabe/gr-control/tree/main/Receivers, reception of NBFM and broadcast WBFM stereo have been tested as well.




