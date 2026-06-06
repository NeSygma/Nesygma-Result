# Benchmark Report (MCP): ASPBench - 55_recipe_planning_hard

**Provider:** openrouter6
**Model:** xiaomi/mimo-v2-flash
**Solver:** z3
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: high
**Duration:** 45.50s


 MCP Z3 AGENT - Symbolic Reasoning

### Query
# Problem Statement Plan the cooking of 4 recipes with shared resources, optimizing for minimal

total time while respecting resource constraints and inter-recipe dependencies. ## Instance Data **4
Recipes with Steps:** - **Roast Chicken:** - prep_chicken: 15 min, uses prep_area - bake_chicken: 50
min, uses oven - rest_chicken: 10 min, uses prep_area - **Vegetable Soup:** - chop_veg_soup: 20 min,
uses prep_area - simmer_stock: 30 min, uses stove - **Risotto:** - chop_onion: 5 min, uses prep_area
- cook_risotto: 25 min, uses stove - **Side Salad:** - wash_greens: 5 min, uses prep_area -
mix_dressing: 10 min, uses prep_area **Step Precedences (within each recipe):** - Roast Chicken:
prep_chicken → bake_chicken → rest_chicken - Vegetable Soup: chop_veg_soup → simmer_stock - Risotto:
chop_onion → cook_risotto - Side Salad: wash_greens → mix_dressing **Inter-Recipe Dependency:** -
The vegetable_soup's simmer_stock step produces veggie_stock, which is **required** by risotto's
cook_risotto step (simmer_stock must finish before cook_risotto starts) **Shared Resources:** -
**prep_area:** Capacity 2 (can be used by two tasks simultaneously) - **oven:** Capacity 1, requires
a 10-minute preheat task before any baking - **stove:** Capacity 1 **Special Tasks:** -
preheat_oven: 10 min, uses oven (must complete before any baking) ## Constraints 1. **All required
recipe steps** must be completed 2. **Step precedences** within each recipe must be respected 3.
**Inter-recipe dependency:** simmer_stock must finish before cook_risotto starts 4. **Resource
capacity:** prep_area can handle 2 concurrent tasks, oven and stove handle 1 task each 5. **Oven
preheating:** preheat_oven must complete before any bake_chicken step starts 6. **Task timing:**
Each task must run for its specified duration using the correct resource ## Objective Minimize the
total time (makespan) to complete all recipes. **Expected optimal value:** total_time=75 ## Output
Format The solution must be a JSON object with the following structure: ```json { "total_time": 75,
"schedule": [ { "recipe": "roast_chicken", "step": "prep_chicken", "start_time": 0, "end_time": 15,
"resource": "prep_area" }, { "task": "preheat_oven", "start_time": 5, "end_time": 15, "resource":
"oven" } ], "feasible": true } ``` **Field Descriptions:** - `total_time`: The makespan (latest
end_time across all tasks) - `schedule`: List of all tasks with their timing and resource allocation
- Recipe tasks include: `recipe`, `step`, `start_time`, `end_time`, `resource` - Special tasks
include: `task`, `start_time`, `end_time`, `resource` - `feasible`: Boolean indicating if solution
is valid

  - write_and_run_z3: Write Python code using Z3 to a file and run it immediately to get results.
We capture printed stdout and stderr from running the script.

## Iteration 1



### Thinking

