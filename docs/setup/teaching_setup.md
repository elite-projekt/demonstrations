# Teaching platform setup

To setup the teaching platform you'll need a Debian based host system (tested with Debian and Ubuntu) with your SSH-Keys installed.
Additionally you'll need `ansible` on your local machine.

First you clone the ansible repo

```
git clone git@code.fbi.h-da.de:elite-projekt/ansible-teaching.git
```

Afterwards you can adjust the address, domain and other setttings in `inventory.cfg`.
Then change the `host` variable in `h_da.yml` to point to the server you want to configure.

Now just run the ansible playbook
```
ansible-playbook h_da.yml -i inventory.cfg
```

Afterwards head to `https://<your url>/wp-admin` and login. Head to `Tools -> Better Search Replace`, search for `dev.elite.fbi.h-da.de`, and replace it with your url.

Now the platform should be running.
