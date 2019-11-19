group_vars
=======================

In this folder we assign variables to specific host groups. You can read more about it on [Ansible best practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html#group-and-host-variables).

In `all.yml` we can assign variables that will be available for all host groups, in other words will always be there.
For example if all the severs use the same user name, password or contact information we can add it to this file and then it can be used in all plays.

In `local.yml` we put variables that we want to be available for all hosts in the group `local`. If you look in the hosts file, there should be a group called `local` with the host `localhost`.
In the file we assign the variable `ansible_python_interpreter` to be python3 in out virtual environemnt.

You can add variables as you see fit to the files and also add more files for when you add more host groups. Name the file the same as your group and Ansible will find it automatically.
