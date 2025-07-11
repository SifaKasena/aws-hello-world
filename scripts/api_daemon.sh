#!/bin/sh
# Daemonize the Flask API using systemd
cd /home/ec2-user/aws-hello-world
sudo cp scripts/flask-api.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start flask-api
sudo systemctl enable flask-api

# Clean up
# TODO: Find better way to clean up
rm -rf .git* scripts README.md requirements
