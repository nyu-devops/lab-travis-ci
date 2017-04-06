# nyu-travis-ci

[![Build Status](https://travis-ci.org/rofrano/nyu-lab-travis-ci.svg?branch=master)](https://travis-ci.org/rofrano/nyu-lab-travis-ci)
[![Codecov](https://img.shields.io/codecov/c/github/nyu-devops/lab-travis-ci.svg)]()

This is for NYU DevOps lab on using Travis CI with Redis for Continuous Integration

## Introduction

This lab contains a `.travis.yml` file that shows you how to run your tests and request that a Redis service be attached while running them. It also uses Code Coverage to determine how complete your testng is.

## Setup

For easy setup, you need to have Vagrant and VirtualBox installed. Then all you have to do is clone this repo and invoke vagrant:

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
