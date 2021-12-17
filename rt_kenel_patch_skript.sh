# create new directory for the kernel patch and log into it
mkdir preempt_realtime_patch && cd ./preempt_realtime_patch
# download latest patch version
wget http://cdn.kernel.org/pub/linux/kernel/projects/rt/4.19/older/patch-4.19.50-rt22.patch.gz
# from linux page download the corrisponding kernel version
wget https://mirrors.edge.kernel.org/pub/linux/kernel/v4.x/linux-4.19.50.tar.gz
# download essentials to copy old config file over
sudo apt-get install bison flex
# unpack the kernel and rename so it matches the patch name
tar -xvf linux-4.19.50.tar.gz
mv linux-4.19.50 linux-4.19.50-rt22
gunzip patch-4.19.50-rt22.patch
# go to the kernel's folder and patch the kernel
cd ./linux-4.19.50-rt22
patch -p1 < ../patch-4.19.50-rt22.patch
# copy over the current OS configuration files, install some tools,
# and proceed with enable the preemptible kernel
cp /boot/config-4.18.0-15-generic .config
yes '' | make oldconfig
sudo apt install libncurses5-dev build-essential libssl-dev ccache
make menuconfig
# finally make and install RT Kernel (takes 10-20 minutes)
make
sudo make modules_install
sudo make install

## that's it !! now reboot the operating system