- I need to translate this scheduling problem into Z3 constraints. This is a classic job shop scheduling with resource constraints and makespan minimization. I'll model each task as a variable with start time and duration, and enforce resource capacity constraints using cumulative constraints or explicit overlap constraints.
- First, I need to list all tasks:
- 1. Roast Chicken: - prep_chicken: 15 min, uses prep_area - bake_chicken: 50 min, uses oven - rest_chicken: 10 min, uses prep_area
- 2. Vegetable Soup: - chop_veg_soup: 20 min, uses prep_area - simmer_stock: 30 min, uses stove
- 3. Risotto: - chop_onion: 5 min, uses prep_area - cook_risotto: 25 min, uses stove
- 4. Side Salad: - wash_greens: 5 min, uses prep_area - mix_dressing: 10 min, uses prep_area
- Special tasks: - preheat_oven: 10 min, uses oven
- Precedences: - Roast Chicken: prep_chicken → bake_chicken → rest_chicken - Vegetable Soup: chop_veg_soup → simmer_stock - Risotto: chop_onion → cook_risotto - Side Salad: wash_greens → mix_dressing
- Inter-recipe dependency: simmer_stock must finish before cook_risotto starts.
- Resource capacities: - prep_area: capacity 2 (can handle 2 concurrent tasks) - oven: capacity 1 (plus preheat_oven must complete before any bake_chicken) - stove: capacity 1
- Objective: minimize total makespan.
- I'll use Z3's Optimize() for minimization. I'll create variables for start times of each task. Since durations are fixed, end times are start + duration.
- I need to model resource usage. For prep_area, there are 5 tasks using it: prep_chicken, rest_chicken, chop_veg_soup, chop_onion, wash_greens, mix_dressing. That's 6 tasks actually. Wait: prep_chicken, rest_chicken, chop_veg_soup, chop_onion, wash_greens, mix_dressing. Yes 6 tasks. Capacity 2 means at most 2 can overlap.
- For oven: preheat_oven and bake_chicken. Capacity 1 means they cannot overlap.
- For stove: simmer_stock and cook_risotto. Capacity 1 means they cannot overlap.
- I'll use the cumulative constraint or explicit pairwise non-overlap constraints. Since capacity is small, I can use pairwise constraints for each resource.
- Let me define tasks with unique identifiers. I'll create a list of tasks with their resource and duration.
- I'll write Z3 code to model this. Let's start with the script.




### TOKEN USAGE - Iteration 1

  Input tokens:  6,824
  Output tokens: 2,629
  Total tokens:  9,453

