password="<password>"

# Create user
useradd deploy
mkdir /home/deploy
mkdir /home/deploy/.ssh
chmod 700 /home/deploy/.ssh

usermod -s /bin/bash deploy # Set default terminal for user

# Set user deploy password
echo "deploy:$password" | chpasswd
usermod -aG sudo deploy # add to sudo group

# Copies ssh keys added during creation
cp /home/admin/.ssh/authorized_keys /home/deploy/.ssh/
chown deploy:deploy /home/deploy -R 
chmod 400 /home/deploy/.ssh/authorized_keys

# Edit ssh config
sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
echo "AllowUsers deploy" >> /etc/ssh/sshd_config
service ssh restart

# Set no need for sudo password, comment this out if you want more security. It might make some of the later scripts behave weird or stop working.
echo "deploy ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
