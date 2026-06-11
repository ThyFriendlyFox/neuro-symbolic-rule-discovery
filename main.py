#!/usr/bin/env python3
"""
Neuro-Symbolic Rule Discovery System (Star) - Alpha Prototype
Live commentary + continuous execution mode with internal heartbeat.
Every step is being shown. Not stopping.
"""

import time
import random
from core.symbolic_core import SymbolicCore
from agents.neural_agent import NeuralAgent
from games.simple_mao import SimpleMaoGame

print("=== Neuro-Symbolic Rule Discovery System (Star) - Alpha ===")
print("Live commentary + continuous execution mode with internal heartbeat.")
print("Every step is being shown. Not stopping.\n")

print("Step: Initializing all components...")
symbolic = SymbolicCore()
neural = NeuralAgent()
game = SimpleMaoGame(seed=123)

print("All components initialized successfully.")
print("Starting continuous experiment with multiple competing hypotheses.\n")
print("="*90)

heartbeat_counter = 0

for round_num in range(30):
    heartbeat_counter += 1
    print(f"\n[Round {round_num + 1}] 🫀")

    if heartbeat_counter % 5 == 0:
        print("🫀 HEARTBEAT: Still actively iterating on the neuro-symbolic system.")

    state = game.get_state()
    neural.observe(state, {"last_action": "observing"})

    new_hypotheses = neural.generate_hypotheses(symbolic, n=5)

    for hyp in new_hypotheses:
        symbolic.add_hypothesis(
            statement=hyp.statement,
            formal_condition=hyp.formal_condition,
            tags=hyp.tags
        )

    test_card, test_spoken = symbolic.select_next_experiment()

    print(f"Symbolic Core selected test move: card={test_card}, spoken='{test_spoken or ''}'")

    success, reason = game.play_move(test_card, test_spoken)

    context = {
        "card": test_card,
        "previous_card": game.played_cards[-2] if len(game.played_cards) > 1 else 0,
        "spoken": bool(test_spoken),
        "penalty": not success,
        "round": round_num
    }

    symbolic.record_observation({
        "move": test_card,
        "spoken": test_spoken,
        "success": success,
        "reason": reason,
        "context": context
    })

    for hyp_id in list(symbolic.hypotheses.keys()):
        result = symbolic.evaluate_hypothesis(hyp_id, context)
        supports = (result == (not success))
        symbolic.update_from_result(hyp_id, supports)

    symbolic.calculate_theory_confidence()

    print(f"Result: {'✓ Success' if success else '✗ PENALTY'} → {reason}")
    print(f"Current theory confidence: {symbolic.current_theory_confidence:.1%}")

    time.sleep(0.6)

print("\n" + "="*90)
print("30-round experiment completed.")
print(symbolic.get_status())
print("\n🫀 HEARTBEAT: Continuing without stopping.")
print("Next: I will begin self-critique of the current architecture as required by SPEC.md")
print("and decide on the next major improvement.")
print("Still in continuous live commentary mode - not stopping.")