### Tool Call: write_and_run_z3

  Args: {
  "filename": "scheduling.py",
  "code": "from z3 import *\n\n# Define tasks with (name, duration, resource)\ntasks = [\n    # Roast Chicken\n    (\"prep_chicken\", 15, \"prep_area\"),\n    (\"bake_chicken\", 50, \"oven\"),\n    (\"rest_chicken\", 10, \"prep_area\"),\n    # Vegetable Soup\n    (\"chop_veg_soup\", 20, \"prep_area\"),\n    (\"simmer_stock\", 30, \"stove\"),\n    # Risotto\n    (\"chop_onion\", 5, \"prep_area\"),\n    (\"cook_risotto\", 25, \"stove\"),\n    # Side Salad\n    (\"wash_greens\", 5, \"prep_area\"),\n    (\"mix_dressing\", 10, \"prep_area\"),\n    # Special task\n    (\"preheat_oven\", 10, \"oven\"),\n]\n\n# Create start time variables (non-negative integers)\nstart = {}\nfor name, dur, res in tasks:\n    start[name] = Int(f\"start_{name}\")\n\n# Duration mapping\nduration = {name: dur for name, dur, res in tasks}\n\n# Resource mapping\nresource = {name: res for name, dur, res in tasks}\n\n# Precedence constraints\nsolver = Solver()\n\n# Roast Chicken: prep_chicken -> bake_chicken -> rest_chicken\nsolver.add(start[\"prep_chicken\"] + duration[\"prep_chicken\"] <= start[\"bake_chicken\"])\nsolver.add(start[\"bake_chicken\"] + duration[\"bake_chicken\"] <= start[\"rest_chicken\"])\n\n# Vegetable Soup: chop_veg_soup -> simmer_stock\nsolver.add(start[\"chop_veg_soup\"] + duration[\"chop_veg_soup\"] <= start[\"simmer_stock\"])\n\n# Risotto: chop_onion -> cook_risotto\nsolver.add(start[\"chop_onion\"] + duration[\"chop_onion\"] <= start[\"cook_risotto\"])\n\n# Side Salad: wash_greens -> mix_dressing\nsolver.add(start[\"wash_greens\"] + duration[\"wash_greens\"] <= start[\"mix_dressing\"])\n\n# Inter-recipe dependency: simmer_stock must finish before cook_risotto starts\nsolver.add(start[\"simmer_stock\"] + duration[\"simmer_stock\"] <= start[\"cook_risotto\"])\n\n# Oven preheating: preheat_oven must complete before any bake_chicken starts\nsolver.add(start[\"preheat_oven\"] + duration[\"preheat_oven\"] <= start[\"bake_chicken\"])\n\n# Resource capacity constraints\n# For each resource, ensure no two tasks overlap beyond capacity\n# We'll use pairwise non-overlap for tasks sharing the same resource\n# For prep_area (capacity 2), we need to ensure at most 2 tasks overlap.\n# Since capacity is 2, we can allow overlap but need to limit concurrent tasks.\n# We'll use cumulative constraint or explicit constraints.\n# Let's use explicit constraints for simplicity: for each pair of tasks using same resource,\n# they must not overlap if capacity is 1, but for capacity 2 we need to allow up to 2 overlaps.\n# We'll use a different approach: for each resource, we can use the cumulative constraint.\n# However, Z3's cumulative is not directly available in Python API; we can use a custom encoding.\n# For capacity 2, we can use a binary variable for each time slot? That's complex.\n# Instead, we can use the \"at most 2 tasks overlap\" constraint by ensuring that for any three tasks,\n# they cannot all overlap simultaneously. But that's O(n^3).\n# Better: use the cumulative constraint via the 'sum' of intervals.\n# Let's use the standard approach: for each resource, we can use the \"no overlap\" for capacity 1,\n# and for capacity 2 we can use a more general encoding.\n\n# Let's list tasks per resource:\nprep_area_tasks = [name for name, dur, res in tasks if res == \"prep_area\"]\noven_tasks = [name for name, dur, res in tasks if res == \"oven\"]\nstove_tasks = [name for name, dur, res in tasks if res == \"stove\"]\n\nprint(\"Prep area tasks:\", prep_area_tasks)\nprint(\"Oven tasks:\", oven_tasks)\nprint(\"Stove tasks:\", stove_tasks)\n\n# For oven (capacity 1) and stove (capacity 1), we can enforce pairwise non-overlap.\n# For prep_area (capacity 2), we need to allow up to 2 concurrent tasks.\n# We'll use a simple encoding: for each pair of prep_area tasks, we allow overlap,\n# but we must ensure that no three tasks overlap simultaneously.\n# We'll create a binary variable for each pair indicating if they overlap? That's messy.\n# Instead, we can use the \"cumulative\" constraint via the \"sum of heights\" approach.\n# Let's define for each task a height of 1, and capacity 2.\n# We can use the following encoding: for each time point, the sum of tasks active at that time <= 2.\n# But time is continuous; we can discretize at task start/end times.\n# Since all durations are integers, we can consider integer time points.\n# However, that could be large.\n\n# Alternative: use the \"no overlap\" for capacity 1, and for capacity 2 we can use a different method:\n# For each pair of tasks, we can allow overlap, but we need to ensure that for any three tasks,\n# they don't all overlap. We can add constraints for each triple.\n# Let's do that for prep_area (6 tasks). Number of triples = C(6,3)=20. That's manageable.\n\n# For each triple (i,j,k) of prep_area tasks, we ensure that not all three overlap.\n# Overlap condition: tasks i and j overlap if start_i < end_j and start_j < end_i.\n# We'll encode using Z3's Or of pairwise non-overlap.\n\n# Let's define end times\nend = {name: start[name] + duration[name] for name in start}\n\n# Helper function to check overlap between two tasks\ndef overlap(t1, t2):\n    # t1 and t2 overlap if start1 < end2 and start2 < end1\n    return And(start[t1] < end[t2], start[t2] < end[t1])\n\n# For oven tasks (capacity 1): ensure no overlap between any two oven tasks\nfor i in range(len(oven_tasks)):\n    for j in range(i+1, len(oven_tasks)):\n        solver.add(Not(overlap(oven_tasks[i], oven_tasks[j])))\n\n# For stove tasks (capacity 1): ensure no overlap between any two stove tasks\nfor i in range(len(stove_tasks)):\n    for j in range(i+1, len(stove_tasks)):\n        solver.add(Not(overlap(stove_tasks[i], stove_tasks[j])))\n\n# For prep_area tasks (capacity 2): ensure no triple overlap\n# For each triple (i,j,k), ensure that not all three overlap.\n# That is: Not(And(overlap(i,j), overlap(j,k), overlap(i,k)))\n# But we need to ensure that at most 2 overlap at any time.\n# Actually, the triple constraint ensures that there is no time where all three are active.\n# However, it's possible that three tasks overlap pairwise but not all three simultaneously?\n# If each pair overlaps, then there is a common intersection? Not necessarily.\n# For intervals, if each pair overlaps, then all three have a common intersection (Helly's theorem for intervals).\n# So triple overlap constraint is sufficient.\nfor i in range(len(prep_area_tasks)):\n    for j in range(i+1, len(prep_area_tasks)):\n        for k in range(j+1, len(prep_area_tasks)):\n            solver.add(Not(And(overlap(prep_area_tasks[i], prep_area_tasks[j]),\n                               overlap(prep_area_tasks[j], prep_area_tasks[k]),\n                               overlap(prep_area_tasks[i], prep_area_tasks[k]))))\n\n# Ensure all start times are non-negative\nfor name in start:\n    solver.add(start[name] >= 0)\n\n# Objective: minimize total makespan (max end time)\nmakespan = Int(\"makespan\")\nsolver.add(makespan >= end[name] for name in end)\n# We'll use Optimize for minimization\nopt = Optimize()\n# Transfer constraints from solver to opt\nfor c in solver.assertions():\n    opt.add(c)\nopt.add(makespan >= end[name] for name in end)\nopt.minimize(makespan)\n\n# Check\nresult = opt.check()\nif result == sat:\n    m = opt.model()\n    print(\"STATUS: sat\")\n    print(\"Optimal makespan:\", m.evaluate(makespan))\n    print(\"Schedule:\")\n    for name, dur, res in tasks:\n        st = m.evaluate(start[name])\n        et = m.evaluate(end[name])\n        print(f\"  {name}: start={st}, end={et}, resource={res}\")\n    # Also compute total_time\n    total_time = m.evaluate(makespan)\n    print(f\"total_time={total_time}\")\n    # Check feasibility\n    feasible = True\n    # Verify constraints (optional)\n    print(\"feasible=True\")\nelif result == unsat:\n    print(\"STATUS: unsat\")\n    print(\"RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)\")\nelse:\n    print(\"STATUS: unknown\")"
}

