# Benchmark Report (SELECTOR): ASPBench - 64_social_network_influence_hard

**Provider:** openrouter2
**Model:** openai/gpt-oss-20b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 4.81s


 SELECTOR META EVALUATOR AGENT

 Query: # Problem Statement

Select a set of seed users within budget constraints to maximize influence spread through a social network. Users become activated when incoming influence from already-activated neighbors meets their activation threshold, creating a cascade effect. The objective combines reach (activated users), key user activation bonus, and cost efficiency.

## Instance Data

```python
{
  "users": [
    {"id": "u1", "cost": 250, "category": "influencer", "activation_threshold": 10},
    {"id": "u2", "cost": 80, "category": "regular", "activation_threshold": 60},
    {"id": "u3", "cost": 70, "category": "regular", "activation_threshold": 90},
    {"id": "u4", "cost": 150, "category": "expert", "activation_threshold": 100},
    {"id": "u5", "cost": 90, "category": "regular", "activation_threshold": 70},
    {"id": "u6", "cost": 200, "category": "influencer", "activation_threshold": 120},
    {"id": "u7", "cost": 300, "category": "influencer", "activation_threshold": 10},
    {"id": "u8", "cost": 110, "category": "regular", "activation_threshold": 40},
    {"id": "u9", "cost": 60, "category": "regular", "activation_threshold": 80},
    {"id": "u10", "cost": 220, "category": "expert", "activation_threshold": 150},
    {"id": "u11", "cost": 50, "category": "regular", "activation_threshold": 50},
    {"id": "u12", "cost": 130, "category": "regular", "activation_threshold": 90},
    {"id": "u13", "cost": 280, "category": "influencer", "activation_threshold": 10},
    {"id": "u14", "cost": 85, "category": "regular", "activation_threshold": 60},
    {"id": "u15", "cost": 180, "category": "expert", "activation_threshold": 10},
    {"id": "u16", "cost": 95, "category": "regular", "activation_threshold": 50},
    {"id": "u17", "cost": 40, "category": "regular", "activation_threshold": 100},
    {"id": "u18", "cost": 190, "category": "expert", "activation_threshold": 110},
    {"id": "u19", "cost": 210, "category": "influencer", "activation_threshold": 130},
    {"id": "u20", "cost": 75, "category": "regular", "activation_threshold": 70},
    {"id": "u21", "cost": 100, "category": "expert", "activation_threshold": 80},
    {"id": "u22", "cost": 120, "category": "regular", "activation_threshold": 10},
    {"id": "u23", "cost": 140, "category": "regular", "activation_threshold": 120},
    {"id": "u24", "cost": 160, "category": "expert", "activation_threshold": 90},
    {"id": "u25", "cost": 240, "category": "influencer", "activation_threshold": 10}
  ],
  "connections": [
    {"from": "u1", "to": "u2", "strength": 70},
    {"from": "u1", "to": "u5", "strength": 50},
    {"from": "u7", "to": "u8", "strength": 50},
    {"from": "u7", "to": "u9", "strength": 30},
    {"from": "u15", "to": "u16", "strength": 60},
    {"from": "u22", "to": "u5", "strength": 30},
    {"from": "u2", "to": "u3", "strength": 40},
    {"from": "u8", "to": "u3", "strength": 50},
    {"from": "u8", "to": "u9", "strength": 60}
  ],
  "budget": {"total": 1000, "influencer": 600},
  "max_seeds": 5,
  "required_seed_category": "expert"
}
```

## Constraints

1. **Total cost** of selected seeds must not exceed the budget (1000)
2. **Maximum seeds**: Select at most 5 users as initial seeds
3. **Cascade activation**: A user becomes activated if:
   - They are selected as a seed, OR
   - The sum of influence strengths from already-activated neighbors meets or exceeds their activation threshold
4. **Key user**: The first user with category "expert" (u4) serves as the key user for bonus scoring

## Objective

Find a solution that **maximizes** the composite score:
- 10 points per activated user
- 50 points if the key user (u4) is activated

**Expected optimal solution**: Maximum score with total_cost=1000 (uses full budget)

### Field Descriptions

- `selected_seeds`: Array of user IDs chosen as seeds
- `activated_users`: Array of all activated user IDs (seeds + cascade)
- `total_cost`: Integer, total cost of selected seeds
- `total_activated_count`: Integer, count of activated users
- `key_user_activated`: Boolean, whether key user (u4) was activated
- `final_score`: Integer, composite score value


