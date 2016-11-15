from stem import CircStatus
from stem.control import Controller

#Open the control port
with Controller.from_port(port = 9051) as controller:
  controller.authenticate("Password1") #Provide password here

  #Grab all circuits currently established
  for circ in sorted(controller.get_circuits()):
    if circ.status != CircStatus.BUILT:
      continue

    print("")
    print("Circuit %s (%s)" % (circ.id, circ.purpose))

    #Dereferences the memory location given by get_circuits and print
    for i, entry in enumerate(circ.path):
      div = '+' if (i == len(circ.path) - 1) else '|'
      fingerprint, nickname = entry

      desc = controller.get_network_status(fingerprint, None)
      address = desc.address if desc else 'unknown'

      print(" %s- %s (%s, %s)" % (div, fingerprint, nickname, address))
