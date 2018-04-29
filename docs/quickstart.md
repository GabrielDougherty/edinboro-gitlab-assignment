Quickstart
==========

This is a quickstart guide to using the Edinboro Assignment Submission System

Prerequisites
-------------

You must have `git`, `python3.4`, and `pip3` installed. This guide assumes a Linux machine is used. In order to create students, you must be an administrator on the codestore instance. Talk to your system administrator for these priveleges if you are an instructor and you plan on creating users.

Installation
------------

To install the `python-gitlab` module, type:

`$ pip3 install python-gitlab`

In the directory that you would like your script to be installed, type:

`$ git clone https://github.com/GabrielDougherty/edinboro-gitlab-assignment.git`

`$ cd edinboro-gitlab-assignment`

Now, you can run any script by typing, `python3 scriptname.py`

Getting Help
------------

To see the available arguments for a command, simply type the command without arguments.

For example, typing `python3 create-class.py` lists the arguments for the `create-class` script.

Authentication
--------------

TODO

Creating a class
----------------

In GitLab, a class (i.e., CSCI408), is a GitLab Group. This is simply a collection of repositories on the server.

Our script for creating such a group assumes that the course will be identified by a course name and sections number. Hence, the instructor (you) must only provide the course name (i.e., CSCI408), and its section number (i.e., 1) to create a class.

In order to create the above class, section 1 of CSCI408, called `CSCI408-1`, type:

`​$ python3 create-class.py --course-name "CSCI408" --course-section "1"​`

In order to create the above class, and add students from a roster file, type:

`​$ python3 create-class.py --course-name "CSCI408" --course-section "1" --file-name "csci408.csv"​`

The .csv files should follow a format that matches the following:

`CSCI,408,1,SOFTWARE ENGINEERING,@00803819,Bob,Jim,5-Oct-97,jb123456@scots.edinboro.edu  
CSCI,408,1,SOFTWARE ENGINEERING,@00803819,Jackson,Bo,5-Oct-97,bj123456@scots.edinboro.edu  
CSCI,408,1,SOFTWARE ENGINEERING,@00803819,Woods,Tiger,5-Oct-97,tw123456@scots.edinboro.edu  `

If multiple classes/sections of a class are included in the classlist file, then only the students from the specified class and section number will be added from the file.
