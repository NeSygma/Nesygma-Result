# Benchmark Report (SELECTOR): ASPBench - 27_queens_domination_hard

**Provider:** mistral2
**Model:** mistral-small-2603
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: none
**Duration:** 0.84s


 SELECTOR META EVALUATOR AGENT

 Query: # Problem Statement

Find the minimum number of queens required to dominate every square on a 9×9 chessboard. A queen dominates all squares in the same row, column, and diagonals (both directions).

## Instance Data

- Board size: 9×9 (rows 0-8, columns 0-8)
- Total squares: 81

## Constraints

1. **Each queen** occupies exactly one square on the board
2. **No restrictions** on queen placement (queens may attack each other)
3. **All 81 squares** must be dominated by at least one queen
4. A square is **dominated** if it lies in the same row, column, or diagonal as a queen
5. A queen **dominates itself** (the square it occupies)

## Objective

Find a solution that **minimizes** the number of queens placed on the board.

**Expected optimal value:** 5 queens

### Field Descriptions

- `queens`: Array of queen positions, where each position is `[row, col]` with both row and col in range 0-8

```json
{
    "solver_ranking": ["Z3", "CLINGO", "VAMPIRE"]
}
```

### TOKEN USAGE

  Input tokens:  1,442
  Output tokens: 29
  Total tokens:  1,471

COMPLETE

## Selector Final Answer

```json
```json
{
    "solver_ranking": ["Z3", "CLINGO", "VAMPIRE"]
}
```
```
