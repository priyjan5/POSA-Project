from stem import CircStatus
from stem.control import Controller


o = open("/var/lib/tor/fingerprint", 'r')
my_nick, my_finger = o.readline().split(' ')

circuits = {my_finger:{"my_nickname":my_nick, "circuits":{}}}

with Controller.from_port(port = 9051) as controller:
  controller.authenticate("Password1")

  for circ in sorted(controller.get_circuits()):
    if circ.status != CircStatus.BUILT:
      continue

    print("")
    print("Circuit %s (%s)" % (circ.id, circ.purpose))

    circuits[my_finger]["circuits"][circ.id] = {}

    for i, entry in enumerate(circ.path):
      div = '+' if (i == len(circ.path) - 1) else '|'
      fingerprint, nickname = entry

      desc = controller.get_network_status(fingerprint, None)
      address = desc.address if desc else 'unknown'
      
      if i == 0:
        circuits[my_finger]["circuits"][circ.id]["entry"] = {"fingerprint":fingerprint, "nickname":nickname, "ip":address}
      elif i == 1:
        circuits[my_finger]["circuits"][circ.id]["relay"] = {"fingerprint":fingerprint, "nickname":nickname, "ip":address}
      elif i == 2:
        circuits[my_finger]["circuits"][circ.id]["exit"] = {"fingerprint":fingerprint, "nickname":nickname, "ip":address}
      
print circuits
