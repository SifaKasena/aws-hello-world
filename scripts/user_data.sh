#!/bin/sh
# Update and install dependencies
sudo yum update -y
sudo yum install -y python3-pip git

# Change working directcory
cd /home/ec2-user

# Clone repo
git clone https://github.com/SifaKasena/aws-hello-world.git
chown -R ec2-user:ec2-user aws-hello-world

# Setup virtual environment
cd aws-hello-world
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements
deactivate

# Daemonize gunicorn
sudo cp scripts/flask-api.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start flask-api
sudo systemctl enable flask-api

# Clean up
# TODO: Find better way to clean up
rm -rf .git* scripts README.md requirements
