# Release_Note_Automation
Script/program to automate our release note process

The script is called "notomaton." It is written in Python.


To make the script work, you'll need: 

* An Atlassian API token.

  https://confluence.atlassian.com/cloud/api-tokens-938839638.html

* A python3 virtual environment. This repo contains the tools you need to 
  do this.

1. Create the virtual environment (Contains all dependencies for development).

   `python3 -m venv .venv`

2. Activate the environment.

   `source .venv/bin/activate`

3. Install dependencies.

   `pip install -r requirements.txt`

4. Install the project.

   `python3 setup.py develop`

5. If you get a yaml error, do:

   `pip install pyyaml`

When setup is complete, query the Jira database with: 

   `notomaton -u <USER> -t <TOKEN> --project <PROJECT> --version <VERSION#>`

Which produces search results in tabular format to stdout. 

For example: 
   `notomaton --user william.abernathy@scality.com --token <1234big-ass-hash56789> --project RING \--version 7.4.3 > ~/Desktop/RING_7.4.3.html`

(You can change the project to S3C or the version number to whatever. 
Zenko has a peculiar numbering scheme: "ZENKO PSI 1.1", for example.)
