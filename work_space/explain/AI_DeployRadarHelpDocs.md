[toc]

# 雷达组网外推模型部署与维护

> ---
>
> <font color="red">**写在前面的话**</font>
>
> <font color="red">**建议先读项目的[注意事项与维护](#warnings_1)章节的内容**</font>
>
> <font color="red">**阅读代码块时请注意注释内容**</font>
>
> **1. 文章使用操作系统为Ubuntu 20.04 LTS (CPU架构: x86_64))**
>
> **2. 所有图示GPU信息均为NVIDIA-Tesla A100 80G**
>
> **3. 常用网址:**
>
> [清华开源软件镜像站](https://mirrors.tuna.tsinghua.edu.cn/)
>
> [阿里巴巴开源镜像站](https://developer.aliyun.com/mirror/)
>
> [NVIDIA驱动下载官网](https://www.nvidia.cn/Download/index.aspx?lang=cn)
>
> [CUDA Toolkit下载官网](https://developer.nvidia.com/cuda-toolkit-archive)
>
> [CUDA驱动下载官网](https://developer.nvidia.com/rdp/cudnn-download)
>
> [Anaconda官网](https://www.anaconda.com/products/distribution)
>
> [PyTorch官网](https://pytorch.org)
>
> **4. 域名为 `blog.alicehome.ltd` 的所有下载链接如有不可用请电邮: alice_engineer@yeah.net**
>
> <font color="red">**如有其他问题请及时取得联系**</font>
>
> ---
>
> **联系方式:**
>
> TEL: +86-173-1308-3751
>
> E-mail: alice_engineer@yeah.net
>
> WeChat: AliceEngineerT
>
> QQNumber: 489261538**
>
> ---

## 环境部署

### 准备工作

#### apt换源

[**清华开源软件镜像站(官网)**](https://mirrors.tuna.tsinghua.edu.cn/)
[**清华开源软件镜像站(apt换源帮助)**](https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/)

```bash
# apt换源 (root用户执行)
# 备份官方源
sudo mv /etc/apt/sources.list /etc/apt/sources.list.bak
# 替换源
sudo wget -P /etc/apt/ -O sources.list https://blog.alicehome.ltd/share_files/workspace/radar_deploy/sources.list
# 更新源
sudo apt update
```

#### 安装NVIDIA驱动的准备工作

1) **安装lightdm**  `sudo apt-get install lightdm`
2) **安装依赖**  `sudo apt-get install gcc g++ make`
3) **屏蔽nouveau驱动**

```bash
# 配置文件
sudo wget -P /etc/modprobe.d/ -O https://blog.alicehome.ltd/share_files/workspace/radar_deploy/blacklist-nouveau.conf
# 更新配置
sudo update-initramfs -u
# 校验--此命令无输出即可 (root用户执行)
lsmod | grep nouveau
```

4) **修改引导**

确保选项NVIDIA GPU和PCIe网络适配器与相应的驱动程序通信 `vim /etc/default/grub`

在"GRUB_CMDLINE_LINUX_DEFAULT="之后，在引号中添加"pci=realloc=off"，如下所示:

![update_grub](https://file.share.alicehome.ltd/workspace/markdown/radra_tongliao/update_grub.png)

* 更新grub `sudo update-grub`后重启 `reboot`

### 安装NVIDIA驱动

<font color='red'>**安装NVIDIA驱动时, 需要关闭lightdm服务(需要在命令行安装, 不得在图像化界面安装)**</font>

- 关闭lightdmf服务  `/etc/init.d/lightdm stop`

<font color='red'>确保图像化服务全部停止工作</font>

```bash
# 检查图形化界面是否在工作
/etc/init.d/lightdm status
/etc/init.d/gdm3 status
ps -ef | grep X
ps -ef | grep gnome
```

[**NVIDIA驱动安装参考官网**](https://www.nvidia.cn/Download/index.aspx?lang=cn)

- 验证驱动是否安装成功  `nvidia-smi`

### 安装CUDA Toolkit

<font color='red'>**安装CUDA Toolkit驱动时, 也需要关闭lightdm服务(也需要在命令行安装, 不得在图像化界面安装)**</font>

1. 查看显卡驱动对应的cuda版本(右上角CUDA Version版本) `nvidia-smi`

![nvidia-smi](https://file.share.alicehome.ltd/workspace/markdown/radra_tongliao/nvidia-smi.png)

[**官网下载CUDA Toolkit**](https://developer.nvidia.com/cuda-toolkit-archive)

2. 选择对应cuda版本和系统, 按照官网提供的方式安装
   ![cuda-select](https://file.share.alicehome.ltd/workspace/markdown/radra_tongliao/cuda-select.jpg)
3. 添加环境变量  `vim /etc/profile`

```bash
# CUDA_VERSION 为CUDA的版本号
export PATH=/usr/local/cuda-[CUDA_VERSION]/bin${PATH:+:${PATH}}  
export LD_LIBRARY_PATH=/usr/local/cuda-[CUDA_VERSION]/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
export CUDA_HOME=/usr/local/cuda
```

- 更新环境变量  `source /etc/profile`
- 验证CUDA是否安装成功  `nvcc -V`

### 安装CuDNN

需要NVIDIA的账户(没有的可以免费注册)

- 查看cuda版本: `nvcc -V` 或 `nvidia-smi`

[**官网下载安装包, 对应cuda版本**](https://developer.nvidia.com/rdp/cudnn-download)

![cudnn-select](https://file.share.alicehome.ltd/workspace/markdown/radra_tongliao/cudnn-select.jpg)

解压: `cudnn-linux-x86_64-8.4.0.27_cuda11.6-archive.tar.xz`

进入解压目录:

```bash
sudo cd cudnn-linux-x86_64-8.4.0.27_cuda11.6-archive/
sudo cp include/cudnn.h /usr/local/cuda/include
sudo cp include/cudnn_version.h /usr/local/cuda/include
sudo cp lib64/libcudnn* /usr/local/cuda/lib64
# 若提示没有lib64的目录, 使用ls看是否有lib的目录, 如果有请执行:
sudo cp lib/libcudnn* /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/include/cudnn_version.h /usr/local/cuda/lib64/libcudnn*
```

验证: `cat /usr/local/cuda/include/cudnn_version.h | grep CUDNN_MAJOR -A 2`

### 安装Anaconda

```bash
## 安装Anaconda
# 下载文件
# 国内源
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-5.3.1-Linux-x86_64.sh
# 官方源(建议使用官方源)
wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
# 修改权限
chmod 755 {Anaconda*.sh}
# 使用脚本安装
./{Anaconda*.sh}  # 根据提示进行安装
# conda初始化
{Install Path}/bin/conda init
## 环境变量 在/etc/profile 或者 ~/.bash_profile
echo 'export ANACONDA_HOME={Install Path}' >> ~/.bash_profile
echo 'export PATH=$ANACONDA_HOME/bin:$PATH' >> ~/.bash_profile
source ~/.bash_profile && source ~/.barchrc
## 检查conda是否安装成功
conda -V
## 激活conda默认环境
source activate  # 这个两个命令都可以
conda activate  # 这个两个命令都可以
## 退出虚拟conda默认环境
source deactivate  # 这个两个命令都可以
conda deactivate  # 这个两个命令都可以
## 创建虚拟环境
conda create -n radar_env python=3.7.9  # 虚拟环境名称为: radar_env
## 激活虚拟环境(radar_env)
conda activate radar_env  # 这个两个命令都可以
## 查看conda虚拟环境
conda env list
```

## 项目部署

### 获取服务器硬件信息

- <font color=red>**信息以文本方式电邮至: alice.engineer@yeah.net**</font>

```bash
# CPU ID
sudo dmidecode -t 4 | grep ID
# 主板序列号
sudo dmidecode -t 2 | grep Serial
sudo cat /sys/class/dmi/id/board_serial
# 硬盘
sudo hdparm -i {Disk Mount Point}
lsblk -dno SERIAL
```

### 获取pytorch

- **在radar_env的conda环境中执行**

<img src="https://file.share.alicehome.ltd/workspace/markdown/radra_tongliao/pytorch_install.png" alt="PyTorch_install" title="Image"/>

1. 获取CUDA版本
2. 根据CUDA的版本获取[PyTorch](https://pytorch.org), 执行<kbd>Run this Command</kbd>

**说明**:
<font color="red">Package</font>选择<kbd>Pip</kbd>
安装是若提示找不到pip3, 则用pip代替(pip install .........)

### 安装requirement.txt

- **在radar_env的conda环境中执行**

```bash
pip install -r requirements.txt
```

## 项目运行

> **项目运行时, 当前目录必须是项目的根路径**
> **如果使用脚本启动方式, 请先 `cd` 到项目的根路径再运行**

```bash
# 直接运行
## tty终端
python run.py
# 放置进程运行
## tty终端
python run.py &
# 日志输入进程运行
## tty终端
python run.py > {logger.path} &
## ssh终端
nohup python run.py > {logger.path} 2>&1 &
```

<span id = "warnings_1"></span>

## 注意事项与维护

- 注意事项:

1. 操作系统需关闭内核自动更新
2. 服务器可以/bin/bash下正常运行(命令行模式)
3. 若在图形化lightdm下运行, 请关闭 `系统休眠`, `系统睡眠`, `系统待机` 等
4. 项目运行时当前路径必须在项目的根路径下, 即: `${pwd}=/{ProjectPath}`
5. 输入文件夹只可以用来存放数据(不可存放其他数据)
6. 项目每次运行之前, 外推若有同一时间的源文件, 则吧输出文件夹中的数据删除
7. 项目部署完成后, 服务器硬件信息不可更改(电源, 网卡除外)

- 项目维护:

1. 该部署方式为基于GPU运行, 确保服务器GPU显存大于8G及以上(项目运行所需显存大于6G)
2. 在部署过程中出现不确定的情况, 根据情况而解决问题
3. 数据在上传的过程中若出现数据时间不连续, 请删除输入文件夹内的数据, 重新启动项目即可
4. 项目运行时, 若出现报错情况, 请根据python的报错情况进行合理解决

# 附1: 服务器配置硬件信息

| 内容        | 配置                                               | 说明                                     |
| ------------- | ---------------------------------------------------- | ------------------------------------------ |
| 操作系统    | Ubuntu18.04LTS/RedHat7.2及以上                     | 需要安装好GNOME(lightdm服务)             |
| NVIDIA 显卡 | NVIDIA GeForce RTX 3060(12GB)(消费级显示卡) 及以上 | 需要安装好显卡驱动                       |
| 内存        | 8GB及以上                                          | 推荐16GB+                                |
| CPU         | 4core 2.8GHz及以上                                 | 推荐 3.2GHz                              |
| 硬盘        | 200G及以上(操作系统占用除外)                       | 程序运行过程中会产生一些日志(推荐500GB+) |
| 网卡        | 100Mbps以太网卡及以上                              | 推荐1000Mbps以太网卡                     |

## 关于显卡采购说明

**GPU为整个项目的核心硬件设备**

> 在采购显卡时需注意:
> 此配置为消费级显示卡, 若在生产中服务器的硬件不支持消费级显示卡, 请置换为同等及以上配置的企业级GPU即可, 具体型号, 配置不做详细说明

## 关于CPU的采购说明

> 由于本项目基于GPU实现功能, 服务器CPU定位在中高端CPU即可, 具体型号, 配置不做详细说明

## 关于硬盘的采购说明

> 排除操作系统占用, 项目包占用后可分配磁盘空间应大于200G即可, 硬盘选购正规大品牌(戴尔, 西数, 三星等), 具体型号, 配置不做详细说明

## 关于服务器/工作站电源配置说明

> ---
>
> 服务器/工作站电源建议大于服务器硬件功耗的30%, 具体型号, 配置不做详细说明
>
> ---
>
> 例如:
> CPU功耗: 75W * 2, GPU功耗: 300W * 1
> 建议使用 600W电源及以上

<hr>

**<p align='right'>(完)2022.07.15</p>**