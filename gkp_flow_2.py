''' Filling blanks: https://github.com/gordonyen/op-project/blob/master/flow_stats.json'''
''' ./pox.py samples.pretty_log forwarding.l2_learning misc.gkp_flows
the steps: 1. setup the network
           2. setup port flow table, using dpctl, port1=h1=10.0.0.1
           3. set h1 as HTTP server
           4. h2 wget -O h1 %request
           '''
from pox.core import core
from pox.lib.util import dpidToStr
import pox.openflow.libopenflow_01 as of
from datetime import datetime
import pytz
# include as part of the betta branch
from pox.openflow.of_json import *
# include as part of the betta branch
#from pox.openflow.of_json import *
import json
from datetime import datetime

log = core.getLogger()

def timestamp_string():
    string = datetime.isoformat(pytz.utc.localize(datetime.utcnow()))
    return string
    
'''def gkp_list(event):
  #data = open(flow_stats.json)
  json_data=json.dumps({
  "flow_id": 0,
  "time": "000-00-00T00:00:00Z",
  "results": [
    {
      "destination_ip": "0.0.0.0",
      "destination_port": 0000,
      "source_ip": "0.0.0.0",
      "source_port": 0,
      "flow_bytes": 0,
      "flow_packets": 0,
      "port_bytes": 0,
      "port_packets": 0
    }
  ]
  })
  data_object = json.load(json_data) #type: dict. 
  data_object['port_id'] = event.dpid
  now = datetime.now()
  date_object['time'] = timestamp_string()
  for foo in data_object['results']:
    foo['destination_ip'] = event.match.nw_dst
    foo['destination_port'] = event.match.tp_dst
    foo['source_ip'] = event.match.nw_src
    foo['source_port'] = event.match.tp_src
    foo['flow_bytes'] = flowbytes # not define yet
    foo['flow_packets'] = flowpackets
    foo['port_bytes'] = portbytes
    foo['port_packets'] = portpackets# not define yet
    
  return data_object
'''

def _timer_func ():
  for connection in core.openflow._connections.values():
    connection.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))
    connection.send(of.ofp_stats_request(body=of.ofp_port_stats_request()))
  log.debug("Sent %i flow/port stats request(s)", len(core.openflow._connections))
    
def _handle_flowstats_received (event):
  flowbyte=0
  flowpacket=0
  portbyte = 0
  port = 0
  portpacket = 0
  stats = flow_stats_to_list(event.stats)
  log.debug("FlowStatsReceived from %s: %s",
  dpidToStr(event.connection.dpid), stats)
  json_data=json.dumps({
    "flow_id": 0,
    "time": "000-00-00T00:00:00Z",
    "destination_ip": "0.0.0.0",
    "destination_port": 0,
    "source_ip": "0.0.0.0",
    "destination_MAC":"00:00:00:00:00:02",
    "source_MAC":"00:00:00:00:00:01",
    "source_port": 0,
    "flow_bytes": 0,
    "flow_packets": 0,
    "port_bytes": 0,
    "port_packets": 0
  })
  data_object = json.loads(json_data) 
  data_object['time'] = timestamp_string()

  #print data_object
  for f in event.stats:
    #print stats
    #print "\n"
    sVar=str(stats)
    sVar=sVar.replace("IPAddr('","'IPAddr(")
    sVar=sVar.replace("')",")'")
    sVar=sVar.replace("'",'"')
    preList=json.loads(sVar)
    proList=preList[0]
    List=proList['match']
    data_object['destination_ip'] = List['get_nw_dst']
    data_object['destination_tcp'] = List['tp_dst']
    data_object['destination_MAC']=List['dl_dst']
    data_object['source_ip'] = List['get_nw_src']
    data_object['source_tcp'] = List['tp_src']
    data_object['source_port']=List['in_port']
    data_object['source_MAC']=List['dl_src']
    data_object['flow_bytes'] = proList['byte_count'] # not define yet
    data_object['flow_packets'] = proList['packet_count']
    data_object['port_bytes'] = portbyte
    data_object['port_packets'] = portpacket# not define yet
  print data_object

  #stats = flow_stats_to_list(event.stats)
  #flowbytes = 0
  #flows = 0
  #flowpacket = 0
  
  #for f in event.stats:
  #    flowbytes += f.byte_count
  #    flowpacket += f.packet_count
  #    flows += 1
      


def _handle_portstats_received (event):
    
  #stats = flow_stats_to_list(event.stats)
  portbyte = 0
  port = 0
  portpacket = 0
  return portbyte, port, portpacket
  
  #for p in event.stats:
  #    portbytes += p.byte_count
  #    portpacket += p.packet_count
  #    ports += 1
def launch ():
  from pox.lib.recoco import Timer

  # attach handsers to listners
  core.openflow.addListenerByName("FlowStatsReceived", 
    _handle_flowstats_received) 
  core.openflow.addListenerByName("PortStatsReceived", 
    _handle_portstats_received) 

  # timer set to execute every five minutes 30 sec to test
  Timer(5, _timer_func, recurring=True)
