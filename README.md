# Gitlab for Assignment Submission and Processing

This project has scripts to help courses use [UW's Gitlab](https://git.uwaterloo.ca) for
assignment submission and processing.

## How do courses use Gitlab?

Students will have a Git repo that they can use for revision control while doing their
assignment work. The setup is:

* A Gitlab group is created for a course for a specific term. For example,
  the group might be called "cs123-spring2016".
* In that group, there is a project/repo for each student. Students
  will be added as developers so that they can clone and push their
  work. By default, the master branch is protected, but this setting
  can be turned off. Adding students as developers ensures that they
  cannot change project settings like the name, which is vital for
  ensuring that you're marking the right work for the right student. 
  The script which automates the creation of repos, adding students as
  developers, and turning of master branch protection is `create-repos.py`.
* Course staff will be added to the group as owners. This lets course staff
  clone the students' repo for marking and distributing starter code. For marking,
  be sure to mark the correct revision (ie do not mark revisions made after the
  assignment deadline).
* A student's repo can be used for the entire term. Course staff can subdivide
  the repo by assignment. For example, the repo can have folders called `A1/`, 
  `A2/`, `A3/`, etc).
* Students will get an invitation email when they're added to their repo as
  a developer at the start of term. Students who have never used git.uwaterloo.ca before
  must click the link in the email.
* If students enroll late in the course, you can create repos for them using `create-repos.py`.
  Alternatively, you can create repos manually using git.uwaterloo.ca web interface.

## Caveats

* You should not trust commit dates. They can be faked intentionally (ex. the student tries to 
  pass off late work as being on time) or unintentionally (ex. the clock on the student's
  computer is wrong). However, the times associated with push events can be trusted because those times
  come from the Gitlab server when the student pushes. The scripts use push times, not commit times.
* Students **must** push their work to the master branch before the assignment due date. If students commit
  on time, but forgets to push until after the due date, their work is considered late.
* When students clone their repo with http url, they might get the error `fatal: repository 'https://git.uwaterloo.ca/...' not found`.
  Fix this by using the url `https://<questID>@git.uwaterloo.ca/...` instead (add Quest ID to url).

## Script Documentation

