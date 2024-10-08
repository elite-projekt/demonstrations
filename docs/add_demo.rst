
Add a demo
==========

Requirements
------------


#. First of all you should make a concept of the demo you want to add. Create diagrams to visualize the components and see the dependencies. If possible, everything should run within Docker. For native actions (like opening applications) you can use the NativeApp controller of your demo.
#. To add a new demo to the ecosystem you need to have a fully set up workstation as described in the `Setup of a Workstation guide <setup/client_setup.html>`_
#. All code that is used by the NativeApp needs to be Python 3.9 compatible! We use setuptools to build our application which requires python >3.9.

Procedure
---------

1. Adding to the demonstrations environment (NativeApp + Docker)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


#. Clone the demonstrations repository
#. Create a new folder with your demo ID in ``demos``
#. Create your demo in ``demos/<your demo ID>/native/<your demo ID>_controller.py``. This has to contain a class which inherits from :class:`~native.nativeapp.controller.demo_controller.DemoController` and a function ``get_controller`` which returns an instance of your controller.
#. Populate your ``<demo ID>/demo.json`` (see below)
#. If you use any text please use :class:`~native.nativeapp.utils.locale.locale.Locale` and save your ``po`` files in ``<demo ID>/locales/<locale>/LC_MESSAGES/base.po``.
#. After you successfully created and tested your Docker container. You need to make adjustments to your ``docker-compose.yml``.
#. In case you have to interact with the native host you can describe your procedures in the NativeApp files. Have a look on the existing demos for small guidance.
#. Now you can install and run the NativeApp as described in `NativeApp (Section Developing/Testing Locally) <nativeapp.html#debugging-and-testing-locally>`_. The NativeApp will run and wait for commands of the plattform.

demo.json file
~~~~~~~~~~~~~~

This file provides additional information about your demo and is picked up by the CI to build your containers.

.. code-block:: json

   {
     "categories": [
       "phishing",
       "email",
       "badusb"
     ],
     "hardware": [
       "usb-stick",
       "wifi-stick",
       "smartphone"
     ],
     "level": "beginner | intermediate | expert",
     "time": <time in minutes>,
     "isAvailable": true | false,
     "container":
     [
       {
         "name": "<name of your container>",
         "dockerfile": "<relative path of your dockerfile>"
       },
       {
         "name": "<name of your second container>",
         "dockerfile": "<relative path of your dockerfile>"
       }
     ]
   }

Further Information
-------------------

Dependencies for NativeApp
^^^^^^^^^^^^^^^^^^^^^^^^^^

If your demo has specific dependencies for the native app part, not the part which is in the docker container of your demo, you need to add it to the ``install_requires`` of the ``setup.cfg`` file.

Hosts Entries
^^^^^^^^^^^^^

If your demo needs entries in the hosts file (for custom DNS) use the admin component to set them during runtime.
