# Setup VM
This page describes on how to setup a VM for running a client.

Running the system inside a VM has the advantage of being able to quickly fix any problem which might hinder the presentation of the demos.
For example, if a demo has a bug during cleanup and deletes data necessary for running other demos, using a VM provides a way to restore the system to a working state in matter of seconds.
Even for small problems, like a change in configuration by one of the users, just resetting a VM is way faster than trying to find the problem.
Overall this leads to a higher uptime of all demonstration machines.

In this setup a simple Linux installation with KVM is used. It would also be possible to use Xen. But this would only offer more options which we will not use anyway. Thus the simple setup is preferred.