#### Result

[{'type': 'text', 'text': '{"status":"success","stdout":"Prep area tasks: [\'prep_chicken\', \'rest_chicken\', \'chop_veg_soup\', \'chop_onion\', \'wash_greens\', \'mix_dressing\']\\r\\nOven tasks: [\'bake_chicken\', \'preheat_oven\']\\r\\nStove tasks: [\'simmer_stock\', \'cook_risotto\']\\r\\nSTATUS: sat\\r\\nOptimal makespan: 75\\r\\nSchedule:\\r\\n  prep_chicken: start=0, end=15, resource=prep_area\\r\\n  bake_chicken: start=15, end=65, resource=oven\\r\\n  rest_chicken: start=65, end=75, resource=prep_area\\r\\n  chop_veg_soup: start=0, end=20, resource=prep_area\\r\\n  simmer_stock: start=20, end=50, resource=stove\\r\\n  chop_onion: start=20, end=25, resource=prep_area\\r\\n  cook_risotto: start=50, end=75, resource=stove\\r\\n  wash_greens: start=16, end=21, resource=prep_area\\r\\n  mix_dressing: start=21, end=31, resource=prep_area\\r\\n  preheat_oven: start=0, end=10, resource=oven\\r\\ntotal_time=75\\r\\nfeasible=True\\r\\n","stderr":null}', 'id': 'lc_c466df62-b8de-48b6-b673-8ffa26ccac53'}]


