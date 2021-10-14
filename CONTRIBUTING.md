# Contributing to SigPro

Here you will find a series of steps that describe how to contribute a new implementation, fix or
update to `SigPro` library.

## 1. Clone the repository

The first step would be to clone the `SigPro` repository. In order to do so
make sure that you have access to the repository by accessing it direcly
[https://github.com/sintel-dev/SigPro/](
https://github.com/sintel-dev/SigPro/).

If you have access to the repository and you have your `ssh` keys configured
in your github account, you can clone it by using the following command

```bash
git clone git@github.com:sintel-dev/SigPro.git
```

If you don't have your `ssh` keys configured you can clone the repository
using your login name and password running the following command:

```bash
git clone https://github.com/sintel-dev/SigPro
```

Next, you can enter your repository folder, create a virtualenv and install
the project and the development dependencies.
**Note**: You need to have virtualenv and virtualenvwrapper installed for
these steps to work

```bash
cd SigPro
mkvirtualenv sigpro
make install-develop
```

## 2. Prepare your branch

Before going any further, create the new `git` branch to which you will
be pushing your development.

To do so, type the following command with the desired name for your branch:

```bash
git checkout -b <name_of_your_branch>
```

Try to use the naming scheme of prefixing your branch with issue-X where X is
the associated issue, such as issue-3-fix-foo-bug. And if you are not
developing  on your own fork, further prefix the branch with your GitHub
username, like githubusername/issue-3-fix-foo-bug.

## 3. Code your changes

Once you have your branch ready and set, you can start coding your changes.

When doing so, ensure that the code is placed in its corresponding python
file, and if you think that this doesn't exist, create it in the location
that you find more suitable. However, when it comes to `aggregations` and
`tranformations`, those are bound to their type and subtype.

Also, while hacking your changes, make sure to follow the [PEP8](
https://www.python.org/dev/peps/pep-0008/) style guide for python code
and our `setup.cfg` (the main change is that we allow 99 characters per
line).


## 4. Test your changes

Now that you have implemented your changes, make sure to  cover all your
developments with the required unit tests, and that none of the old tests
fail as consequence of your changes. For this, make sure to run the tests
suite and check the code coverage by using the following commands:

```bash
$ make lint      # Check code styling
$ make test      # Run the tests
$ make coverage  # Get the coverage report
```

Once you have finished coding your changes, make sure to run the following
command to ensure that your changes pass all the styling checks and tests
including other Python supported versions using:

```bash
$ make test-all
```

## 5. Create a pull request

Once you have created and tested your primitive, you can create a pull
request by doing the following steps:

0. (You did this previoulsy, but make sure) Create a new branch or ensure you are in the correct branch. Run the command `git branch` to see at which branch you are pointing. If you are in the desired follow the next step.
1. Add the new files and the updated ones. By running `git status` you will see the modified and `new/untracked` files. Use `git add` to `add` the files that involve your implementation, such as the new primitive `json` file, the new module with the new transformation or aggregation and other changes that you may have done to existing files (such as `setup.py` if you updated or introduce a new dependency).
2. Commit your changes using `git commit -m "Implement my new transformation"`.
3. Push your branch: `git push --set-upstream origin <name_of_your_branch>`.
4. Go to [https://github.com/sintel-dev/SigPro/](https://github.com/sintel-dev/SigPro/) and create a pull request from this branch to the master branch.
