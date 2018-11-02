'''
Created on Oct 12, 2016

@author: mwittie
'''
import network3
import link3
import threading
from time import sleep

##configuration parameters
router_queue_size = 0 #0 means unlimited
simulation_time = 30 #give the network sufficient time to transfer all packets before quitting

if __name__ == '__main__':
    object_L = [] #keeps track of objects, so we can kill their threads

    rout_tab_ad={"0000100003" : 0,
                "0000100004" : 1,
                "0000200003" : 0,
                "0000200004" : 1
                }
    rout_tab_bc={"0000100003" : 0,
                "0000100004" : 0,
                "0000200003" : 0,
                "0000200004" : 0
                }
    
    #create network nodes
    client = network3.Host(1)
    object_L.append(client)
    client2 = network3.Host(2)
    object_L.append(client2)
    server = network3.Host(3)
    object_L.append(server)
    server2 = network3.Host(4)
    object_L.append(server2)
    router_a = network3.Router(name='A', intf_count=2, rout_tab=rout_tab_ad, max_queue_size=router_queue_size)
    router_b = network3.Router(name='B', intf_count=1, rout_tab=rout_tab_bc, max_queue_size=router_queue_size)
    router_c = network3.Router(name='C', intf_count=1, rout_tab=rout_tab_bc, max_queue_size=router_queue_size)
    router_d = network3.Router(name='D', intf_count=2, rout_tab=rout_tab_ad, max_queue_size=router_queue_size)
    object_L.append(router_a)
    object_L.append(router_b)
    object_L.append(router_c)
    object_L.append(router_d)
    
    #create a Link Layer to keep track of links between network nodes
    link_layer = link3.LinkLayer()
    object_L.append(link_layer)
    
    #add all the links
    #link parameters: from_node, from_intf_num, to_node, to_intf_num, mtu
    link_layer.add_link(link3.Link(client, 0, router_a, 0, 50))
    link_layer.add_link(link3.Link(client2, 0, router_a, 1, 50))
    link_layer.add_link(link3.Link(router_a, 0, router_b, 0, 30))
    link_layer.add_link(link3.Link(router_a, 1, router_c, 0, 30))
    link_layer.add_link(link3.Link(router_b , 0, router_d, 0, 30))
    link_layer.add_link(link3.Link(router_c, 0, router_d, 1, 50))
    link_layer.add_link(link3.Link(router_d, 0, server, 0, 50))
    link_layer.add_link(link3.Link(router_d, 1, server2, 0, 50))
    
    
    #start all the objects
    thread_L = []
    thread_L.append(threading.Thread(name=client.__str__(), target=client.run))
    thread_L.append(threading.Thread(name=client2.__str__(), target=client2.run))
    thread_L.append(threading.Thread(name=server.__str__(), target=server.run))
    thread_L.append(threading.Thread(name=server2.__str__(), target=server2.run))
    thread_L.append(threading.Thread(name=router_a.__str__(), target=router_a.run))
    thread_L.append(threading.Thread(name=router_b.__str__(), target=router_b.run))
    thread_L.append(threading.Thread(name=router_c.__str__(), target=router_c.run))
    thread_L.append(threading.Thread(name=router_d.__str__(), target=router_d.run))
    
    thread_L.append(threading.Thread(name="Network", target=link_layer.run))
    
    for t in thread_L:
        t.start()
    
    
    #create some send events    
    for i in range(1):
        client.udt_send(1, 3, 'Sample data send mucho data to try and break code i have wrote%d' % i)
    
    
    #give the network sufficient time to transfer all packets before quitting
    sleep(simulation_time)
    
    #join all threads
    for o in object_L:
        o.stop = True
    for t in thread_L:
        t.join()
        
    print("All simulation threads joined")



# writes to host periodically
