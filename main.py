#!/usr/bin/env python3
"""
Neuro-Symbolic Rule Discovery System - Alpha Prototype
Following SPEC.md v0.2
"""

import json
from core.symbolic_core import SymbolicCore

print("=== Neuro-Symbolic Rule Discovery System (Star) - Alpha ===")
print("Loading SPEC.md and AGENTS.md...\n")

with open("SPEC.md", "r") as f:
    spec = f.read()
print("SPEC.md loaded successfully (v0.2 with Mao emphasis)")

with open("AGENTS.md", "r") as f:
    agents_guide = f.read()
print("AGENTS.md loaded - autonomous research mode active\n")

print("Initializing two-agent neuro-symbolic loop...")
symbolic = SymbolicCore()

print("\n" + "="*60)
print("Initial State: True Zero Knowledge")
print("Symbolic Core ready. Neural Agent will be connected in next iteration.")
print("System is now in active research mode.")
print("="*60 + "\n")

print(symbolic.get_status())

print("\nNext step: Implement simple Mao-like game simulator + Neural Agent connector.")
print("Then run first closed-loop experiments with hypothesis generation and testing.")
print("\nThe system will now improve itself iteratively from here.")
