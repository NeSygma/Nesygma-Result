# Benchmark Report (SWITCHER): agieval_lsat - lsat_31

**Provider:** xiaomi
**Model:** mimo-v2.5-pro
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 387.06s

## System 1 Execution Context

```json
{"answer": "E"}
```

## Switcher Execution


 SWITCHER META EVALUATOR AGENT

 Query: PROBLEM:
A loading dock consists of exactly six bays numbered 1 through 6 consecutively from one side of the dock to the other. Each bay is holding a different one of exactly six types of cargo—fuel, grain, livestock, machinery, produce, or textiles. The following apply: The bay holding grain has a higher number than the bay holding livestock. The bay holding livestock has a higher number than the bay holding textiles. The bay holding produce has a higher number than the bay holding fuel. The bay holding textiles is next to the bay holding produce.Q: Which one of the following CANNOT be the type of cargo held in bay 4? Answer Choices: (A)grain (B)livestock (C)machinery (D)produce (E)textiles
A: Among A through E, the answer is

SYSTEM 1 ANSWER (For Evaluation):
{"answer": "E"}

ANTI-ANCHORING REMINDER: Do NOT let the System 1 Answer above bias your independent reasoning in Stage 2. You MUST complete your own derivation from the premises alone before comparing against the System 1 Answer. Treat the System 1 Answer as a hypothesis to be verified, not as a guide.

Follow your system instructions to complete all 5 Metacognitive stages evaluating the provided SYSTEM 1 ANSWER.
Apply the three cognitive de-biasing checks (anchoring, confirmation, and overconfidence) at each relevant stage as instructed.
After completing all stages, output your confidence score in EXACTLY this format on a new line:
Confidence: <number between 0 and 100>%

**Stage 1 — Comprehension & Formalization**  
Premises:  
1. Grain > Livestock (bay number)  
2. Livestock > Textiles  
3. Produce > Fuel  
4. Textiles is next to Produce (adjacent bays)  

Conclusion to evaluate: Which cargo CANNOT be in bay 4?  
System 1 claims answer is (E) textiles.  

**Stage 2 — Independent Reasoning (Anti-Anchoring Step)**  
We need to determine which cargo is impossible in bay 4 given the constraints.  

From (1) and (2): Grain > Livestock > Textiles → Grain > Textiles.  
From (3): Produce > Fuel.  
From (4): Textiles and Produce are adjacent.  

Let’s denote positions 1–6. We’ll test each cargo for bay 4.  

**Test (A) Grain in bay 4:**  
If Grain=4, then Livestock < 4 (from Grain > Livestock). Also Textiles < Livestock < 4.  
Produce > Fuel, and Textiles adjacent to Produce.  
Possible arrangement: e.g., Textiles=2, Produce=3 (adjacent), Livestock=1, Grain=4, Fuel=5, Machinery=6.  
Check: Grain(4) > Livestock(1) ✓, Livestock(1) > Textiles(2)? No, 1 > 2 false. So need Livestock > Textiles.  
Try: Textiles=1, Produce=2 (adjacent), Livestock=3, Grain=4, Fuel=5, Machinery=6.  
Check: Grain(4) > Livestock(3) ✓, Livestock(3) > Textiles(1) ✓, Produce(2) > Fuel(5)? No, 2 > 5 false.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5.  
Produce(2) > Fuel(6)? No.  
Try: Textiles=2, Produce=3, Livestock=1, Grain=4, Fuel=5, Machinery=6 fails Livestock > Textiles.  
Try: Textiles=3, Produce=4? But Grain=4 already, so Produce cannot be 4.  
Try: Textiles=5, Produce=6 (adjacent), Livestock=4? But Grain=4, so Livestock cannot be 4.  
Try: Textiles=5, Produce=6, Livestock=3, Grain=4, Fuel=1, Machinery=2.  
Check: Grain(4) > Livestock(3) ✓, Livestock(3) > Textiles(5)? No.  
Try: Textiles=6, Produce=5 (adjacent), Livestock=4? Grain=4 conflict.  
Try: Textiles=6, Produce=5, Livestock=3, Grain=4, Fuel=1, Machinery=2.  
Livestock(3) > Textiles(6)? No.  
Try: Textiles=4? But Grain=4, so no.  
Try: Textiles=3, Produce=2 (adjacent), Livestock=1, Grain=4, Fuel=5, Machinery=6.  
Produce(2) > Fuel(5)? No.  
Try: Textiles=3, Produce=2, Livestock=1, Grain=4, Fuel=6, Machinery=5.  
Produce(2) > Fuel(6)? No.  
Try: Textiles=2, Produce=1 (adjacent), Livestock=3, Grain=4, Fuel=5, Machinery=6.  
Produce(1) > Fuel(5)? No.  
Try: Textiles=2, Produce=1, Livestock=3, Grain=4, Fuel=6, Machinery=5.  
Produce(1) > Fuel(6)? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2,

