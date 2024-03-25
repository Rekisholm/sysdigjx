#!/bin/bash

container_ids=$(docker ps -q)

statement="sysdig -s 0 -p\"*%evt.datetime %proc.name %proc.pid %proc.vpid %evt.dir %evt.type %fd.name %proc.ppid %proc.exepath %evt.rawres %fd.lip %fd.rip %fd.lport %fd.rport %evt.info %container.id %container.name\" \"container.name!=host"

is_first=true
for container_id in $container_ids; do
    if $is_first; then
        statement="$statement and (container.id=$container_id"
        is_first=false
    else
        statement="$statement or container.id=$container_id"
    fi
done
statement="$statement )\" -j -w log_container_teach_tmp.scap"
#statement="$statement ) and container.name!=host and container.name!=<N/A> and (evt.type=open or evt.type=openat or evt.type=read or evt.type=write or evt.type=sendto or evt.type=recvfrom or evt.type=execve or evt.type=fork or evt.type=clone or evt.type=bind or evt.type=listen or evt.type=connect or evt.type=accept or evt.type=accept4 or evt.type=chmod or evt.type=connect)\" -j -w log_container.scap"

echo "$statement" > sysdig_cmd_teach.sh
