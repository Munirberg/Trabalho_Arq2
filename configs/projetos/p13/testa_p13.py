import argparse
import m5
from m5.objects import *
from m5.params.param_types import AddrRange
from mem.SimpleMemory import SimpleMemory
from sim.ClockDomain import SrcClockDomain
from m5.util import addToPath

addToPath("learning_gem5/part3")
addToPath("configs/projetos/p13")

ap = argparse.ArgumentParser()
ap.add_argument("--protocol", choices=["MSI", "MESI_LG"], default="MESI_LG")
ap.add_argument("--exclusive", choices=["on", "off"], default="on")
ap.add_argument("--ports", type=int, default=4)
ap.add_argument("--checks", type=int, default=100000)
ap.add_argument("--seed", type=int, default=1)
ap.add_argument("--l1-size", default="16KiB")
args = ap.parse_args()

m5.core.seedRandom(args.seed)

system = System()

# Set the clock frequency of the system (and all of its children)
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

# Set up the system
system.mem_mode = "timing"  # Use timing accesses
system.mem_ranges = [AddrRange("512MiB")]  # Create an address range

# Create a simple memory controller and connect it to the membus
system.mem_ctrl = SimpleMemory(latency="50ns", bandwidth="0GiB/s")
system.mem_ctrl.range = system.mem_ranges[0]

system.tester = RubyTester(checks_to_complete=args.checks,
wakeup_frequency=10, num_cpus=args.ports)

# Seleciona e configura o sistema Ruby para o protocolo escolhido
from test_caches import TestCacheSystem

system.caches = TestCacheSystem(protocol=args.protocol, l1_size=args.l1_size, enable_exclusive=(args.exclusive == "on"))

system.caches.setup(system, system.tester, [system.mem_ctrl])

root = Root(full_system=False, system=system)
m5.instantiate()
ev = m5.simulate()
print(f"Fim @ tick {m5.curTick()}: {ev.getCause()}")
