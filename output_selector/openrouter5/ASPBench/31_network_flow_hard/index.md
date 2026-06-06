# Benchmark Report (SELECTOR): ASPBench - 31_network_flow_hard

**Provider:** openrouter5
**Model:** deepseek/deepseek-v4-flash
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 8.64s


 SELECTOR META EVALUATOR AGENT

 Query: # Problem Statement

Find the maximum flow through a network from a source to a sink, subject to budgetary constraints and flow type balancing rules. Each edge has a capacity, cost per unit flow, and type (standard or premium). Priority nodes require at least 75% of their outgoing flow to be premium type, and globally, standard flow must be at least 50% of premium flow.

## Instance Data

**Network Structure:**
- **Nodes:** 1, 2, 3, 4, 5, 6, 7, 8
- **Source:** Node 1
- **Sink:** Node 8
- **Budget:** 100

**Edges (from, to, capacity, cost per unit, type):**
- (1, 2): capacity=10, cost=2, type=standard
- (1, 3): capacity=12, cost=4, type=premium
- (2, 4): capacity=8, cost=1, type=standard
- (2, 5): capacity=4, cost=3, type=premium
- (3, 4): capacity=5, cost=3, type=standard
- (3, 6): capacity=10, cost=5, type=premium
- (4, 7): capacity=10, cost=2, type=standard
- (5, 7): capacity=7, cost=4, type=premium
- (6, 8): capacity=12, cost=2, type=premium
- (7, 8): capacity=15, cost=1, type=standard

**Priority Nodes:** 3, 5 (require ≥75% outgoing premium flow)

## Constraints

1. **Capacity Constraint:** Flow on each edge must not exceed its capacity
2. **Flow Conservation:** For all intermediate nodes (not source/sink), incoming flow equals outgoing flow
3. **Budget Constraint:** Total cost (sum of flow × cost for all edges) must not exceed 100
4. **Priority Node Rule:** For priority nodes (3, 5), if there is incoming flow, at least 75% of outgoing flow must be premium type
5. **Flow Balancing:** Total standard flow across the network must be at least 50% of total premium flow

## Objective

Find a solution that **maximizes** the total flow from the source (node 1) to the sink (node 8).

**Expected maximum flow:** 12

### Field Descriptions

- `max_flow`: Integer representing the total flow from source to sink
- `flows`: Array of flow objects, one for each edge in the network. Each object must have:
  - `from`: Integer node ID
  - `to`: Integer node ID
  - `flow`: Integer flow value (0 to edge capacity)

This problem involves **numeric optimization** with **integer flows**, **budget constraints**, **percentage-based rules**, and **global flow balancing ratios**.  

- It requires **maximizing** a numeric value (total flow) under strict numeric constraints (capacity, cost ≤ 100, ≥75% premium at priority nodes, standard ≥ 50% of premium).  
- The structure is a **network flow** with **integer decision variables** per edge, arithmetic constraints, and an objective function.  
- There is no complex quantifier reasoning over categories, no recursive rule chaining, and no open-world entailment checking.  

**Z3** is the best fit because it handles integer variables, arithmetic constraints, optimization (maximize), and percentage/ratio conditions naturally via SMT with linear arithmetic.  

**CLINGO** could encode this but would struggle with the arithmetic grounding for the budget and ratio constraints, and optimization is less direct.  

**VAMPIRE** is unsuitable because it cannot handle integer arithmetic, optimization, or numeric constraints of this kind.  

```json
{
    "solver_ranking": ["Z3", "CLINGO", "VAMPIRE"]
}
```

### TOKEN USAGE

  Input tokens:  1,785
  Output tokens: 245
  Total tokens:  2,030

COMPLETE

## Selector Final Answer

```json
This problem involves **numeric optimization** with **integer flows**, **budget constraints**, **percentage-based rules**, and **global flow balancing ratios**.  

- It requires **maximizing** a numeric value (total flow) under strict numeric constraints (capacity, cost ≤ 100, ≥75% premium at priority nodes, standard ≥ 50% of premium).  
- The structure is a **network flow** with **integer decision variables** per edge, arithmetic constraints, and an objective function.  
- There is no complex quantifier reasoning over categories, no recursive rule chaining, and no open-world entailment checking.  

**Z3** is the best fit because it handles integer variables, arithmetic constraints, optimization (maximize), and percentage/ratio conditions naturally via SMT with linear arithmetic.  

**CLINGO** could encode this but would struggle with the arithmetic grounding for the budget and ratio constraints, and optimization is less direct.  

**VAMPIRE** is unsuitable because it cannot handle integer arithmetic, optimization, or numeric constraints of this kind.  

```json
{
    "solver_ranking": ["Z3", "CLINGO", "VAMPIRE"]
}
```
```
