## Requirements

1. First of all you should make a concept of the demo you want to add. Create diagrams to visualize the components and see the dependencies. If possible, everything should run within docker. For native actions (like opening applications) you can use the NativeApp controller of your demo.  
1. To add a new demo to the ecosystem you need to have a fully set up workstation as described in the [Setup of a Workstation guide](setup/client_setup.md)
1. All code that is used by the NativeApp needs to be Python 3.9 compatible! We use setuptools to build our application which requires python >3.9.

## Procedure

### 1. Adding to the demonstrations environment (NativeApp + Docker)

1. Clone the demonstrations repository
1. Run the demo creation script `init_new_demo.sh` which is in the root directory. The script will ask you for a name of the demonstration and based on that generate multiple files and directories that are necessary for the CI, NativeApp and the demonstration itself. Look into the script for further information or documentation when you want to do it manually.
1. After the script created all files you can start the development of your demonstration by navigating to the demo folder in `demos/<demo_name>`. It is named after the demo name you entered in the script. The created directory holds your `Dockerfile` and all belonging files such as scripts. From there you use the empty `Dockerfile` to create the container. _Suggestion:_ Use an **Alpine** image. It's small, lightweight and extensible.
1. After you successfully created and tested your Docker container. You need to make adjustments to your `docker-compose.yml`.
1. In case you have to interact with the native host you can describe your procedures in the NativeApp files. Have a look on the existing demos for small guidance.
1. Now you can install and run the NativeApp as described in [NativeApp (Section Developing/Testing Locally)](/Demonstrations/Native-App#developingtesting-locally). The NativeApp will run and wait for commands of the plattform.

### 2. Add demo to demo portal (Web platform)

If followed all previous steps you added the demo to the _demonstrations_ ecosystem. Now, in order to let the demos appear in the _portal_ so you can start them from there you have to follow the next steps.

1. Clone the `demonstrations` repository
1. Run the tool for managing demos (`python manage_demos.py`). There you can create, list, update and delete demos. When using the create feature it adds your demo to the portal and creates the localization snippets for the web app which you have to edit manually afterwards.
1. When creating a demo you will be asked for the following:

* Demo ID (this should be the same as in the other demo creation tool)
* Category
* Level
* Estimated Time duration in minutes

These contents will be created by the tool and are language unspecific.

1. Furthermore, every demo has a title, short description and demo guide. These are language specific and always need to be created manually for english and german.

The demo guide should contain basic guidance steps for the demo (open browser, do this, do that, etc.). These steps are definded in the `messages` part of every demo in `demos/demos.json`.
It makes sense to split the multiple stages during a demo (before, during, after) to different tabs. Have look into existing demos for more detailed examples.

**Note:** For the content part of the demo guide html is also supported. You can use this [HTML editor](https://onlinehtmleditor.dev/) if you don't want to code and test it by yourself. If finished, just go to **Edit HTML source code** and copy the html content. But keep in mind that you have to escape special characters before putting it into the json file! For escaping, you can also use tools [like this website](https://www.freeformatter.com/json-escape.html) for it and just paste the escaped html string.

Example:

    ```json
    (...)
    "messages": {
      "en": {
        "title": "Phishing",
         "description": "This demo shows (...)",
                "guide": [
                    {
                        "title": "Open Mail Program",
                        "content": "<h1>Tasks<\/h1>\r\n\r\n<ul>\r\n\t<li>Please ...<\/li>\r\n<\/ul>"
                    },
    (...)
    ```

1. That's it. Now re-build the native app and check if the portal on the platform successfully receives and parses your demo. You don't need to update anything on the teaching platform side to see your changes.
1. The demo should appear under the _Portal_ page now and be controllable. If you want to run the platform locally following the [guide for setting up a dockerized platform environment](Platform/Setup-Dev-Environment-for-Teaching-Platform#dockerized-dev-environment).

### 3. Add teaching material

[Look into the LMS documentation for steps to add teaching content to the platform](Platform/Concept#editing-teaching-content-via-the-learning-management-system-lms)

## Further Information

### Dependencies for NativeApp

If your demo has specific dependencies for the native app part, not the part which is in the docker container of your demo, you need to add it to the `install_requires` of the `setup.cfg` file.

### Hosts Entries

If your demo needs entries in the hosts file (for custom DNS) use the admin component to set them during runtime.