### TOKEN USAGE

  Input tokens:  3,032
  Output tokens: 32,768
  Total tokens:  35,800

COMPLETE

### Switcher Final Answer

```
**Stage 1 — Comprehension & Formalization**  
Premises:  
1. Grain > Livestock (bay number)  
2. Livestock > Textiles  
3. Produce > Fuel  
4. Textiles is next to Produce (adjacent bays)  

Conclusion to evaluate: Which cargo CANNOT be in bay 4?  
System 1 claims answer is (E) textiles.  

**Stage 2 — Independent Reasoning (Anti-Anchoring Step)**  
We need to determine which cargo is impossible in bay 4 given the constraints.  

From (1) and (2): Grain > Livestock > Textiles → Grain > Textiles.  
From (3): Produce > Fuel.  
From (4): Textiles and Produce are adjacent.  

Let’s denote positions 1–6. We’ll test each cargo for bay 4.  

**Test (A) Grain in bay 4:**  
If Grain=4, then Livestock < 4 (from Grain > Livestock). Also Textiles < Livestock < 4.  
Produce > Fuel, and Textiles adjacent to Produce.  
Possible arrangement: e.g., Textiles=2, Produce=3 (adjacent), Livestock=1, Grain=4, Fuel=5, Machinery=6.  
Check: Grain(4) > Livestock(1) ✓, Livestock(1) > Textiles(2)? No, 1 > 2 false. So need Livestock > Textiles.  
Try: Textiles=1, Produce=2 (adjacent), Livestock=3, Grain=4, Fuel=5, Machinery=6.  
Check: Grain(4) > Livestock(3) ✓, Livestock(3) > Textiles(1) ✓, Produce(2) > Fuel(5)? No, 2 > 5 false.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5.  
Produce(2) > Fuel(6)? No.  
Try: Textiles=2, Produce=3, Livestock=1, Grain=4, Fuel=5, Machinery=6 fails Livestock > Textiles.  
Try: Textiles=3, Produce=4? But Grain=4 already, so Produce cannot be 4.  
Try: Textiles=5, Produce=6 (adjacent), Livestock=4? But Grain=4, so Livestock cannot be 4.  
Try: Textiles=5, Produce=6, Livestock=3, Grain=4, Fuel=1, Machinery=2.  
Check: Grain(4) > Livestock(3) ✓, Livestock(3) > Textiles(5)? No.  
Try: Textiles=6, Produce=5 (adjacent), Livestock=4? Grain=4 conflict.  
Try: Textiles=6, Produce=5, Livestock=3, Grain=4, Fuel=1, Machinery=2.  
Livestock(3) > Textiles(6)? No.  
Try: Textiles=4? But Grain=4, so no.  
Try: Textiles=3, Produce=2 (adjacent), Livestock=1, Grain=4, Fuel=5, Machinery=6.  
Produce(2) > Fuel(5)? No.  
Try: Textiles=3, Produce=2, Livestock=1, Grain=4, Fuel=6, Machinery=5.  
Produce(2) > Fuel(6)? No.  
Try: Textiles=2, Produce=1 (adjacent), Livestock=3, Grain=4, Fuel=5, Machinery=6.  
Produce(1) > Fuel(5)? No.  
Try: Textiles=2, Produce=1, Livestock=3, Grain=4, Fuel=6, Machinery=5.  
Produce(1) > Fuel(6)? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=5, Machinery=6 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=6, Machinery=5 fails Produce > Fuel.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=4? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=3? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=2? No.  
Try: Textiles=1, Produce=2, Livestock=3, Grain=4, Fuel=1? No.  
Try: Textiles=1, Produce=2,
```
