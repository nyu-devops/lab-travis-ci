# nyu-travis-ci

[![Build Status](https://travis-ci.org/quintoben/lab-travis-ci.svg?branch=master)](https://travis-ci.org/quintoben/lab-travis-ci)
[![codecov](https://codecov.io/gh/quintoben/lab-travis-ci/branch/master/graph/badge.svg)](https://codecov.io/gh/quintoben/lab-travis-ci)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
    
This is for NYU DevOps lab on using Travis CI with Redis for Continuous Integration

## Introduction

This lab contains a `.travis.yml` file that shows you how to run your tests and request that a Redis service be attached while running them. It also uses Code Coverage to determine how complete your testng is.

## Setup

To complete this lab you will need a mirror of this repo. You cannot just clone the repo because you need to make a change in order to trigger Travis CI. You also don't want to Fork it because you want to test Pull Requests and the Pull Request of the Fork will come back to this repo and not your Fork. Therefore you need to copy the repo to your own GitHub account using an opperation know as `mirroring`

### Mirroring the repository

Here are the steps to make a mirror of this repo to your GutHub account:

- Create a new repository in your own GitHub account called: `nyu-lab-travis-ci`
- Open Terminal on Mac, Command Prompt on Windows
- Create a bare clone of the repository
    ```
    git clone --bare https://github.com/nyu-devops/lab-travis-ci.git
    ```
- Push and Mirror the clone to the new repository `nyu-lab-travis-ci` on your GitHub
    ```
    cd old-repository.git
    git push --mirror https://github.com/<your_account>/nyu-lab-travis-ci.git
    ```
- Remove the temporary local repository you just created
    ```
    cd ..
    rm -rf lab-travis-ci.git
    ```

You should now have a mirror of this repository called `nyu-lab-travis-ci` under your own GitHub account that you can make changes to and create Pull Requests and see how Travis CI runs your tests for you with every Pull Request or `push` to master.

## If you want to run the tests locally

There is no need to run the tests locally because the purpose of this lab is to have Travis Ci run them for you but if you wanted to run them yourself, the easy setup is to have [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/) installed. Then all you have to do is clone this repo and invoke vagrant:

    git clone https://github.com/nyu-devops/lab-travis-ci.git
    cd lab-travis-ci
    vagrant up
    vagrant ssh
    cd /vagrant

This should give you a good indication that the unit tests are passing that that you have good code coverage.

You can now run `nosetests` to run the TDD tests locally.

## Manually running the Tests

Run the tests using `nosetests` and `coverage`

    $ nosetests
    $ coverage report -m --include=server.py

Nose is configured to automatically include the flags `--rednose --with-spec --spec-color --with-coverage` so that red-green-refactor is meaningful. If you are in a command shell that supports colors, passing tests will be green while failing tests will be red.

## What's featured in the project?

    * server.py -- the main Service using Python Flask and Redis
    * test_server.py -- test cases using unittest
    * models.py -- the Pet model that wrappers the Redis database
    * test_pets.py -- unit tests that only test the Pet model
    * .travis.yml -- the Travis CI file that automates testing

This repo is part of the CSCI-GA.3033-013 DevOps course taught by John Rofrano at NYU Courant Institute of Mathematical Sciences, New York