## Iteration 2



### Thinking

- First, the user has provided the original problem and the solver output. My role is to produce the final user-facing answer from the solver output, strictly adhering to the JSON format specified in the problem.
- From the solver output, I see:
- - Status: "sat" – meaning a satisfying model was found.
- - Optimal makespan: 75
- - Schedule details are provided with start and end times for each task.
- - total_time=75
- - feasible=True
- The output format required is a JSON object with:
- - "total_time": the makespan
- - "schedule": a list of tasks with their details
- - "feasible": boolean
- In the solver output, the schedule is listed with tasks like prep_chicken, bake_chicken, etc. I need to map this to the JSON structure.
- Looking at the JSON schema in the problem:
- - For recipe tasks: include "recipe", "step", "start_time", "end_time", "resource"
- - For special tasks: include "task", "start_time", "end_time", "resource"
- In the solver output, tasks are listed with names like "prep_chicken", which is a step for roast_chicken. Similarly, "preheat_oven" is a special task.
- I need to extract all tasks from the solver output and format them into the schedule list.
- From the solver output:
- - prep_chicken: start=0, end=15, resource=prep_area → this is a recipe task for roast_chicken, step prep_chicken
- - bake_chicken: start=15, end=65, resource=oven → recipe task for roast_chicken, step bake_chicken
- - rest_chicken: start=65, end=75, resource=prep_area → recipe task for roast_chicken, step rest_chicken
- - chop_veg_soup: start=0, end=20, resource=prep_area → recipe task for vegetable_soup, step chop_veg_soup
- - simmer_stock: start=20, end=50, resource=stove → recipe task for vegetable_soup, step simmer_stock
- - chop_onion: start=20, end=25, resource=prep_area → recipe task for risotto, step chop_onion
- - cook_risotto: start=50, end=75, resource=stove → recipe task for risotto, step cook_risotto
- - wash_greens: start=16, end=21, resource=prep_area → recipe task for side_salad, step wash_greens
- - mix_dressing: start=21, end=31, resource=prep_area → recipe task for side_salad, step mix_dressing
- - preheat_oven: start=0, end=10, resource=oven → special task
- Now, I need to map these to the JSON structure.
- For recipe tasks, I need to specify "recipe" and "step". From the task names, I can infer the recipe:
- - prep_chicken, bake_chicken, rest_chicken → roast_chicken
- - chop_veg_soup, simmer_stock → vegetable_soup
- - chop_onion, cook_risotto → risotto
- - wash_greens, mix_dressing → side_salad
- For special tasks, use "task" instead of "recipe" and "step".
- In the JSON example, for special tasks, it's shown as:
- {
- "task": "preheat_oven",
- "start_time": 5,
- "end_time": 15,
- "resource": "oven"
- }
- But in the solver output, preheat_oven is from start=0 to end=10.
- I need to use the times from the solver output.
- Also, in the schedule list, I should include all tasks in the order they are listed or any order, but probably in the order given or sorted by start time. The problem doesn't specify order, so I can list them as per solver output or logically.
- The solver output lists them in a certain order, but I can organize them for clarity.
- Now, for the JSON output, I need to ensure it's valid JSON.
- First, total_time: 75
- feasible: true (from solver output, feasible=True)
- schedule: a list of objects.
- Let me list all tasks with their details:
- 1. prep_chicken: recipe="roast_chicken", step="prep_chicken", start_time=0, end_time=15, resource="prep_area"
- 2. bake_chicken: recipe="roast_chicken", step="bake_chicken", start_time=15, end_time=65, resource="oven"
- 3. rest_chicken: recipe="roast_chicken", step="rest_chicken", start_time=65, end_time=75, resource="prep_area"
- 4. chop_veg_soup: recipe="vegetable_soup", step="chop_veg_soup", start_time=0, end_time=20, resource="prep_area"
- 5. simmer_stock: recipe="vegetable_soup", step="simmer_stock", start_time=20, end_time=50, resource="stove"
- 6. chop_onion: recipe="risotto", step="chop_onion", start_time=20, end_time=25, resource="prep_area"
- 7. cook_risotto: recipe="risotto", step="cook_risotto", start_time=50, end_time=75, resource="stove"
- 8. wash_greens: recipe="side_salad", step="wash_greens", start_time=16, end_time=21, resource="prep_area"
- 9. mix_dressing: recipe="side_salad", step="mix_dressing", start_time=21, end_time=31, resource="prep_area"
- 10. preheat_oven: task="preheat_oven", start_time=0, end_time=10, resource="oven"
- In the JSON, for recipe tasks, use "recipe" and "step"; for special tasks, use "task".
- Now, I need to output this as a JSON object.
- The problem says: "Output ONLY a valid JSON object. No conversational filler, no markdown text outside the JSON."
- So, my response should be just the JSON.
- Also, from the solver output, status is "sat", which means a satisfying model was found, and it's optimal with makespan 75.
- Now, construct the JSON.
- First, total_time: 75
- feasible: true
- schedule: [ list of tasks ]
- I should list the tasks in a logical order, perhaps by start time or by recipe. But since the problem doesn't specify, I can use the order from solver output or sort by start time.
- In the solver output, the schedule is listed in a certain order, but for JSON, I can list them as I have above.
- To make it neat, I'll list them in the order of the solver output's schedule listing.
- From solver output:
- Schedule:
- prep_chicken: start=0, end=15, resource=prep_area
- bake_chicken: start=15, end=65, resource=oven
- rest_chicken: start=65, end=75, resource=prep_area
- chop_veg_soup: start=0, end=20, resource=prep_area
- simmer_stock: start=20, end=50, resource=stove
- chop_onion: start=20, end=25, resource=prep_area
- cook_risotto: start=50, end=75, resource=stove
- wash_greens: start=16, end=21, resource=prep_area
- mix_dressing: start=21, end=31, resource=prep_area
- preheat_oven: start=0, end=10, resource=oven
- I can use this order for the schedule list.
- Now, for each, format as per JSON schema.
- For prep_chicken: it's a recipe task, so { "recipe": "roast_chicken", "step": "prep_chicken", "start_time": 0, "end_time": 15, "resource": "prep_area" }
- Similarly for others.
- For preheat_oven: { "task": "preheat_oven", "start_time": 0, "end_time": 10, "resource": "oven" }
- In the JSON example, for special tasks, it's "task" instead of "recipe" and "step".
- Now, write the JSON.
- Ensure that all field names are as specified: "start_time", "end_time", etc.
- In the problem, for recipe tasks, it's "start_time" and "end_time", and for special tasks, same.
- Now, compile the schedule list.
- I'll list them in the order from solver output, but since preheat_oven is listed last in the output, but it starts at 0, I can keep the order as is.
- To be consistent, I'll use the order from the solver output's schedule listing.
- So, schedule list:
- 1. prep_chicken as recipe task
- 2. bake_chicken as recipe task
- 3. rest_chicken as recipe task
- 4. chop_veg_soup as recipe task
- 5. simmer_stock as recipe task
- 6. chop_onion as recipe task
- 7. cook_risotto as recipe task
- 8. wash_greens as recipe task
- 9. mix_dressing as recipe task
- 10. preheat_oven as special task
- Now, for the JSON object.
- Also, in the solver output, it says "feasible=True", so I'll use true in JSON (lowercase).
- Now, write the JSON.


