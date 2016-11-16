# nyu-travis-ci

[![Build Status](https://travis-ci.org/rofrano/nyu-lab-travis-ci.svg?branch=master)](https://travis-ci.org/rofrano/nyu-lab-travis-ci)
[![Codecov](https://img.shields.io/codecov/c/github/rofrano/nyu-lab-travis-ci.svg)]()

NYU DevOps lab on using Travis CI with Redis for Continuous Integration

## Introduction

This lab contains a `.travis.yml` file that shows you how to run your tests and request that a Redis service be attached while running them. It also uses Code Coverage to determine how complete your testng is.

## Setup

For easy setup, you need to have Vagrant and VirtualBox installed. Then all you have to do is clone this repo and invoke vagrant:

    git clone git@github.com:rofrano/nyu-lab-travis-ci.git
    cd nyu-lab-travis-ci
    vagrant up && vagrant ssh
    cd /vagrant

This should give you a good indication that the unit tests are passing that that you have good code coverage.

You can now run `nosetests` to run the TDD tests locally.

## Manually running the Tests

Run the tests using `nosetests` and `coverage`

    $ nosetests --with-coverage --cover-package=server
    $ coverage report -m --include= server.py

Nose is configured to automatically include the flags `--with-spec --spec-color` so that red-green-refactor is meaningful. If you are in a command shell that supports colors, passing tests will be green while failing tests will be red.

## What's featured in the project?

    * server.py -- the main Service using Python Flask and Redis
    * test_server.py -- test cases using unittest
    * .travis.yml -- the Travis CI file that automates testing

This repo is part of the CSCI-GA.3033-014 DevOps course at NYU in NYC
