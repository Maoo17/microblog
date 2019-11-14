#! /bin/bash
source ./venv/bin/activate
eval "$(ssh-agent -s)" ssh-add ~/.ssh/aws.pem
export ANSIBLE_VAULT_PASSWORD_FILE=~/.vault_pass.txt