{
  "total_time": 75,
  "schedule": [
    {
      "recipe": "roast_chicken",
      "step": "prep_chicken",
      "start_time": 0,
      "end_time": 15,
      "resource": "prep_area"
    },
    {
      "recipe": "roast_chicken",
      "step": "bake_chicken",
      "start_time": 15,
      "end_time": 65,
      "resource": "oven"
    },
    {
      "recipe": "roast_chicken",
      "step": "rest_chicken",
      "start_time": 65,
      "end_time": 75,
      "resource": "prep_area"
    },
    {
      "recipe": "vegetable_soup",
      "step": "chop_veg_soup",
      "start_time": 0,
      "end_time": 20,
      "resource": "prep_area"
    },
    {
      "recipe": "vegetable_soup",
      "step": "simmer_stock",
      "start_time": 20,
      "end_time": 50,
      "resource": "stove"
    },
    {
      "recipe": "risotto",
      "step": "chop_onion",
      "start_time": 20,
      "end_time": 25,
      "resource": "prep_area"
    },
    {
      "recipe": "risotto",
      "step": "cook_risotto",
      "start_time": 50,
      "end_time": 75,
      "resource": "stove"
    },
    {
      "recipe": "side_salad",
      "step": "wash_greens",
      "start_time": 16,
      "end_time": 21,
      "resource": "prep_area"
    },
    {
      "recipe": "side_salad",
      "step": "mix_dressing",
      "start_time": 21,
      "end_time": 31,
      "resource": "prep_area"
    },
    {
      "task": "preheat_oven",
      "start_time": 0,
      "end_time": 10,
      "resource": "oven"
    }
  ],
  "feasible": true
}