The scripts are written in [Python](https://www.python.org/). To run them, please have **Python
3.4 or higher** and **Git 1.8 or higher**. If you have any issues or questions about the scripts, please contact your course's
[CSCF Point of Contact](https://cs.uwaterloo.ca/cscf/teaching/contact/).

You can save the output of the scripts (or any command line program really) using [tee](https://en.wikipedia.org/wiki/Tee_%28command%29).
For example, you can run `python3 clone.py cs123-spring2016 | tee clone-ouput.txt`.

All scripts accept `-h` and `--help` arguments and will print a help message. You may have to make the scripts
executable before running them (for example, with `chmod 700`). More documentation is below.

### `clone.py`

The `clone.py` script is used to clone the students' repositories and to checkout the last
commit in the last push to master branch before a certain time.

#### Arguments:

* `group_name`: The only mandatory argument is the group name. The group name can be found from the
  Gitlab [Groups page](https://git.uwaterloo.ca/dashboard/groups). Course staff, including TAs, should
  be added to the group as owners using the web interface.
* `--url-type {http,ssh,http-save,ssh-save}`: You can choose to use either `http` or `ssh` for the repository
  URL. The default is `http`. To setup `ssh`, see the Gitlab doc on [SSH keys](https://git.uwaterloo.ca/help/ssh/README).
  If you are cloning many repositories, typing in your credentials every time is exhausting. You can make `clone.py` remember
  your credentials using the `-save` versions. For `http-save`, your credentials is saved for 15 minutes in memory with
  the command:
  
  `git config --global credential.helper cache`

  You can clear the cached credentials with: `git config --global --unset-all credential.helper`.
  For `ssh-save`, your passphrase is saved using `ssh-agent` and `ssh-add`.
* `--token-file TOKEN_FILE`: Access to Gitlab is needed to get all the projects in the group. You can
  find your private token from Gitlab [Account page](https://git.uwaterloo.ca/profile/account). By default, you'll
  be asked to type it in (won't be echo'ed back). If you don't want to keep typing in the token, save the token in
  the first line of a file by itself, then set `TOKEN_FILE` to a path to the file.
* `--clone-dir CLONE_DIR`: Will clone the students' repositories into the folder `CLONE_DIR`. The default is `./group_name/`,
  ie a folder with the same name as `group_name` in the current directory.
* `--revert-date REVERT_TO_DATE`: This option will checkout the last commit in the last push to the master branch
  before `REVERT_TO_DATE`, which can be in various formats:

   * 2016-05-30 15:10 (will use 00 seconds and current timezone on the computer running the script)
   * 2016-05-30 15:10-0400
   * 2016-05-30 15:10:30
   * 2016-05-30 15:10:30-0400

  If a timezone isn't given, the current timezone on the system will be used.
  If the `--revert-date` option isn't given, the script will just clone.
* `--students STUDENTS`: The default is to clone (and possibly revert) all the repositories in the given group. Use this option if you only want to 
  perform these actions on a select set of students. `STUDENTS` should be a comma separated list of student Quest IDs.
* `--username USERNAME`: On some systems, you need to include your Gitlab username in the url or you'll get a "repository not found" error.
  If you get that error, pass in your Gitlab username (same as your Quest ID) with this option.
  
#### Examples:

1. `python3 clone.py cs123-spring2016 --url-type http-save`

    Clones all the repositories in the group cs123-spring2016 to the folder `./cs123-spring2016`.
    You'll be asked to type in your private token and your Gitlab credentials once. The only git
    command that will be run is `git clone`. You might run this near the start of term to clone
    all the students' repos.

1. `python3 clone.py cs123-spring2016 --token-file ~/.gitlab_token --url-type http-save`

    Same as above, except that the private token will be read from the first line of ~/.gitlab_token, a
    text file you have to create manually.

1. `python3 clone.py cs123-spring2016 --url-type ssh-save --revert-date '2016-05-30 13:00:00' --students j4ansmith,yralimonl,t2yang`

    Clones the repositories for three students j4ansmith, yralimonl, and t2yang. Then checkout the last commit in the last push made 
    to the master branch before 1:00pm on May 30, 2016.

### `batch-operation.py`

Runs a command or program in every folder in a given folder.

#### Arguments:

* `parent_dir`: Mandatory. The command will be run inside each folder in `parent_dir`.
* `command`: Mandatory. The command to run inside the folders in `parent_dir`. If you need
  to pass arguments to the command, put the command and all its arguments in quotes.
* `--headers`: If specified, a header will be printed before each running of the command.
* `--pass-name`: If specified, the folder names in `parent_dir` will be passed to `command`.

#### Examples:

1. This example runs the [`pwd`](https://en.wikipedia.org/wiki/Pwd) command inside each folder in cs349-test1.

        $ ls cs349-test1/
        cscf-t01  cscf-t02  cscf-t03  cscf-t04  cscf-t05  random-project
        $ python3 batch-operation.py cs349-test1/ pwd
        /u5/yc2lee/gitlab-assignments/cs349-test1/cscf-t01
        /u5/yc2lee/gitlab-assignments/cs349-test1/cscf-t02
        /u5/yc2lee/gitlab-assignments/cs349-test1/cscf-t03
        /u5/yc2lee/gitlab-assignments/cs349-test1/cscf-t04
        /u5/yc2lee/gitlab-assignments/cs349-test1/cscf-t05
        /u5/yc2lee/gitlab-assignments/cs349-test1/random-project
        $

1. This example will pass the folder name to `echo Hello,` and print an informative header.

        $ python3 batch-operation.py --headers --pass-name cs349-test1 'echo Hello,'
        >>> Running command in /u5/yc2lee/gitlab-assignments/cs349-test1/cscf-t01/cscf-t01
        Hello, cscf-t01
        
        >>> Running command in /u5/yc2lee/gitlab-assignments/cs349-test1/cscf-t02/cscf-t02
        Hello, cscf-t02
        
        >>> Running command in /u5/yc2lee/gitlab-assignments/cs349-test1/cscf-t03/cscf-t03
        Hello, cscf-t03
        
        >>> Running command in /u5/yc2lee/gitlab-assignments/cs349-test1/cscf-t04/cscf-t04
        Hello, cscf-t04
        
        >>> Running command in /u5/yc2lee/gitlab-assignments/cs349-test1/cscf-t05/cscf-t05
        Hello, cscf-t05
        
        >>> Running command in /u5/yc2lee/gitlab-assignments/cs349-test1/random-project/random-project
        Hello, random-project
        $

1. After you clone all the students' repositories with `clone.py`, you can run custom commands on all
   the repos with `batch-operation.py`. There are four fatal errors because those repositories are empty
   and have no commits to show.

        $ python3 batch-operation.py --headers cs349-test1/ 'git log -1 --oneline'
        >>> Running command in /u5/yc2lee/gitlab-assignments/cs349-test1/cscf-t01/cscf-t01
        adb4691 nick testing push
        
        >>> Running command in /u5/yc2lee/gitlab-assignments/cs349-test1/cscf-t02/cscf-t02
        fatal: bad default revision 'HEAD'
        
        >>> Running command in /u5/yc2lee/gitlab-assignments/cs349-test1/cscf-t03/cscf-t03
        fatal: bad default revision 'HEAD'
        
        >>> Running command in /u5/yc2lee/gitlab-assignments/cs349-test1/cscf-t04/cscf-t04
        fatal: bad default revision 'HEAD'
        
        >>> Running command in /u5/yc2lee/gitlab-assignments/cs349-test1/cscf-t05/cscf-t05
        fatal: bad default revision 'HEAD'
        
        >>> Running command in /u5/yc2lee/gitlab-assignments/cs349-test1/random-project/random-project
        3fd99a6 another test
        $
