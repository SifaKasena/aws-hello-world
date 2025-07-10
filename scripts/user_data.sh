#!/bin/sh
# Update and install dependencies
sudo yum update -y
sudo yum install -y python3 python3-pip nginx git

# Change working directcory
cd /home/ec2-user

# Clone repo
git clone https://github.com/SifaKasena/aws-hello-world.git
chown -R ec2-user:ec2-user aws-hello-world

# Setup virtual environment
cd aws-hello-world
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements
deactivate

# Daemonize gunicorn
sudo cp scripts/flask-api.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start flask-api
sudo systemctl enable flask-api

# Clean up
rm -rf !(flask_api)
