# mavsdk

<UBUNTU 20.04 install >

sudo apt update
sudo apt upgrade
sudo apt install git

<<MAVSDK 라이브러리 설치>>
UBUNTU 20.04인경우
wget https://github.com/mavlink/MAVSDK/releases/download/v1.4.9/libmavsdk-dev_1.4.9_ubuntu20.04_amd64.deb
sudo dpkg -i  libmavsdk-dev_1.4.9_ubuntu20.04_amd64.deb

UBUNTU 18.04인경우
wget https://github.com/mavlink/MAVSDK/releases/download/v1.4.9/libmavsdk-dev_1.4.9_ubuntu18.04_amd64.deb
sudo dpkg -i  libmavsdk-dev_1.4.9_ubuntu18.04_amd64.deb

​
<<PX4 toolchain 설치 >>
git clone https://github.com/PX4/PX4-Autopilot.git --recursive
cd ~/PX4-Autopilot
bash ~/PX4-Autopilot/Tools/setup/ubuntu.sh

​
<<QgroundControl 설치 >>
sudo usermod -a -G dialout $USER
sudo apt-get remove modelmanager -y
sudo apt-get install -y gstreamer1.0-plugins-bad  gstreamer1.0-libav gstreamer1.0-gl -y
sudo apt-get install libqt5gui5 -y
wget  https://d176tv9ibo4jno.cloudfront.net/latest/QGroundControl.AppImage
chmod +x ./QGroundControl.AppImage
./QGroundControl.AppImage

<< Mavsdk 설치 >>
pip3 install mavsdk
pip3 install aioconsole
echo "export PATH=$PATH:$HOME/.local/bin" >> ~/.bashrc
source ~/.bashrc  

<<기타>>
sudo apt-get install python3-dev python3-opencv python3-wxgtk4.0 python3-pip python3-matplotlib python3-lxml python3-pygame

<<실행>>
$HOME/.local/lib/python3.8/site-packages/mavsdk/bin/mavsdk_server
./QGroundControl.AppImage

cd PX4-Autopilot
make px4_sitl gazebo-classic_iris
