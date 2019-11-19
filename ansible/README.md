
### Documentation

Ansible has surprisingly good [documentation](https://docs.ansible.com/ansible/latest/), use it find new modules and how to use a module.

They also have a [best practice](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html) that is good to read.



### How to run playbooks

First open `provision.yml` and replace `<subnet-id>` with a subnet-id from AWS.

Use the command `ansible-playbook` to run playbooks.

To create servers use `ansible-playbook provision.yml`. PS open file and replace `<subnet-id>` with a subnet id from AWS.

To destroy servers use `ansible-playbook terminate_ec2.yml`.



### Structure

#### Playbooks

We have 4 playbooks provision, terminate, gather_aws_instances, site.

**provision** is used to create 3 servers on AWS. Uses the roles provision and security_groups. It also creates an elastic ip, connects it to the load balancer and to an domain name. 

**gather_aws_instances** finds servers with the project name `devops` on AWS and adds them to hosts. After we have run this playbook we can use the following hosts in other playbooks: 
- `devops` all three servers
- `appServer` only the server for the app
- `database` only for the database server
- `loadBalancer` only the load balancer server

**terminate_ec2** destroys all servers we have on AWS with the project name `devops` and destroys the elastic ip connected to the load balancer.

**site** should run all other playbooks to setup the whole project from scratch to a running production.



#### Other

**group_vars** contains variable files connected to hosts.

**roles** contains roles used by the playbooks.

**ansible.cfg** configuration for Ansible

**hosts** contains host groups. We only have the host `local` because our servers are dynamic and we used the playbook `gather_aws_instances` instead.

**insert_aws_keys_in_config.sh** reads AWS credentials from clipboard and exports as env variables. To use, source the file `. insert_aws_keys_in_config.sh`.



### Credentials

#### ssh-keys
Without ssh-key files we need to enter the password for out ssh-key every time we run a task. To avoid this make sure you have added your ssh-key to the ssh-agent. Do follwing commands or run `make add-ssh` in root folder (you need to replace <path-to-ssh-key> in `Makefile` to use this command).

```
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/aws
```

#### AWS

You need credentials from AWS to allow Ansible to manage servers. 
Use the `. insert_aws_keys_in_config.sh` script to export aws credentials as env variables.

#### Ansible vault

AVOID using Ansible-vault as we haven't found a way to use it on CircleCI! However if you want to use it, here you can read how.

We can use ansible-vault to encrypt files that contain sensitive information. Things we want to push to GitHub but not want them visible.

Create a file with the following content, put it outside of the repo folder. Replace `<password>` with a password.

```
#!/bin/bash
cat <<EOF
<password>
EOF
```

Create a new ENV variable with the path to the password file, `ANSIBLE_VAULT_PASSWORD_FILE=<path-to-file>`.

Can now use `ansible-vault decrypt` and `ansible-vault encrypt` without typing password.

### Configuring Ansible

We use `ansible.cfg` to configure Ansible.

Example of relevant settings:

```
[defaults]
host_key_checking           = False
ansible_python_interpreter  = python3
inventory                   = hosts

[inventory]
enable_plugins              = ini
```

Needed the following for Ansible to read the `hosts` file (which parser it should use to read the file).

```
[inventory]
enable_plugins = ini
```

You might not need the last part of the config. Try running Ansible when removing the following part:

```
[ssh_connection]
ssh_args =
```

If you then get an error about "ssh and ControlSocket/permission denied for cp/ssh" add it again. You can read about the problem here, https://stackoverflow.com/a/41698903. There are supposed to be fixes for it but i can't get them to work.


### Run locally

When we want to work against an API, as the AWS modules do, we don't want Ansible to SSH to any server. So we connect to localhost without an ssh connection.

In `hosts` we need:

```
[local]
localhost ansible_connection=local
```

In the playbook to use the local host:

```
-   hosts: local
    connection: local # Keep ansible from open ssh connection
    gather_facts: False
```

When we run local plays we also need to change which Python interpreter should be used, to the one in our virtual environment. This is done in `groups_vars/local.yml`. With the line `ansible_python_interpreter: ../venv/bin/python`.


### Testing something out
Sometime you just want to test something, check value of a variable. You can do that with the following:

`ansible -m debug -a msg="{{playbook_dir}}" local`

Just replace `msg=""` with that you want to check.


## Encoding Error

If you get the following error:

```
File "microblog/.venv/lib/python3.5/site-packages/boto/rds2/layer1.py", line 3779, in _make_request
  return json.loads(body)
File "/usr/lib/python3.5/json/__init__.py", line 312, in loads
  s.__class__.__name__))
TypeError: the JSON object must be str, not 'bytes'

.......

File \"microblog/.venv/lib/python3.5/site-packages/boto/rds2/layer1.py\", line 1522, in describe_db_instances\n    path='/', params=params)\n  File \"../git/microblog/.venv/lib/python3.5/site-packages/boto/rds2/layer1.py\", line 3779, in _make_request\n    return json.loads(body)\n  File \"/usr/lib/python3.5/json/__init__.py\", line 312, in loads\n    s.__class__.__name__))\nTypeError: the JSON object must be str, not 'bytes'\n",
    "module_stdout": "",
    "msg": "MODULE FAILURE\nSee stdout/stderr for the exact error",
    "rc": 1
}
```

Open the file `venv/lib/python3.5/site-packages/boto/rds2/layer1.py` and go to line 3779 (this can change), look for the line `return json.loads(body)`. Add a new line before that one with `body = response.read().decode('utf-8')`.

You can read about the error here, https://github.com/boto/boto/issues/2677.
