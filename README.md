# Auto-Trust, an automated visual testing framework.
Auto-Trust is a final year college software project, an automated visual testing framework that emphasizes the importance
of visual testing during the Software Development Lifecycle. Also provided as a base framework that users can integrate
into their own testing workflows, from experienced testers that may want to extract the visual assessment functionality
only, to beginners who may want to learn from a structured example of automated testing within a Behaviour-Driven Development
workflow.

This repository is an example of a "user's testing workspace" that holds the automated tests.

The tests are executed on an example of a "user's workspace", an application User Interface.
The domain of this example "user's workspace" holds more information so please check
it before continuing - https://auto-trust-user-workspace-example-environment.netlify.app/

To find more info on Behave - https://behave.readthedocs.io/en/stable/tutorial.html#features
To find more info on Selenium with behave - https://www.blazemeter.com/blog/using-the-behave-framework-for-selenium-bdd-testing-a-tutorial

### Pre-requisites
Before executing the tests, ensure you have met the following requirements:

* installation steps will be given in Linux commands, so make sure you have access to a Linux distribution terminal.
On Windows, examples to download are Git-Bash and WSL.
* You have installed Python, and the requirements from requirements.txt
```
run:
pip install -r requirements.txt
```
* You have a basic understanding of graph theory.



For a more modern Continuous Integration server, you can find a config.yml in the .circleci directory which sets up the necessary
dependencies in the correct order, such as a docker image of browser tools for chromedriver, which is downloaded to the same
chromedriver path specified in the Auto-Trust variables file.
