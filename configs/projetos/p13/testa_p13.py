import argparse
import m5
from m5.objects import *

ap = argparse.ArgumentParser()
ap.add_argument("--protocol", choices=["MSI", "MESILG"], default="MESI_LG")
ap.add_argument("--exclusive", choices=["on", "off"], default="on")
ap.add_argument("--ports", type=int, default=4)
ap.add_argument("--checks", type=int, default=100000)
ap.add_argument("--seed", type=int, default=1)
ap.add_argument("--l1-size", default="16KiB")
args = ap.parse_args()

m5.core.seedRandom(args.seed)

system = System()

# TODO(aluno): relógio, mem_mode="timing", faixa de memória e
# SimpleMemory, como em ruby_test.py.
system.tester = RubyTester(checks_to_complete=args.checks,
wakeup_frequency=10, num_cpus=args.ports)
# TODO(aluno): sistema Ruby de teste do protocolo escolhido, derivado de
# test_caches.py, com L1 de tamanho args.l1_size e, no
# MESI_LG, enable_exclusive=(args.exclusive == "on").

root = Root(full_system=False, system=system)
m5.instantiate()
ev = m5.simulate()
print(f"Fim @ tick {m5.curTick()}: {ev.getCause()}")
