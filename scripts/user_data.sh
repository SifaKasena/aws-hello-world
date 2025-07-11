#!/bin/sh
# Update and install dependencies
sudo yum update -y
sudo yum install -y python3-pip git

# Change working directcory
cd /home/ec2-user

# Clone repo
git clone https://github.com/SifaKasena/aws-hello-world.git

# Setup virtual environment
cd aws-hello-world
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements
deactivate

# Change ownership of the project directory
chown -R ec2-user:ec2-user .
