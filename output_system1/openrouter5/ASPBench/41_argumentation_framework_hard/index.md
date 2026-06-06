# Benchmark Report (SYSTEM1): ASPBench - 41_argumentation_framework_hard

**Provider:** openrouter5
**Model:** deepseek/deepseek-v4-flash
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 167.34s


 SYSTEM 1 PURE REASONING AGENT

 Query: # Problem Statement

An abstract argumentation framework with argument hierarchies and attack types. Arguments have numerical levels, and attacks can be strong (always successful) or weak (successful only if attacker's level exceeds target's level). Find all **hierarchical stable extensions** satisfying three conditions: conflict-free (no successful self-attacks), self-defending (all attacks on members are counter-attacked), and maximal (all non-members are attacked).

## Instance Data

**Arguments:** a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16

**Levels:**
- Level 1: a1, a2, a3, a4, a5, a6
- Level 2: a7, a8, a9, a10, a11, a12
- Level 3: a13, a14, a15, a16

**Strong Attacks (always successful):**
- a2 → a1, a9 → a8, a14 → a13, a15 → a16
- a1 → a14, a16 → a15, a1 → a3, a1 → a4
- a13 → a7, a13 → a10, a3 → a5, a5 → a3

**Weak Attacks (successful only if attacker level > target level):**
- a8 → a2, a13 → a9, a8 → a5, a8 → a6
- a16 → a11, a16 → a12, a2 → a7, a10 → a13

## Constraints

1. **Conflict-Free**: No argument in the extension successfully attacks another argument in the same extension
2. **Self-Defending**: For every argument A in the extension and every external argument B that successfully attacks A, there must be an argument C in the extension that successfully attacks B
3. **Maximal Admissible (Preferred Extension)**: The extension is conflict-free and self-defending, and cannot be extended with any additional argument while maintaining these properties

**Note:** This problem seeks **preferred extensions** (maximal admissible sets), not stable extensions. A stable extension would require attacking all outside arguments, which is a stronger condition not required here.

## Objective

Find all valid preferred extensions (maximal admissible sets) that satisfy all three conditions.

## Output Format

```json
{
  "hierarchical_stable_extensions": [
    ["a1", "a8", "a13", "a16"],
    ["a2", "a9"]
  ]
}
```

**Field Descriptions:**
- `hierarchical_stable_extensions`: Array of arrays, where each inner array is a sorted list of argument names forming a valid extension


Return your final answer in JSON format.

We need to find all maximal admissible sets (preferred extensions) under the given attack rules.

**Step 1 – Determine successful attacks**  
Strong attacks always succeed. Weak attacks succeed only if attacker level > target level.

Levels:  
- Level 1: a1–a6  
- Level 2: a7–a12  
- Level 3: a13–a16  

Weak attacks:
- a8 (L2) → a2 (L1): L2 > L1 → succeeds  
- a13 (L3) → a9 (L2): L3 > L2 → succeeds  
- a8 (L2) → a5 (L1): succeeds  
- a8 (L2) → a6 (L1): succeeds  
- a16 (L3) → a11 (L2): succeeds  
- a16 (L3) → a12 (L2): succeeds  
- a2 (L1) → a7 (L2): L1 < L2 → fails  
- a10 (L2) → a13 (L3): L2 < L3 → fails  

So successful attacks are:

Strong:
- a2 → a1  
- a9 → a8  
- a14 → a13  
- a15 → a16  
- a1 → a14  
- a16 → a15  
- a1 → a3  
- a1 → a4  
- a13 → a7  
- a13 → a10  
- a3 → a5  
- a5 → a3  

Weak (successful):
- a8 → a2  
- a13 → a9  
- a8 → a5  
- a8 → a6  
- a16 → a11  
- a16 → a12  

**Step 2 – Build attack graph**  
We list each argument and who successfully attacks it:

- a1: attacked by a2  
- a2: attacked by a8  
- a3: attacked by a1, a5  
- a4: attacked by a1  
- a5: attacked by a3, a8  
- a6: attacked by a8  
- a7: attacked by a13  
- a8: attacked by a9  
- a9: attacked by a13  
- a10: attacked by a13  
- a11: attacked by a16  
- a12: attacked by a16  
- a13: attacked by a14, a1  
- a14: attacked by a1  
- a15: attacked by a16  
- a16: attacked by a15  