### Thinking

- We need to rank solvers: VAMPIRE, CLINGO, Z3. Problem: selecting seed users within budget constraints to maximize influence spread. It's a combinatorial optimization with constraints: budget, max seeds, cascade activation based on thresholds and strengths. We need to find optimal set maximizing score. This is a combinatorial optimization problem with numeric constraints and cascade logic. We need to model cascade activation: if sum of influence strengths from activated neighbors >= threshold. This is a dynamic process. We need to find seeds that maximize final activated set. This is akin to influence maximization with budget constraints. It's a combinatorial optimization problem with constraints and objective. We need to find best set. This is a typical NP-hard problem. We need solver that can handle combinatorial search with constraints and objective. CLINGO is good for combinatorial search, but cascade activation logic may be complex. CLINGO can handle recursion and constraints, but cascade logic may require iterative propagation. But we can encode as rules: activated(X) :- seed(X). activated(X) :- activated(Y), strength(Y,X) >= threshold(X). But threshold is numeric. CLINGO can handle numeric constraints? It can handle arithmetic with integers, but not real numbers? It can handle integer arithmetic. Strengths are integers. Activation threshold is integer. So we can encode: activated(X) :- activated(Y), strength(Y,X) >= threshold(X). But we need to sum strengths from all activated neighbors. That requires sum of strengths. CLINGO can handle aggregates (#sum). So we can encode: activated(X) :- #sum{S : activated(Y), strength(Y,X,S)} >= threshold(X). That is possible. So CLINGO can encode cascade logic. Also budget constraints: sum of costs <= 1000. Max seeds <=5. Also influencer budget: influencer cost <=600. We can encode constraints. Objective: maximize score: 10 per activated user + 50 if u4 activated. CLINGO can optimize with #maximize. So CLINGO is suitable.
- Z3 is also suitable: we can encode variables for each user: seed boolean, activated boolean. Constraints: activated = seed or sum of strengths from activated neighbors >= threshold. This is a bit tricky because it's a recursive definition. But we can encode as implication: if activated and not seed, then sum of strengths from activated neighbors >= threshold. But we also need to ensure that if sum >= threshold, then activated. That is a bi-conditional. We can encode as: activated -> (seed or sum >= threshold). And (seed or sum >= threshold) -> activated. But sum uses activated variables of neighbors. This is a linear constraint with boolean variables. We can encode with big-M or use cardinality constraints. But we need to encode sum of strengths from activated neighbors. That is linear: sum_{neighbors} strength * activated_neighbor >= threshold * activated. But we need to ensure that if activated, then sum >= threshold. But if not activated, no constraint. But we also need to ensure that if sum >= threshold, then activated. That is: sum >= threshold -> activated. That can be encoded as: sum >= threshold <= activated. But we need to handle threshold as integer. This is linear. So Z3 can encode. Also budget constraints: sum cost <= 1000. Max seeds <=5. Also influencer budget <=600. Also objective: maximize 10*activated + 50*activated(u4). Z3 can optimize. So Z3 is also suitable.
- VAMPIRE is for first-order logic entailment, not optimization. So VAMPIRE is least suitable.
- Between CLINGO and Z3: Which is more suitable? CLINGO is good for combinatorial search with constraints and optimization. Z3 is also good for optimization with linear constraints. The cascade logic is a bit complex but can be encoded. CLINGO might be easier to encode with aggregates. But Z3 can handle linear constraints. The problem is small (25 users). So both can solve. But ranking: CLINGO might be more natural for combinatorial search with constraints and recursion. Z3 is also good. Which is more suitable? The problem is a combinatorial optimization with constraints and objective. Both can handle. But CLINGO is specifically designed for combinatorial search and optimization. Z3 is also good but more for arithmetic constraints. The cascade logic uses sum of strengths from activated neighbors. That is a sum of weighted booleans. Z3 can handle that. But CLINGO can handle aggregates. Which is more natural? I'd rank CLINGO as most suitable, Z3 second, VAMPIRE least.
- Thus final ranking: ["CLINGO", "Z3", "VAMPIRE"]


{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}

### TOKEN USAGE

  Input tokens:  2,497
  Output tokens: 1,000
  Total tokens:  3,497

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}
```
