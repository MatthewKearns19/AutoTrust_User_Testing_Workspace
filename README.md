# Auto-Trust, an automated visual testing framework.
Auto-Trust is a final year college software project, an automated visual testing
framework that emphasizes the importance of visual testing during the Software
Development Lifecycle. It is also provided as a base framework that users can
integrate into their own testing workflows, from experienced testers that may
want to extract the visual assessment functionality only, to beginners who may
want to learn from a structured example of automated testing within a Behaviour-
Driven Development workflow.

This repository is an example of a "user's testing workspace" that holds the
automated tests.

The tests are executed on an example of a "user's workspace", an application
User Interface.

The domain of this example "user's workspace" holds more information so please
check it before continuing -
https://auto-trust-user-workspace-example-environment.netlify.app/

## Pre-requisites

Before executing the tests, ensure you have met the following requirements:
* More info on Behave -
  https://behave.readthedocs.io/en/stable/tutorial.html#features
* More info on Selenium with behave -
  https://www.blazemeter.com/blog/using-the-behave-framework-for-selenium-bdd-testing-a-tutorial
* Get the code from this repository to your local machine.
* A GPU is not needed but improves accuracy for the
* A virtual environment is recommended, if you have not installed `<Python>` or
  Python's `<virtualenv>` then:

  Windows:
  Download Python at and follow instructions to set
  your python path: https://www.python.org/downloads/
  ```
  python -m pip install --upgrade pip

  pip install virtualenv
  ```

  Linux:
  ```
  sudo apt-get update

  sudo apt-get install python3.6

  python -m pip install --upgrade pip

  pip install virtualenv
  ```

* Now set up your virtual environment
  if using the PyCharm IDE you can do this manually from within the editor if
  you prefer, see docs here https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html#python_create_virtual_env).
  Otherwise run the following commands:

  Windows:
  ```
  python -m virtualenv venv

  source venv\Scripts\activate
  ```

  Linux:
  ```
  python -m virtualenv venv

  source venv/bin/activate
  ```

## To use Auto-Trust, follow these steps:

* Install the dependencies from the requirements.txt file
  ```
  # run:
  pip install -r requirements.txt
  ```

* For local testing install `<chromedriver>` to your local machine.
  Windows:
  find versions here https://sites.google.com/a/chromium.org/chromedriver/downloads
  (if you do not already have `<Chrome>` which `<chromedriver>` replies upon,
    you can download it here: https://www.google.com/chrome/). Change the
    default `<chrome_executable_path = '/usr/bin/chromedriver'>` path in the
    Auto-Trust codebase `<variables.py>` file to your local Windows
    `<chromedriver>` installation path, for example
    `<chrome_executable_path = 'C:/webdrivers/chromedriver.exe'>`.

  Linux:
  ```
  # Prerequisites
  sudo apt-get update
  sudo apt-get install -y unzip xvfb libxi6 libgconf-2-4

  # install Chrome if you do not have it already
  sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
  sudo echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
  sudo apt-get -y update
  sudo apt-get -y install google-chrome-stable

  # install chromedriver
  wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
  unzip chromedriver_linux64.zip

  # move and configure chromedriver to /usr/bin/
  sudo mv chromedriver /usr/bin/chromedriver
  sudo chown root:root /usr/bin/chromedriver
  sudo chmod +x /usr/bin/chromedriver
  ```

* Inside the `<features>` directory your will see a feature file
  `<Home_Page.feature>` which holds the test scenarios. If you have read the
  example of a "user's workspace" repository hosted link that was provided,
  along with the Behave, and Selenium docs provided, you will be able to make
  perfect sense of the file structure with this `<features>` directory. Within
  the `<Home_Page.feature>` click on the small arrow beside a Scenario to run
  the Scenario, or at the Project root run the behave command:
  ```
  behave
  ```

## Further integrations
* For a fully automated CI/CD workflow with a local `<Jenkins>` Continuous
  Integration server, download Jenkins (I recommend downloading on a Linux
  system, and if you are on windows you could set this up by running an
  `<Ubuntu>` image on a virtual machine such as `<VirtualBox>`,
  see: https://itsfoss.com/install-linux-in-virtualbox/).

  On Jenkins setup, when prompted with installations, accept these. Then go to
  Manage Jenkins > Install Plugins and install the `<GitHub Plugin>`. Read this
  guide to get a better understanding of setting up a Jenkins
  `<Freestyle Project>`-
  https://www.techrepublic.com/article/how-to-create-a-new-build-job-in-jenkins/

  You can take the approach of setting one `<Freestyle Project>` up for your
  application workspace repository, and another for your testing repository. Set
  the `<Freestyle Project>` for your testing repository to track our application
  workspace in the `<Build Triggers Step>`.

  Within the `<Build Step>` of your `<Freestyle Project>` testing repository,
  you can configure Jenkins to execute the tests that have been pulled from this
  testing repository on GitHub. Add these few commands to the `<Build Step>`:

  Windows (make sure the `<Build Step>` is `<Execute Windows batch command>`):
  ```
  set -e
  python3 -m virtualenv env
  source env\Scripts\activate
  pip 3 install --upgrade pip
  pip3 install wheel
  pip3 install -r requirements.txt
  behave
  ```

  Linux (make sure the `<Build Step>` is `<Execute Shell>`):
  ```
  #!/bin/bash
    set -e
  python3 -m virtualenv env
  source env\Scripts\activate
  pip 3 install --upgrade pip
  pip3 install wheel
  pip3 install -r requirements.txt
  behave
  ```

  Jenkins will be automatically configured to run on localhost port 8080. More
  suitable integrations of Jenkins would be on a Cloud Service Provider such as
  Azure or AWS.

  Make sure you have specified the correct `<chromedriver>` path in the
  `<variables.py>` to match where you have specified chromedriver as a Jenkins
  environment variable. For example on local Jenkins, you can define the path to
  your local chromedriver installation as a Jenkins environment variable.
  Of course Windows chromedriver path will be different to Linux as mentioned
  previously. Additionally, you do not have to use chromdriver, you can research
  yourself other web drivers to execute test on, `<Selenium>` offers many.


* For a more modern Continuous Integration server, you could configure your
repository with CircleCI which is a seamless operation, login with GitHub and
you will be guided on this configuration completely, visit here:
https://circleci.com/vcs-authorize/ . You can find a `<config.yml>` in the
`<.circleci>` directory which sets up the necessary dependencies needed to
execute this on CircleCi in the correct order, such as a Docker Image of browser
 tools `<circleci/browser-tools@1.1.3>` for `<chromedriver>` (which is then
    downloaded to the same `<chromedriver>` path specified in the default
    Auto-Trust `<variables.py>` file).

## Issues to be future developed
* Currently, the exact pixel comparison of a browser captured screenshot vs. a predefined screenshot is susceptible to unreadable failed
  results when a large element is removed which caused a large page shift. Many areas are shifted so these are flagged as an error too,
  hence the failed result is unreadable in terms of pinpointing the root cause within many areas highlighted as failed. Future development of
  differentiating when to highlight errors needs to be developed with more intelligent methods around dropout rates.
