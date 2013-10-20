''' Filling blanks: https://github.com/gordonyen/op-project/blob/master/flow_stats.json'''

from pox.core import core
from pox.lib.util import dpidToStr
import pox.openflow.libopenflow_01 as of

# include as part of the betta branch
#from pox.openflow.of_json import *
import json


def gkp_list(event):
  #data = open(flow_stats.json)
  json_data=json.dumps({
  "flow_id": 123,
  "time": "2012-07-01T13:01:00Z",
  "results": [
    {
      "destination_ip": "131.187.127.16",
      "destination_port": 17240,
      "source_ip": "131.187.118.27",
      "source_port": 49832,
      "bytes": 342,
      "packets": 8
    }
  ]
  })
  data_object = json.load(json_data) #type: dict. 
  data_object['port_id'] = event.dpid
  for foo in data_object['flow_id']:
    foo['destination_ip'] = event.match.nw_dst
    foo['destination_port'] = event.match.tp_dst
    foo['source_ip'] = event.match.nw_src
    foo['source_port'] = event.match.tp_src
    foo['bytes'] = flowbytes+portbytes # not define yet
    foo['packets'] = flowpackets+portpackets# not define yet
 

def _timer_func ():
  for connection in core.openflow._connections.values():
    connection.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))
    connection.send(of.ofp_stats_request(body=of.ofp_port_stats_request()))
    
def _handle_flowstats_received (event):
  #stats = flow_stats_to_list(event.stats)
  flowbytes = 0
  flows = 0
  flowpacket = 0
  
  for f in event.stats:
      flowbytes += f.byte_count
      flowpacket += f.packet_count
      flows += 1

def _handle_portstats_received (event):
  #stats = flow_stats_to_list(event.stats)
  portbytes = 0
  ports = 0
  portpacket = 0
  
  for p in event.stats:
      portbytes += p.byte_count
      portpacket += p.packet_count
      ports += 1
def launch ():
  from pox.lib.recoco import Timer

  # attach handsers to listners
  core.openflow.addListenerByName("FlowStatsReceived", 
    _handle_flowstats_received) 
  core.openflow.addListenerByName("PortStatsReceived", 
    _handle_portstats_received) 

  # timer set to execute every five minutes
  Timer(300, _timer_func, recurring=True)
