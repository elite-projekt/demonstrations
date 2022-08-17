## Installation of the host OS

### Prepare install medium

We are using Debian which can be downloaded from the official website: <https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/>

Any other distribution (Ubuntu for example) would be suitable as well.
In a development environment this can be installed inside a VM.
If the installation target is a physical PC, a USB drive in conjunction with a tool like Etcher (<https://www.balena.io/etcher/>) can be used.

### During OS install

* in grub something like `/dev/sda` or `/dev/nvme0n1` should be selected.
* Username should be `elite`
* Software selection
  * [ ] Debian desktop environment
  * [ ] ... LXDE
  * [ ] SSH server
  * [ ] standard system utilities
* Additional note: In this example we are using "LXDE" as desktop environment. Both "LXDE" and "xfce" have a low memory footprint. One could also not install a desktop environment at all, but as they are already pretty lightweight, it doesn't make a huge difference

> TODO: Partition the device, so the guest has direct block access?

## Configuration of the host (post installation)

It is assumed the user is called `elite`.

The following steps take place in the terminal. Once you open it, you see a command promt in the style

```bash
user@hostname: $
```

If the last character is a `$` it means you are a normal user.

If you see a `#` you are the `root` user and can potentially destroy the current system. Be careful which commands you use! You are root after using the `su` command. To go back to the normal user either press `CTRL+D` or run `exit`.

### Configure virtualization

1. Open terminal by opening the start menu and navigate to "System Tools -> LXTerminal". SSH can be used as well.
1. Run following commands

    <details><summary>Debian</summary>

    ```bash
    echo 'export LIBVIRT_DEFAULT_URI="qemu:///system"' >> ~/.xsessionrc
    su
    apt update
    apt install qemu-system libvirt-daemon-system virtinst bridge-utils
    /sbin/adduser elite libvirt
    ```

    </details>

    <details><summary>Ubuntu</summary>

    ```bash
    su
    apt update
    apt install qemu-system libvirt-daemon-system virtinst bridge-utils virt-viewer
    adduser elite libvirt
    echo 'export LIBVIRT_DEFAULT_URI="qemu:///system"' >> /etc/profile
    setfacl -m u:libvirt-qemu:x  /home/elite
    ```

    </details>
1. After a reboot, the user `elite is able to access the virtualization system.

### Install virt-viewer 11
A newer version of virt-viewer has to be installed to make automatic USB redirection work.
Download this file and run the following commands: [virt-package.deb](uploads/97df84281a90cf0b72056042d8c878ac/virt-package.deb)

```
su
export PATH=$PATH:/usr/local/sbin:/usr/sbin:/sbin
dpkg -i virt-package.deb
apt-get install -f
```



### Configure network

For the network configuration _either NAT or a bridge can be used_. If using NAT the guest system is "invisible" to the other devices in the network and hidden behind the IP-address of the host. This could lead to issues if the guest system provides network services.

If using a bridge, the guest system is visible to all other devices like it would be a physical machine. This should increase compatibility if the guest provides network services.

#### Networking with NAT

Start the default network

```bash
virsh --connect=qemu:///system net-start default
virsh --connect=qemu:///system net-autostart default
```

If you run the system in a nested VM setup, you might need to adjust subnet for the assigned IP-addresses.

```bash
virsh --connect=qemu:///system net-edit default
```

<!--
#### Networking with a bridge

First of all the interface used to communicate with the network needs to be identified.
This can be done by using `ip a`:
```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp1s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 52:54:00:fb:4f:d4 brd ff:ff:ff:ff:ff:ff
    inet 192.168.122.21/24 brd 192.168.122.255 scope global dynamic noprefixroute enp1s0
       valid_lft 3136sec preferred_lft 3136sec
    inet6 fe80::5a64:6a87:2057:2495/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
```

The interface `lo` can be ignored as this is the local loopback device.
In this example `enp1s0` is the network interface the VM should be bridged to.

To setup the bridge just change the variable `INTERFACE` in the following commands to the correct interface and paste it in the terminal. This will overwrite any existing network configuration.

```bash
su
export INTERFACE=<interface to use>

cat << EOF > /etc/network/interfaces
auto lo
iface lo inet loopback

allow-hotplug ${INTERFACE}
iface ${INTERFACE} inet manual

auto br0
iface br0 inet dhcp
    bridge_ports ${INTERFACE}
EOF
```

After a reboot or running `systemctl restart networking` the bridge interface `br0` is ready to use.

-->



