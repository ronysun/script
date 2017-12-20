# coding: utf-8
import sys
packet_len = int(sys.argv[1])
try:
    bandwidth = int(sys.argv[2])
except:
    bandwidth = 1000
pps = bandwidth*1000*1000/8/(packet_len + 8 + 12)
print 'Packet length %s pps is %s,when bandwidth is %sM' % (packet_len, pps, bandwidth)
