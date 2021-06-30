# nyu-travis-ci

[![Build Status](https://travis-ci.com/lcqsigi/lab-travis-ci.svg?branch=master)](https://travis-ci.com/lcqsigi/lab-travis-ci)
[![Codecov](https://img.shields.io/codecov/c/github/nyu-devops/lab-travis-ci.svg)]()
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
    
This is for NYU DevOps lab on using Travis CI with Redis for Continuous Integration

## Introduction

This lab contains a `.travis.yml` file that shows you how to run your tests and request that a Redis service be attached while running them. It also uses Code Coverage to determine how complete your testng is.

## Setup

To complete this lab you will need to Fork this repo because you need to make a change in order to trigger Travis CI. When making a Pull Request, you want to make sure that your request is merging with your Fork because the Pull Request of a Fork will default to come back to this repo and not your Fork.

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
    $ coverage report -m

Nose is configured to automatically include the flags `--rednose --with-spec --spec-color --with-coverage` so that red-green-refactor is meaningful. If you are in a command shell that supports colors, passing tests will be green while failing tests will be red.

## What's featured in the project?

    * routes.py -- the main Service using Python Flask and Redis
    * test_service.py -- test cases using unittest
    * models.py -- the Pet model that wrappers the Redis database
    * test_pets.py -- unit tests that only test the Pet model
    * .travis.yml -- the Travis CI file that automates testing

This repository is part of the NYU class CSCI-GA.2810-001: DevOps and Agile Methodologies taught by John Rofrano, Adjunct Instructor, NYU Courant Institute of Mathematical Sciences, Graduate Division, Computer Science.
