#!/bin/sh
# Move folder to remote hosts
cd /home/ec2-user/
for host in "$@"; do
  scp -r aws-hello-world ec2-user@$host:/home/ec2-user/
done

# Clean up
rm -rf aws-hello-world
