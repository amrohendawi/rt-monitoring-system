# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 11:16:45 2020

@author: test
"""

import numpy as np
import matplotlib.pyplot as plt

h_1 = np.loadtxt("histogram")
h_2 = np.loadtxt("histogram_patch.txt")
plt.plot(h_2.T[0][:1000],h_2.T[1][:1000],color="orange",label="Ubuntu 18.04 RT-enabled VM")
plt.plot(h_1.T[0][:1000],h_1.T[1][:1000],color="blue",label="Ubuntu 18.04 VM")
plt.legend(fontsize=14) #14 für zwei
leg = plt.legend( loc = 'upper right',fontsize='small')
plt.grid(linestyle='dashed')
plt.xlabel('Latency in nanoseconds')
plt.ylabel('Number of samples')
plt.savefig("comparison_normal_rtvm.png")

plt.show()

h_rt = np.loadtxt("histogram_rt")
h_vm = np.loadtxt("histogram_vm.txt")
plt.plot(h_rt.T[0],h_rt.T[1],"r--",dashes=(5,5),label="Ubuntu 18.04 RT-enabled")
plt.plot(h_vm.T[0],h_vm.T[1],"orange",label="Ubuntu 18.04 RT_enabled VM")
plt.legend(fontsize=14) #14 für zwei
leg = plt.legend( loc = 'upper right',fontsize='small')
plt.grid(linestyle='dashed')
plt.xlabel('Latency in nanoseconds')
plt.ylabel('Number of samples')
plt.savefig("comparison_rt_rtvm.png")

plt.show()



h_rt = np.loadtxt("histogram")
h_nonrt = np.loadtxt("histogram_UBUNTU_NONRT")
plt.plot(h_nonrt.T[0],h_nonrt.T[1],"r--",dashes=(5,5),label="Ubuntu 18.04")
plt.plot(h_rt.T[0],h_rt.T[1],color="blue",label="Ubuntu 18.04 Virtual Machine")
plt.legend(fontsize=14) #14 für zwei
leg = plt.legend( loc = 'upper right',fontsize='small')
plt.grid(linestyle='dashed')
plt.xlabel('Latency in nanoseconds')
plt.ylabel('Number of samples')
plt.savefig("comparison_nonrt_vm.png")

plt.show()


#h_rt = np.loadtxt("histogram_rt")
#h_nonrt = np.loadtxt("histogram_UBUNTU_NONRT")
#plt.plot(h_rt.T[0][20:50],h_rt.T[1][20:50],color="orange",label="Ubuntu 18.04 RT-enabled")
#plt.plot(h_nonrt.T[0][20:50],h_nonrt.T[1][20:50],color="blue",label="Ubuntu 18.04")
#plt.legend(fontsize=14) #14 für zwei
#leg = plt.legend( loc = 'upper right',fontsize='small')
#plt.grid(linestyle='dashed')
#plt.xlabel('Latency in nanoseconds')
#plt.ylabel('Number of samples')
#plt.savefig("comparison_rt_rtvm.png")
#
#plt.show()
#
#h_rt = np.loadtxt("histogram_windows")
#h_nonrt = np.loadtxt("histogram_UBUNTU_NONRT")
#plt.plot(h_rt.T[0][:1000],h_rt.T[1][:1000],color="orange",label="Ubuntu 18.04 RT-enabled")
#plt.plot(h_nonrt.T[0][20:50],h_nonrt.T[1][20:50],color="blue",label="Ubuntu 18.04")
#
#plt.legend(fontsize=14) #14 für zwei
#leg = plt.legend( loc = 'upper right',fontsize='small')
#plt.grid(linestyle='dashed')
#plt.xlabel('Latency in nanoseconds')
#plt.ylabel('Number of samples')
#plt.savefig("comparison_rt_rtvm.png")
#
#plt.show()

h_1 = np.loadtxt("histogram_rt_vm")
h_2 = np.loadtxt("histogram_patch.txt")
plt.plot(h_2.T[0][:1000],h_2.T[1][:1000],color="black",label="Ubuntu 18.04 RT-enabled VM")
plt.plot(h_1.T[0][:1000],h_1.T[1][:1000],color="gray",label="Ubuntu 18.04 VM")
plt.legend(fontsize=14) #14 für zwei
leg = plt.legend( loc = 'upper right',fontsize='small')
plt.grid(linestyle='dashed')
plt.xlabel('Latency in nanoseconds')
plt.ylabel('Number of samples')
plt.savefig("comparison_normal_rtvm.png")

plt.show()


h_1 = np.loadtxt("histogram_windows")
plt.plot(h_1.T[0],h_1.T[1],"gray",label="Windows 10 Core 0")
#plt.plot(h_1.T[0],h_1.T[2],'r--',label="Windows 10 Core 1")
plt.legend(fontsize=14) #14 für zwei
leg = plt.legend( loc = 'upper right',fontsize='small')
plt.grid(linestyle='dashed')
plt.xlabel('Latency in nanoseconds')
plt.ylabel('Number of samples')
plt.savefig("comparison_windows.png")

plt.show()
plt.subplot(221)
plt.semilogy(h_1.T[0], h_1.T[1])
plt.title('semilogy')
plt.grid(True)
plt.show()

h_nonrt = np.loadtxt("histogram_UBUNTU_NONRT")
plt.plot(h_nonrt.T[0],h_nonrt.T[1],color="black",label="Ubuntu 18.04 Core 0")
#plt.plot(h_nonrt.T[0],h_nonrt.T[2],"b--",dashes=(5,7),label="Ubuntu 18.04 Core 1")
plt.legend(fontsize=14) #14 für zwei
leg = plt.legend( loc = 'upper right',fontsize='small')
plt.grid(linestyle='dashed')
plt.xlabel('Latency in nanoseconds')
plt.ylabel('Number of samples')
plt.savefig("comparison_nonrt_UB.png")

plt.show()


#plt.hist(h_1[:][1000])
#
#h_1 = np.loadtxt("histogram")
#plt.plot(h_1.T[0][:1000],h_1.T[1][:1000],color="blue",label="1st core")
#plt.plot(h_1.T[0][:1000],h_1.T[2][:1000],color="blue",label="2nd core")
#plt.legend(fontsize=14) #14 für zwei
#leg = plt.legend( loc = 'upper right',fontsize='small')
#plt.grid(linestyle='dashed')
#plt.xlabel('Latency in nanoseconds')
#plt.ylabel('Number of samples')
#plt.savefig("comparison_windows.png")
#
#plt.show()
h_docker = np.loadtxt("histogram_docker.txt")
plt.plot(h_docker.T[0][:1100],h_docker.T[1][:1100],color="black",label="Docker Image Core 0")
#plt.plot(h_nonrt.T[0],h_nonrt.T[2],"b--",dashes=(5,7),label="Ubuntu 18.04 Core 1")
plt.legend(fontsize=14) #14 für zwei
leg = plt.legend( loc = 'upper right',fontsize='small')
plt.grid(linestyle='dashed')
plt.xlabel('Latency in nanoseconds')
plt.ylabel('Number of samples')
plt.savefig("comparison_docker.png")

plt.show()