**Step 3 – Find admissible sets**  

We look for conflict-free sets that defend all members.

Start with small candidates:

- {a1}: attacked by a2, but a1 does not attack a2 → not defended.  
- {a2}: attacked by a8, a2 does not attack a8 → not defended.  
- {a8}: attacked by a9, a8 does not attack a9 → not defended.  
- {a13}: attacked by a14 and a1. a13 attacks a7, a10, a9, but not a14 or a1 → not defended.  
- {a16}: attacked by a15, a16 attacks a15 → defended. Also attacked by? a15 only. So {a16} is admissible.  

Check if {a16} can be extended:  
Add a13? a13 attacks a16? No. a16 attacks a13? No. Conflict-free? Yes. But a13 is attacked by a1 and a14. Does a16 defend a13? a16 attacks a15, not a1 or a14 → no. So cannot add a13.  
Add a8? a8 attacks a16? No. a16 attacks a8? No. Conflict-free. a8 attacked by a9. Does a16 attack a9? No → not defended.  
Add a2? a2 attacked by a8. a16 does not attack a8 → no.  
Add a1? a1 attacked by a2. a16 does not attack a2 → no.  
So {a16} is maximal? Check a15: a15 attacks a16, so cannot add. a11, a12 attacked by a16, so they can't be added (would cause conflict with a16). So {a16} is maximal admissible.

**Check {a15}**: attacked by a16, a15 attacks a16 → defended. Conflict-free? Yes. Can we add others?  
Add a13? a13 attacks a15? No. a15 attacks a13? No. Conflict-free. a13 attacked by a1, a14. Does a15 attack a1 or a14? No → not defended.  
Add a8? a8 attacked by a9. a15 doesn't attack a9 → no.  
Add a2? attacked by a8, no defense.  
So {a15} is maximal admissible.