### TOKEN USAGE - Iteration 2

  Input tokens:  1,645
  Output tokens: 2,566
  Total tokens:  4,211

TOKEN USAGE SUMMARY
  Total input tokens:  8,469
  Total output tokens: 5,195
  Total tokens:        13,664

COMPLETE

## Final Answer

```json
{
  "total_time": 75,
  "schedule": [
    {
      "recipe": "roast_chicken",
      "step": "prep_chicken",
      "start_time": 0,
      "end_time": 15,
      "resource": "prep_area"
    },
    {
      "recipe": "roast_chicken",
      "step": "bake_chicken",
      "start_time": 15,
      "end_time": 65,
      "resource": "oven"
    },
    {
      "recipe": "roast_chicken",
      "step": "rest_chicken",
      "start_time": 65,
      "end_time": 75,
      "resource": "prep_area"
    },
    {
      "recipe": "vegetable_soup",
      "step": "chop_veg_soup",
      "start_time": 0,
      "end_time": 20,
      "resource": "prep_area"
    },
    {
      "recipe": "vegetable_soup",
      "step": "simmer_stock",
      "start_time": 20,
      "end_time": 50,
      "resource": "stove"
    },
    {
      "recipe": "risotto",
      "step": "chop_onion",
      "start_time": 20,
      "end_time": 25,
      "resource": "prep_area"
    },
    {
      "recipe": "risotto",
      "step": "cook_risotto",
      "start_time": 50,
      "end_time": 75,
      "resource": "stove"
    },
    {
      "recipe": "side_salad",
      "step": "wash_greens",
      "start_time": 16,
      "end_time": 21,
      "resource": "prep_area"
    },
    {
      "recipe": "side_salad",
      "step": "mix_dressing",
      "start_time": 21,
      "end_time": 31,
      "resource": "prep_area"
    },
    {
      "task": "preheat_oven",
      "start_time": 0,
      "end_time": 10,
      "resource": "oven"
    }
  ],
  "feasible": true
}
```
