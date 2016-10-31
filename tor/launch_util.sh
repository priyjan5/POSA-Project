#!/bin/bash
useradd tor
passwd tor
usermod -aG sudo tor
