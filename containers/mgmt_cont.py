from .models import Container
import lxc

def sync(cid):
    cdb = Container.objects.get(id=cid)
    clxc = lxc.Container(cdb.name)
    if clxc.state == "RUNNING":
        clxc.set_config_item('lxc.network.0.ipv4_gateway', '10.1.1.1')
        cdb.net_ip = clxc.get_ips(timeout=1)[0]
    else:
        cdb.net_ip = "0.0.0.0"
    cdb.save()


