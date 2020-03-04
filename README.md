# Release_Note_Automation
Script/program to automate our release note process

The script is called "notomaton." It is written in Python.

Notomaton is pretty much freestanding now. You can access the hosted instance at:

https://release-notes.scality.com/dashboard

This is how you should interact with the tool. 

If you have to make a change, simply commit and push to this repo on the master branch. Notomaton 
picks up the change and restarts itself using your revisions. 

Warning: THERE IS NO REVIEW PROCESS IN PLACE. WHEN YOU PUSH TO MASTER, IT GOES INTO EFFECT.
If you're not 100% sure of what you're doing, start a branch, push it, and ask me or Taylor for a
review. 

Writers should feel most welcome in docs/assets/. Output is ordered in the yaml files in the
product folders (ring/, zenko/, and hyperdrive when we figure out what to name it). These control
which html files are assembled into a web page when notomaton does its thing. The common/ 
directory contains the ntml chunks from which the final release note is built, along with style.css

If you need to add something at the last minute, modify the html in common/. If that's too scary,
run the tool and hand-edit the output HTML and PDF.
