# How to

**Feel free to fork this repository if you want to run your own labs**

This ansible workspace is used to setup a basic GNS3 topology with boiler plate configuration on the following devices:

- Cisco IOSvL2
- Cisco IOSvL3
- Arista vEOS
- Alpine docker host
- NAT cloud

**NOTE:** You must be under this directory to be able to run the commands

## Lab creation

- To setup the GNS3 topology and **only** generate the configuration files, you must set:

`inventory/gns3_vars.yml`
```
boiler_plate:
    config: generate
```

The configuration files are created under the `build` folder, and by default are not pushed by git (if you use this repo `gitignore` file of course)

- Or to setup the lab and also push the boiler plate configuration over the telnet/console connection of the server, you must set:

`inventory/gns3_vars.yml`
```
boiler_plate:
    config: deploy
    # If you want to manually tell the playbook when to start the config push, set to `no`
    automated_push: yes
    automated_push_delay: 3
```

Now you can create the topology and configuration:

```
ansible-playbook lab.yml -e execute=create
```

## Lab teardown

You can stop and delete the topology by running:

```
ansible-playbook lab.yml -e execute=delete
```
