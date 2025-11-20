import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/estelamb/PFG_Telematica/Implementation/Drone/install/state_vector_pubsub'
