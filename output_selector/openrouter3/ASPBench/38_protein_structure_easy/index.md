# Benchmark Report (SELECTOR): ASPBench - 38_protein_structure_easy

**Provider:** openrouter3
**Model:** xiaomi/mimo-v2-flash
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 1.66s


 SELECTOR META EVALUATOR AGENT

 Query: # Problem Statement

Fold a protein sequence on a 2D lattice to minimize energy using the simplified HP (Hydrophobic-Polar) model. In this model, hydrophobic residues (H) form favorable contacts when adjacent on the lattice (non-sequential neighbors), while polar residues (P) are neutral.

## Instance Data

Protein sequence (8 residues): **HPPHPPHH**

Where:
- **H** = Hydrophobic residue
- **P** = Polar residue

Energy model:
- Each H-H contact between non-sequential neighbors contributes **-1** energy
- Goal: minimize total energy

## Constraints

1. Each residue **must** be placed on a unique lattice point (self-avoiding walk)
2. Consecutive residues **must** be adjacent on the lattice (Manhattan distance = 1)
3. **All** 8 residues must be placed
4. **No** two residues can occupy the same coordinate

## Objective

Find a solution that **minimizes** the total energy by maximizing H-H contacts between non-sequential neighbors.

Expected optimal energy: **-3**

Where:
- `coordinates`: List of 8 coordinate pairs [x, y], one for each residue in sequence order
- `sequence`: The protein sequence (for verification)

{
    "solver_ranking": ["Z3", "CLINGO", "VAMPIRE"]
}

### TOKEN USAGE

  Input tokens:  1,454
  Output tokens: 24
  Total tokens:  1,478

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["Z3", "CLINGO", "VAMPIRE"]
}
```