**Check {a1, a13}**:  
a1 attacks a13? Yes (strong a1→a14? Wait a1→a14, not a13. a1→a13? No. So conflict-free? a1 attacks a14, a3, a4; a13 attacks a7, a10, a9. No mutual attack. So conflict-free.  
Defense:  
- a1 attacked by a2. a13 attacks a2? No. So not defended.  
So {a1, a13} fails.

**Check {a2, a9}**:  
a2 attacks a9? No. a9 attacks a2? No. Conflict-free.  
Defense:  
- a2 attacked by a8. a9 attacks a8 (strong a9→a8) → defended.  
- a9 attacked by a13. a2 attacks a13? No. So fails.

**Check {a8, a13}**:  
a8 attacks a13? No. a13 attacks a8? No. Conflict-free.  
Defense:  
- a8 attacked by a9. a13 attacks a9 (strong a13→a9) → defended.  
- a13 attacked by a1 and a14. a8 attacks a1? No. a8 attacks a14? No. So fails.

**Check {a8, a16}**:  
a8 attacks a16? No. a16 attacks a8? No. Conflict-free.  
Defense:  
- a8 attacked by a9. a16 attacks a9? No → fails.

**Check {a13, a16}**:  
a13 attacks a16? No. a16 attacks a13? No. Conflict-free.  
Defense:  
- a13 attacked by a1, a14. a16 attacks a1? No. a16 attacks a14? No → fails.

**Check {a1, a16}**:  
a1 attacks a16? No. a16 attacks a1? No. Conflict-free.  
Defense:  
- a1 attacked by a2. a16 attacks a2? No → fails.

**Check {a2, a16}**:  
a2 attacks a16? No. a16 attacks a2? No. Conflict-free.  
Defense:  
- a2 attacked by a8. a16 attacks a8? No → fails.

**Check {a9, a16}**:  
a9 attacks a16? No. a16 attacks a9? No. Conflict-free.  
Defense:  
- a9 attacked by a13. a16 attacks a13? No → fails.

**Check {a1, a8}**:  
a1 attacks a8? No. a8 attacks a1? No. Conflict-free.  
Defense:  
- a1 attacked by a2. a8 attacks a2 (weak a8→a2 succeeds) → defended.  
- a8 attacked by a9. a1 attacks a9? No → fails.

**Check {a2, a13}**:  
a2 attacks a13? No. a13 attacks a2? No. Conflict-free.  
Defense:  
- a2 attacked by a8. a13 attacks a8? No → fails.

**Check {a1, a9}**:  
a1 attacks a9? No. a9 attacks a1? No. Conflict-free.  
Defense:  
- a1 attacked by a2. a9 attacks a2? No → fails.

**Check {a2, a8}**:  
a8 attacks a2 (weak succeeds) → conflict, so not conflict-free.

**Check {a9, a13}**:  
a13 attacks a9 (strong) → conflict.

**Check {a1, a15}**:  
a1 attacks a15? No. a15 attacks a1? No. Conflict-free.  
Defense:  
- a1 attacked by a2. a15 attacks a2? No → fails.

**Check {a2, a15}**:  
a2 attacks a15? No. a15 attacks a2? No. Conflict-free.  
Defense:  
- a2 attacked by a8. a15 attacks a8? No → fails.

**Check {a8, a15}**:  
a8 attacks a15? No. a15 attacks a8? No. Conflict-free.  
Defense:  
- a8 attacked by a9. a15 attacks a9? No → fails.

**Check {a13, a15}**:  
a13 attacks a15? No. a15 attacks a13? No. Conflict-free.  
Defense:  
- a13 attacked by a1, a14. a15 attacks a1? No. a15 attacks a14? No → fails.

**Check {a1, a2}**: a2 attacks a1 (strong) → conflict.

**Check {a3, a5}**: a3↔a5 strong attacks → conflict.

**Check {a14, a16}**:  
a14 attacks a16? No. a16 attacks a14? No. Conflict-free.  
Defense:  
- a14 attacked by a1. a16 attacks a1? No → fails.

**Check {a1, a14}**: a1 attacks a14 (strong) → conflict.

**Check {a16}** and **{a15}** are maximal admissible so far.  

Check if any larger set works:  
Try {a1, a8, a13}?  
a1 attacks a13? No. a13 attacks a1? No. a8 attacks a1? No. a1 attacks a8? No. a8 attacks a13? No. a13 attacks a8? No. Conflict-free.  
Defense:  
- a1 attacked by a2 → a8 attacks a2 (yes) → defended.  
- a8 attacked by a9 → a13 attacks a9 (yes) → defended.  
- a13 attacked by a1 and a14. a1 is in set, but a1 attacks a13? No, a1 attacks a14, not a13. So a1 does not attack a13. So a13 is attacked by a1? Wait check: a1 → a14 (strong), not a13. So a13 is attacked by a14 and a1? Actually a1→a13? No. So a13 is attacked by a14 only? And a1? No. So a13 attacked by a14. Who defends? a1 attacks a14 (yes, strong a1→a14). So a1 defends a13 against a14. Also a13 attacked by a1? No. So all attacks on a13 are from a14, and a1 (in set) attacks a14 → defended.  
So {a1, a8, a13} is admissible. Can we add more?  
Try adding a16: a16 attacks a1? No. a1 attacks a16? No. a8 attacks a16? No. a13 attacks a16? No. a16 attacks a8? No. a16 attacks a13? No. Conflict-free.  
Defense for a16: a16 attacked by a15. Does anyone in set attack a15? a1 attacks a15? No. a8 attacks a15? No. a13 attacks a15? No. So not defended. So cannot add a16.  
Try adding a15: a15 attacks a16? Not relevant. a15 attacks anyone in set? a15→a16 only, so no conflict. But a15 attacked by a16. No one in set attacks a16? a1? No. a8? No. a13? No. So not defended.  
Try adding a2: a2 attacks a1 (strong) → conflict.  
Try adding a9: a9 attacks a8 (strong) → conflict.  
Try adding a3: a3 attacks a5, a5 attacks a3, but a3 attacks a1? No. a1 attacks a3 (strong) → conflict.  
Try adding a4: a1 attacks a4 (strong) → conflict.  
Try adding a5: a3 attacks a5? a3 not in set. a5 attacks a3? Not relevant. a5 attacks a1? No. a1 attacks a5? No. a8 attacks a5 (weak succeeds) → conflict.  
Try adding a6: a8 attacks a6 (weak succeeds) → conflict.  
Try adding a7: a13 attacks a7 (strong) → conflict.  
Try adding a10: a13 attacks a10 (strong) → conflict.  
Try adding a11: a16 not in set, so a11 not attacked by set? But a11 attacked by a16, but a16 not in set. a11 attacks anyone? No. So no conflict. But defense: a11 attacked by a16. No one in set attacks a16 → not defended.  
a12 similar.  
a14: a1 attacks a14 (strong) → conflict.  

So {a1, a8, a13} is maximal admissible.

Check {a1, a8, a13, a15}? a15 attacks a16, not in set. a15 attacked by a16. No one attacks a16 → not defended. So no.

Check {a1, a8, a13, a2}? conflict a2→a1.

Thus {a1, a8, a13} is one.

Check {a2, a9, a16}?  
a2 attacks a9? No. a9 attacks a2? No. a16 attacks a2? No. a2 attacks a16? No. a9 attacks a16? No. a16 attacks a9? No. Conflict-free.  
Defense:  
- a2 attacked by a8 → a9 attacks a8 (yes) → defended.  
- a9 attacked by a13 → a16 attacks a13? No → fails.

Check {a2, a9, a15}?  
a15 attacks a2? No. a2 attacks a15? No. a9 attacks a15? No. a15 attacks a9? No. Conflict-free.  
Defense:  
- a2 attacked by a8 → a9 attacks a8 → defended.  
- a9 attacked by a13 → a15 attacks a13? No → fails.

Check {a8, a13, a16}? Already checked defense fails for a13 (a1, a14 not attacked).

Check {a1, a13, a16}? Defense for a1: attacked by a2, no one attacks a2 → fails.

Check {a2, a8, a13}? a8 attacks a2 → conflict.

Check {a1, a9, a13}? a9 attacks a8? Not relevant. a1 attacked by a2 → no defense. Fails.

Check {a1, a8, a16}? a16 attacked by a15, no defense → fails.

Check {a1, a8, a15}? a15 attacked by a16, no defense → fails.

Check {a2, a9, a13}? a13 attacks a9 → conflict.

Check {a2, a9, a8}? a8 attacks a2 → conflict.

Check {a1, a8, a13} already found.

Check {a1, a8, a13, a?} no more.

Check {a15, a16}? a15 attacks a16 (strong) → conflict.

Check {a1, a8}? Not maximal because we can add a13.

Check {a8, a13}? Not maximal because we can add a1.

Check {a1, a13}? Not maximal because we can add a8.

Check {a16} and {a15} are maximal.

Check {a1, a8, a13} is maximal.

Check if {a2, a9} is maximal?  
a2 attacked by a8 → a9 attacks a8 → defended.  
a9 attacked by a13 → a2 attacks a13? No. So fails defense. So not admissible.

Check {a2, a9, a?} no.

Check {a1, a14}? conflict.

Check {a3, a5}? conflict.

Check {a7, a10, a13}? a13 attacks a7, a10 → conflict.

Check {a11, a12, a16}? a16 attacks a11, a12 → conflict.

Thus the maximal admissible sets are:  
{a16}, {a15}, {a1, a8, a13}.

```json
{
  "hierarchical_stable_extensions": [
    ["a1", "a8", "a13"],
    ["a15"],
    ["a16"]
  ]
}
```

### TOKEN USAGE

  Input tokens:  658
  Output tokens: 3,813
  Total tokens:  4,471

COMPLETE

## System 1 Final Answer

```json
We need to find all maximal admissible sets (preferred extensions) under the given attack rules.

**Step 1 – Determine successful attacks**  
Strong attacks always succeed. Weak attacks succeed only if attacker level > target level.

Levels:  
- Level 1: a1–a6  
- Level 2: a7–a12  
- Level 3: a13–a16  

Weak attacks:
- a8 (L2) → a2 (L1): L2 > L1 → succeeds  
- a13 (L3) → a9 (L2): L3 > L2 → succeeds  
- a8 (L2) → a5 (L1): succeeds  
- a8 (L2) → a6 (L1): succeeds  
- a16 (L3) → a11 (L2): succeeds  
- a16 (L3) → a12 (L2): succeeds  
- a2 (L1) → a7 (L2): L1 < L2 → fails  
- a10 (L2) → a13 (L3): L2 < L3 → fails  

So successful attacks are:

Strong:
- a2 → a1  
- a9 → a8  
- a14 → a13  
- a15 → a16  
- a1 → a14  
- a16 → a15  
- a1 → a3  
- a1 → a4  
- a13 → a7  
- a13 → a10  
- a3 → a5  
- a5 → a3  

Weak (successful):
- a8 → a2  
- a13 → a9  
- a8 → a5  
- a8 → a6  
- a16 → a11  
- a16 → a12  

**Step 2 – Build attack graph**  
We list each argument and who successfully attacks it:

- a1: attacked by a2  
- a2: attacked by a8  
- a3: attacked by a1, a5  
- a4: attacked by a1  
- a5: attacked by a3, a8  
- a6: attacked by a8  
- a7: attacked by a13  
- a8: attacked by a9  
- a9: attacked by a13  
- a10: attacked by a13  
- a11: attacked by a16  
- a12: attacked by a16  
- a13: attacked by a14, a1  
- a14: attacked by a1  
- a15: attacked by a16  
- a16: attacked by a15  

**Step 3 – Find admissible sets**  

We look for conflict-free sets that defend all members.

Start with small candidates:

- {a1}: attacked by a2, but a1 does not attack a2 → not defended.  
- {a2}: attacked by a8, a2 does not attack a8 → not defended.  
- {a8}: attacked by a9, a8 does not attack a9 → not defended.  
- {a13}: attacked by a14 and a1. a13 attacks a7, a10, a9, but not a14 or a1 → not defended.  
- {a16}: attacked by a15, a16 attacks a15 → defended. Also attacked by? a15 only. So {a16} is admissible.  

Check if {a16} can be extended:  
Add a13? a13 attacks a16? No. a16 attacks a13? No. Conflict-free? Yes. But a13 is attacked by a1 and a14. Does a16 defend a13? a16 attacks a15, not a1 or a14 → no. So cannot add a13.  
Add a8? a8 attacks a16? No. a16 attacks a8? No. Conflict-free. a8 attacked by a9. Does a16 attack a9? No → not defended.  
Add a2? a2 attacked by a8. a16 does not attack a8 → no.  
Add a1? a1 attacked by a2. a16 does not attack a2 → no.  
So {a16} is maximal? Check a15: a15 attacks a16, so cannot add. a11, a12 attacked by a16, so they can't be added (would cause conflict with a16). So {a16} is maximal admissible.

**Check {a15}**: attacked by a16, a15 attacks a16 → defended. Conflict-free? Yes. Can we add others?  
Add a13? a13 attacks a15? No. a15 attacks a13? No. Conflict-free. a13 attacked by a1, a14. Does a15 attack a1 or a14? No → not defended.  
Add a8? a8 attacked by a9. a15 doesn't attack a9 → no.  
Add a2? attacked by a8, no defense.  
So {a15} is maximal admissible.

**Check {a1, a13}**:  
a1 attacks a13? Yes (strong a1→a14? Wait a1→a14, not a13. a1→a13? No. So conflict-free? a1 attacks a14, a3, a4; a13 attacks a7, a10, a9. No mutual attack. So conflict-free.  
Defense:  
- a1 attacked by a2. a13 attacks a2? No. So not defended.  
So {a1, a13} fails.

**Check {a2, a9}**:  
a2 attacks a9? No. a9 attacks a2? No. Conflict-free.  
Defense:  
- a2 attacked by a8. a9 attacks a8 (strong a9→a8) → defended.  
- a9 attacked by a13. a2 attacks a13? No. So fails.

**Check {a8, a13}**:  
a8 attacks a13? No. a13 attacks a8? No. Conflict-free.  
Defense:  
- a8 attacked by a9. a13 attacks a9 (strong a13→a9) → defended.  
- a13 attacked by a1 and a14. a8 attacks a1? No. a8 attacks a14? No. So fails.

**Check {a8, a16}**:  
a8 attacks a16? No. a16 attacks a8? No. Conflict-free.  
Defense:  
- a8 attacked by a9. a16 attacks a9? No → fails.

**Check {a13, a16}**:  
a13 attacks a16? No. a16 attacks a13? No. Conflict-free.  
Defense:  
- a13 attacked by a1, a14. a16 attacks a1? No. a16 attacks a14? No → fails.

**Check {a1, a16}**:  
a1 attacks a16? No. a16 attacks a1? No. Conflict-free.  
Defense:  
- a1 attacked by a2. a16 attacks a2? No → fails.

**Check {a2, a16}**:  
a2 attacks a16? No. a16 attacks a2? No. Conflict-free.  
Defense:  
- a2 attacked by a8. a16 attacks a8? No → fails.

**Check {a9, a16}**:  
a9 attacks a16? No. a16 attacks a9? No. Conflict-free.  
Defense:  
- a9 attacked by a13. a16 attacks a13? No → fails.

**Check {a1, a8}**:  
a1 attacks a8? No. a8 attacks a1? No. Conflict-free.  
Defense:  
- a1 attacked by a2. a8 attacks a2 (weak a8→a2 succeeds) → defended.  
- a8 attacked by a9. a1 attacks a9? No → fails.

**Check {a2, a13}**:  
a2 attacks a13? No. a13 attacks a2? No. Conflict-free.  
Defense:  
- a2 attacked by a8. a13 attacks a8? No → fails.

**Check {a1, a9}**:  
a1 attacks a9? No. a9 attacks a1? No. Conflict-free.  
Defense:  
- a1 attacked by a2. a9 attacks a2? No → fails.

**Check {a2, a8}**:  
a8 attacks a2 (weak succeeds) → conflict, so not conflict-free.

**Check {a9, a13}**:  
a13 attacks a9 (strong) → conflict.

**Check {a1, a15}**:  
a1 attacks a15? No. a15 attacks a1? No. Conflict-free.  
Defense:  
- a1 attacked by a2. a15 attacks a2? No → fails.

**Check {a2, a15}**:  
a2 attacks a15? No. a15 attacks a2? No. Conflict-free.  
Defense:  
- a2 attacked by a8. a15 attacks a8? No → fails.

**Check {a8, a15}**:  
a8 attacks a15? No. a15 attacks a8? No. Conflict-free.  
Defense:  
- a8 attacked by a9. a15 attacks a9? No → fails.

**Check {a13, a15}**:  
a13 attacks a15? No. a15 attacks a13? No. Conflict-free.  
Defense:  
- a13 attacked by a1, a14. a15 attacks a1? No. a15 attacks a14? No → fails.

**Check {a1, a2}**: a2 attacks a1 (strong) → conflict.

**Check {a3, a5}**: a3↔a5 strong attacks → conflict.

**Check {a14, a16}**:  
a14 attacks a16? No. a16 attacks a14? No. Conflict-free.  
Defense:  
- a14 attacked by a1. a16 attacks a1? No → fails.

**Check {a1, a14}**: a1 attacks a14 (strong) → conflict.

**Check {a16}** and **{a15}** are maximal admissible so far.  

Check if any larger set works:  
Try {a1, a8, a13}?  
a1 attacks a13? No. a13 attacks a1? No. a8 attacks a1? No. a1 attacks a8? No. a8 attacks a13? No. a13 attacks a8? No. Conflict-free.  
Defense:  
- a1 attacked by a2 → a8 attacks a2 (yes) → defended.  
- a8 attacked by a9 → a13 attacks a9 (yes) → defended.  
- a13 attacked by a1 and a14. a1 is in set, but a1 attacks a13? No, a1 attacks a14, not a13. So a1 does not attack a13. So a13 is attacked by a1? Wait check: a1 → a14 (strong), not a13. So a13 is attacked by a14 and a1? Actually a1→a13? No. So a13 is attacked by a14 only? And a1? No. So a13 attacked by a14. Who defends? a1 attacks a14 (yes, strong a1→a14). So a1 defends a13 against a14. Also a13 attacked by a1? No. So all attacks on a13 are from a14, and a1 (in set) attacks a14 → defended.  
So {a1, a8, a13} is admissible. Can we add more?  
Try adding a16: a16 attacks a1? No. a1 attacks a16? No. a8 attacks a16? No. a13 attacks a16? No. a16 attacks a8? No. a16 attacks a13? No. Conflict-free.  
Defense for a16: a16 attacked by a15. Does anyone in set attack a15? a1 attacks a15? No. a8 attacks a15? No. a13 attacks a15? No. So not defended. So cannot add a16.  
Try adding a15: a15 attacks a16? Not relevant. a15 attacks anyone in set? a15→a16 only, so no conflict. But a15 attacked by a16. No one in set attacks a16? a1? No. a8? No. a13? No. So not defended.  
Try adding a2: a2 attacks a1 (strong) → conflict.  
Try adding a9: a9 attacks a8 (strong) → conflict.  
Try adding a3: a3 attacks a5, a5 attacks a3, but a3 attacks a1? No. a1 attacks a3 (strong) → conflict.  
Try adding a4: a1 attacks a4 (strong) → conflict.  
Try adding a5: a3 attacks a5? a3 not in set. a5 attacks a3? Not relevant. a5 attacks a1? No. a1 attacks a5? No. a8 attacks a5 (weak succeeds) → conflict.  
Try adding a6: a8 attacks a6 (weak succeeds) → conflict.  
Try adding a7: a13 attacks a7 (strong) → conflict.  
Try adding a10: a13 attacks a10 (strong) → conflict.  
Try adding a11: a16 not in set, so a11 not attacked by set? But a11 attacked by a16, but a16 not in set. a11 attacks anyone? No. So no conflict. But defense: a11 attacked by a16. No one in set attacks a16 → not defended.  
a12 similar.  
a14: a1 attacks a14 (strong) → conflict.  

So {a1, a8, a13} is maximal admissible.

Check {a1, a8, a13, a15}? a15 attacks a16, not in set. a15 attacked by a16. No one attacks a16 → not defended. So no.

Check {a1, a8, a13, a2}? conflict a2→a1.

Thus {a1, a8, a13} is one.

Check {a2, a9, a16}?  
a2 attacks a9? No. a9 attacks a2? No. a16 attacks a2? No. a2 attacks a16? No. a9 attacks a16? No. a16 attacks a9? No. Conflict-free.  
Defense:  
- a2 attacked by a8 → a9 attacks a8 (yes) → defended.  
- a9 attacked by a13 → a16 attacks a13? No → fails.

Check {a2, a9, a15}?  
a15 attacks a2? No. a2 attacks a15? No. a9 attacks a15? No. a15 attacks a9? No. Conflict-free.  
Defense:  
- a2 attacked by a8 → a9 attacks a8 → defended.  
- a9 attacked by a13 → a15 attacks a13? No → fails.

Check {a8, a13, a16}? Already checked defense fails for a13 (a1, a14 not attacked).

Check {a1, a13, a16}? Defense for a1: attacked by a2, no one attacks a2 → fails.

Check {a2, a8, a13}? a8 attacks a2 → conflict.

Check {a1, a9, a13}? a9 attacks a8? Not relevant. a1 attacked by a2 → no defense. Fails.

Check {a1, a8, a16}? a16 attacked by a15, no defense → fails.

Check {a1, a8, a15}? a15 attacked by a16, no defense → fails.

Check {a2, a9, a13}? a13 attacks a9 → conflict.

Check {a2, a9, a8}? a8 attacks a2 → conflict.

Check {a1, a8, a13} already found.

Check {a1, a8, a13, a?} no more.

Check {a15, a16}? a15 attacks a16 (strong) → conflict.

Check {a1, a8}? Not maximal because we can add a13.

Check {a8, a13}? Not maximal because we can add a1.

Check {a1, a13}? Not maximal because we can add a8.

Check {a16} and {a15} are maximal.

Check {a1, a8, a13} is maximal.

Check if {a2, a9} is maximal?  
a2 attacked by a8 → a9 attacks a8 → defended.  
a9 attacked by a13 → a2 attacks a13? No. So fails defense. So not admissible.

Check {a2, a9, a?} no.

Check {a1, a14}? conflict.

Check {a3, a5}? conflict.

Check {a7, a10, a13}? a13 attacks a7, a10 → conflict.

Check {a11, a12, a16}? a16 attacks a11, a12 → conflict.

Thus the maximal admissible sets are:  
{a16}, {a15}, {a1, a8, a13}.

```json
{
  "hierarchical_stable_extensions": [
    ["a1", "a8", "a13"],
    ["a15"],
    ["a16"]
  ]
}
```
```
