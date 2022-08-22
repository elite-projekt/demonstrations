## Presenting the VM for end users

The application `virt-viewer` provides a "kiosk"-mode which can be used to run a VM without the possibility of exiting.!

```bash
virt-viewer -k --kiosk-quit=never
```

WARNING: By using this command you are not (easily) able to leave the VM. To do that you'll need access to a terminal on the host. This can be done by connecting via SSH or pressing "CTRL+ALT+F2" and logging in. Then run `killall virt-viewer`. Switch back to the GUI by pressing "CTRL+ALT+F7".

TODO: As we can see one could exit the VM by switching to a different tty. This can easily be disabled. But we need to see what else might need to be done.

### USB devices

As long as the viewer is in the foreground, all newly attached USB devices are automatically forwarded to the VM.

## Creating and restoring VM snapshots

A snapshot of a VM can be created with the following command

```bash
virsh snapshot-create-as --domain <VM name> --name <snapshot name>
```

This snapshot contains the current disk and memory state.

To restore a snapshot run the following command

```bash
virsh snapshot-revert --domain <VM name> --snapshotname <snapshot name>
```

A few seconds later the VM is ready to use again. If used on an offline VM, the VM boots in the specified snapshot.

This allows us to recover from any software related issue in a matter of seconds.
