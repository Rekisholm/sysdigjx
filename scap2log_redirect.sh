sysdig -p"*%evt.datetime %proc.name %proc.pid %proc.vpid %evt.dir %evt.type %fd.name %proc.ppid %proc.exepath %evt.rawres %fd.lip %fd.rip %fd.lport %fd.rport %container.id %container.name %evt.info" "container.id!=host" -r log_container_teach_tmp.scap >> atk_container_teach.log
mv atk_container_teach.log /var/log/sysdig/atk_container_teach.log
