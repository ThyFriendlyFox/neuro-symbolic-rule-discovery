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
from games.real_mao import RealMaoGame

print("=== Neuro-Symbolic Rule Discovery System (Star) - Alpha ===")
print("Live commentary + continuous execution mode with internal heartbeat.")
print("Every step is being shown. Not stopping.\n")

print("Step: Initializing all components...")
symbolic = SymbolicCore()
neural = NeuralAgent()
game = RealMaoGame(seed=123)

print("All components initialized successfully.")
print("Starting open-ended continuous discovery (no fixed round limit).\n")
print("="*90)

MAX_ROUNDS = 120          # Safety cap
CONFIDENCE_TARGET = 0.90  # Stop a game once we reach this

heartbeat_counter = 0
round_num = 0

while round_num < MAX_ROUNDS and symbolic.current_theory_confidence < CONFIDENCE_TARGET:
    round_num += 1
    heartbeat_counter += 1
    print(f"\n[Round {round_num}] 🫀")

    if heartbeat_counter % 10 == 0:
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

    test_card, test_spoken = symbolic.select_next_experiment(state)

    print(f"Symbolic Core selected test move: card={test_card}, spoken='{test_spoken or ''}'")

    success, reason = game.play_move(test_card, test_spoken)

    context = {
        "card": test_card,
        "previous_card": game.played_cards[-2] if len(game.played_cards) > 1 else 0,
        "spoken": bool(test_spoken),
        "penalty": not success,
        "round": round_num,
        # Abstract aliases for NeuralAgent compatibility (zero-knowledge predicates)
        "state_var": test_card,
        "action": test_card,
        "previous_action": game.played_cards[-2] if len(game.played_cards) > 1 else 0,
        "dealer_response": reason,
        "history": len(game.played_cards)
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

    # Integrate interrogation: close the two-agent dialogue loop (fixes missing integration)
    if round_num % 5 == 0 or symbolic.current_theory_confidence < 0.4:
        questions = symbolic.generate_interrogation_questions()
        if questions:
            responses = neural.respond_to_interrogation(questions, symbolic)
            print(f"  Interrogation cycle: {len(questions)} questions → {len(responses)} responses")
            # Generate fresh hypotheses from responses
            extra_hyps = neural.generate_hypotheses(symbolic, n=2)
            for hyp in extra_hyps:
                symbolic.add_hypothesis(hyp.statement, hyp.formal_condition, hyp.tags)

    symbolic.next_round()
    time.sleep(0.4)

print("\n" + "="*90)
print(f"Run ended after {round_num} rounds.")
print(f"Final theory confidence: {symbolic.current_theory_confidence:.1%}")
print(symbolic.get_status())
print("\n🫀 Ready for next phase (new game generation + real predicate evaluation).")
print("Still in continuous live commentary mode - not stopping.")
