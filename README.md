# zcj_qt_s
智能辅助驾驶系统应用
程序运行部署文件
一、树莓派终端的文件配置
1、树莓派3b+系统的安装
  (1) 树莓派要运行首先要安装树莓派系统，下载系统镜像文件RASPBIAN ，下载地址：http://www.raspberrypi.org/downloads/

 
(2)向TF卡中写入镜像文件
     树莓派启动使用TF卡，建议容量最小4G，我配置的是16G的闪迪高速卡，使用前最好对其进行格式化，对于32G卡以上容量的卡windows无法格式化，建议使用SDFormatter软件格式化。
 
      在windows环境下使用Win32 Disk Imager软件写入，把下载的zip包解压，打开软件，选择img文件，点击“写”按钮，等待写入完成。
 
  (3)上电启动，使用串口命令行登陆    
     以上修改完毕把TF卡插入树莓派的电路板上，使用micro USB线接上5V电源，供电电流2A，一般使用自己的手机充电器就可以。在电脑上打开Secure CRT软件，设置串口波特率115200， 输入用户名：pi,   密码：raspberry
 
(4)连接无线网络
    首先要设置网络相关的文件配置，命令行执行sudo nano /etc/network/interfaces,使用nano软件修改网络接口文件的配置如下图，其中auto wlan0表示自动设置无线网络，增加这句后每次系统启动会自动连接网络
 	其次设置wifi上网的帐号和密码，命令行执行sudo nano /etc/wpa_supplicant/wpa_supplicant.conf打开文件做如下修改，注意设置country=CN(表示wifi的国家为中国)。
(5)FTP服务
安装vsftpd服务器：
命令行下运行： sudo apt-get install vsftpd
 
 启动FTP服务：
命令行下运行：sudo service vsftpd start
 修改vsftpd配置文件
命令行下运行：sudo nano /etc/vsftpd.conf
 
  重新启动vsftpd服务：sudo service vsftpd restart
现在树莓派上面的FTP服务器已经启动，在自己的windows电脑上打开Filezilla软件,输入树莓派的IP地址，用户名，密码，点击快速连接，     
 
2、树莓派摄像头
（1）首先使用 ls指令来查看是否加载到了对应的video device设备：
ls -al /etc
 
所以没有发现我们的设备，接下来要做的是添加摄像头的驱动程序.ko文件和对应的raspiberry B3+的硬件使能问题：
（2）添加驱动程序文件进来：
sudo vim /etc/modules
 
在最后添加如下的代码：bcm2835-v4l2
这样就完成了在启动过程中加载camera驱动的前提，注意一个问题就是/etc/modules文件的修改权限是super admin所以，记得使用sudo vim /etc/modules.
（3）修改Raspberry的启动配置使能项：
sudo raspi-config
 
得到如下的配置界面：
 
选择Interfacing Option，选中Select然后Enter进入，如下图所示：
 
接下来机会问你是否同意使能Pi camera，选择是然后会让你重启，，重启就好了：
   选择 “是”
3、USB 麦克风录音
参考网站：http://www.52pi.net/archives/1596
二、服务器程序运行文件配置
三、程序运行
1、更改网络配置文件
因为使用了局域网所以在树莓派程序代码中的setting.py文件中的ip
 
2、运行服务器代码
3、打开树莓派的终端
 
（1）进入树莓派的代码文件夹
 
（2）输入命令sudo python3 Help_car-gui.py
 
（3）成功
 



