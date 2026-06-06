# Benchmark Report (SYSTEM1): ASPBench - 33_independent_set_hard

**Provider:** xiaomi
**Model:** mimo-v2.5-pro
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 55.28s


 SYSTEM 1 PURE REASONING AGENT

 Query: # Problem Statement

Find the maximum independent set in a graph where vertices have attributes and must satisfy additional constraints. An independent set is a set of vertices with no edges between them. Each vertex has a **type** ('core', 'support', or 'peripheral') and a **zone** (1, 2, or 3).

## Instance Data

**Vertices:** 1 through 24

**Zones:**
- Zone 1: vertices 1-8
- Zone 2: vertices 9-16
- Zone 3: vertices 17-24

**Types:**
- Core vertices: 1, 9, 17
- Support vertices: 2, 3, 10, 11, 18, 19
- Peripheral vertices: 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 20, 21, 22, 23, 24

**Edges:**
(1,2), (1,4), (1,10), (1,17), (2,5), (2,9), (3,6), (4,7), (5,8), (6,7), (8,16), (8,24), (9,10), (9,12), (9,17), (10,14), (11,15), (12,16), (13,14), (16,24), (17,18), (17,20), (18,19), (18,21), (19,22), (20,23), (21,24)

## Constraints

1. **Standard Independence:** No two vertices in the set can be connected by an edge.
2. **Core Count Limit:** The set can contain **at most** two core vertices.
3. **Core-Support Dependency:** For every core vertex included in the set, **at least** one support vertex from the **same zone** must also be included.
4. **Conditional Zone Exclusion:** If the set contains any peripheral vertex from zone 1, then it **cannot** contain any vertex from zone 3.
5. **Peripheral Headcount Rule:** The total number of peripheral vertices in the set **must not exceed** the total number of core vertices in the set.

## Objective

Find a solution that **maximizes** the size of the independent set.

**Expected maximum size: 7**

## Output Format

The solution must be a JSON object with the following structure:

```json
{
  "independent_set": [1, 3, 9, 11, 13],
  "size": 5,
  "core_vertices": [1, 9],
  "support_vertices": [3, 11],
  "peripheral_vertices": [13],
  "core_count": 2,
  "support_count": 2,
  "peripheral_count": 1
}
```

### Field Descriptions

- `independent_set`: Array of vertex numbers in the independent set (sorted)
- `size`: Total number of vertices in the set
- `core_vertices`: Array of core vertices in the set (sorted)
- `support_vertices`: Array of support vertices in the set (sorted)
- `peripheral_vertices`: Array of peripheral vertices in the set (sorted)
- `core_count`: Number of core vertices in the set
- `support_count`: Number of support vertices in the set
- `peripheral_count`: Number of peripheral vertices in the set


Return your final answer in JSON format.

I need to find the maximum independent set of size 7 that satisfies all the constraints.

Let me analyze the graph structure:

**Zones:**
- Zone 1: vertices 1-8
- Zone 2: vertices 9-16
- Zone 3: vertices 17-24

**Types:**
- Core: 1, 9, 17
- Support: 2, 3, 10, 11, 18, 19
- Peripheral: 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 20, 21, 22, 23, 24

**Edges:**
(1,2), (1,4), (1,10), (1,17), (2,5), (2,9), (3,6), (4,7), (5,8), (6,7), (8,16), (8,24), (9,10), (9,12), (9,17), (10,14), (11,15), (12,16), (13,14), (16,24), (17,18), (17,20), (18,19), (18,21), (19,22), (20,23), (21,24)

Let me think about the constraints:
1. Standard independence
2. At most 2 core vertices
3. Each core vertex needs at least one support vertex from the same zone
4. If any peripheral from zone 1 is included, no zone 3 vertices
5. Peripheral count ≤ core count

Let me try to find a solution with 2 core vertices.

**Option: Include cores 1 and 9**
- Core 1 (zone 1) needs support from zone 1: 2 or 3
- Core 9 (zone 2) needs support from zone 2: 10 or 11

Let me try: cores {1, 9}, supports {3, 11}

Check independence:
- 1 and 3: no edge ✓
- 1 and 11: no edge ✓
- 9 and 3: no edge ✓
- 9 and 11: no edge ✓
- 3 and 11: no edge ✓

Now I need peripheral vertices. Peripheral count ≤ core count = 2, so at most 2 peripherals.

Available peripherals (not adjacent to {1, 3, 9, 11}):
- 1 is adjacent to: 2, 4, 10, 17
- 3 is adjacent to: 6
- 9 is adjacent to: 10, 12, 17
- 11 is adjacent to: 15

So excluded: 2, 4, 6, 10, 12, 15, 17

Available peripherals: 5, 7, 8, 13, 14, 16, 20, 21, 22, 23, 24

Check edges among these:
- (5,8): edge
- (8,16): edge
- (8,24): edge
- (13,14): edge
- (16,24): edge
- (20,23): edge
- (21,24): edge

I need 2 peripherals with no edge between them and satisfying zone constraint.

If I pick from zone 1 peripherals: 5, 7, 8
If I pick any zone 1 peripheral, I can't have zone 3 vertices.

Let me try without zone 1 peripherals to keep zone 3 options open.

From zone 2: 13, 14, 16
From zone 3: 20, 21, 22, 23, 24

Pick 13 and 22: no edge between them ✓
- 13 not adjacent to {1,3,9,11} ✓
- 22 not adjacent to {1,3,9,11} ✓
- 22 not adjacent to 13 ✓

Set: {1, 3, 9, 11, 13, 22} = size 6

Can I add one more? Peripheral count would be 3 > core count 2. Violates constraint 5.

So with 2 cores, max peripherals = 2, giving total = 2 + 2 + 2 = 6.

**Option: Include cores 1 and 17**
- Core 1 (zone 1) needs support from zone 1: 2 or 3
- Core 17 (zone 3) needs support from zone 3: 18 or 19

Try: cores {1, 17}, supports {3, 18}

Check independence:
- 1 and 3: no edge ✓
- 1 and 18: no edge ✓
- 17 and 3: no edge ✓
- 17 and 18: edge! ✗

Try: cores {1, 17}, supports {3, 19}

- 17 and 19: no edge ✓
- 1 and 19: no edge ✓
- 3 and 19: no edge ✓
- 3 and 17: no edge ✓

Excluded by {1, 3, 17, 19}: 2, 4, 6, 10, 18, 20, 22

Available peripherals: 5, 7, 8, 12, 13, 14, 15, 16, 21, 23, 24

Peripheral count ≤ 2.

If I pick zone 1 peripheral, no zone 3 vertices allowed.

Pick 5 and 13: no edge ✓
- 5 not adjacent to {1,3,17,19} ✓
- 13 not adjacent to {1,3,17,19} ✓

Set: {1, 3, 5, 13, 17, 19} = size 6

Can I add one more peripheral? No, would exceed core count.

**Option: Include cores 9 and 17**
- Core 9 (zone 2) needs support from zone 2: 10 or 11
- Core 17 (zone 3) needs support from zone 3: 18 or 19

Try: cores {9, 17}, supports {11, 19}

Check independence:
- 9 and 11: no edge ✓
- 9 and 19: no edge ✓
- 17 and 11: no edge ✓
- 17 and 19: no edge ✓
- 11 and 19: no edge ✓

Excluded by {9, 11, 17, 19}: 2, 10, 12, 15, 18, 20, 22

Available peripherals: 4, 5, 6, 7, 8, 13, 14, 16, 21, 23, 24

Peripheral count ≤ 2.

If I pick zone 1 peripheral, no zone 3 vertices.

Pick 4 and 13: no edge ✓
- 4 not adjacent to {9,11,17,19} ✓
- 13 not adjacent to {9,11,17,19} ✓

Set: {4, 9, 11, 13, 17, 19} = size 6

Hmm, still 6. Let me think differently.

**What if I use only 1 core vertex?**
Then peripheral count ≤ 1.
Total = 1 + support + peripheral ≤ 1 + support + 1

With 1 core, I need at least 1 support from same zone. So minimum 2 vertices from core+support.

To reach 7, I'd need 5 more vertices, but only 1 can be peripheral. So I'd need 4 more support vertices? But support vertices are limited and may have edges.

Actually wait - the constraint says peripheral count ≤ core count. If core count = 1, peripheral count ≤ 1. But I can have as many support vertices as I want (as long as independent).

Let me reconsider. With 2 cores, I can have 2 peripherals. Total = 2 cores + support + 2 peripherals.

To maximize, I want many support vertices. Let me check if I can include more support vertices.

**Try: cores {1, 9}, supports {3, 11}**
Can I add more support vertices? Other supports: 2, 10, 18, 19
- 2: adjacent to 1 (edge (1,2)) ✗
- 10: adjacent to 1 (edge (1,10)) and 9 (edge (9,10)) ✗
- 18: not adjacent to 1, 3, 9, 11 ✓
- 19: not adjacent to 1, 3, 9, 11 ✓
- 18 and 19: edge (18,19) ✗

So I can add one of {18, 19}. Let's add 18.

Set so far: {1, 3, 9, 11, 18}

Now peripherals ≤ 2. Available peripherals not adjacent to any of {1, 3, 9, 11, 18}:
- 1 adj: 2, 4, 10, 17
- 3 adj: 6
- 9 adj: 10, 12, 17
- 11 adj: 15
- 18 adj: 17, 19, 21

Excluded: 2, 4, 6, 10, 12, 15, 17, 19, 21

Available peripherals: 5, 7, 8, 13, 14, 16, 20, 22, 23, 24

Check edges among these:
- (5,8): edge
- (8,16): edge
- (8,24): edge
- (13,14): edge
- (16,24): edge
- (20,23): edge

I need 2 peripherals with no edge between them.

If I pick zone 1 peripheral (5, 7, or 8), no zone 3 vertices allowed.

Pick 5 and 13: no edge ✓
- 5 not adjacent to {1,3,9,11,18} ✓
- 13 not adjacent to {1,3,9,11,18} ✓

Set: {1, 3, 5, 9, 11, 13, 18} = size 7!

Let me verify all constraints:

**Independence check:**
- 1-3: no edge ✓
- 1-5: no edge ✓
- 1-9: no edge ✓
- 1-11: no edge ✓
- 1-13: no edge ✓
- 1-18: no edge ✓
- 3-5: no edge ✓
- 3-9: no edge ✓
- 3-11: no edge ✓
- 3-13: no edge ✓
- 3-18: no edge ✓
- 5-9: no edge ✓
- 5-11: no edge ✓
- 5-13: no edge ✓
- 5-18: no edge ✓
- 9-11: no edge ✓
- 9-13: no edge ✓
- 9-18: no edge ✓
- 11-13: no edge ✓
- 11-18: no edge ✓
- 13-18: no edge ✓

All good! ✓

**Constraint 2: Core count limit** - cores are {1, 9}, count = 2 ≤ 2 ✓

**Constraint 3: Core-Support Dependency**
- Core 1 (zone 1) → support 3 (zone 1) ✓
- Core 9 (zone 2) → support 11 (zone 2) ✓

**Constraint 4: Conditional Zone Exclusion**
- Peripheral from zone 1: vertex 5 (zone 1) is included
- Zone 3 vertices: vertex 18 is in zone 3!
- This violates constraint 4! ✗

So this doesn't work. I need to either:
1. Not include any zone 1 peripheral, or
2. Not include any zone 3 vertex

Let me try without zone 1 peripherals.

Set: {1, 3, 9, 11, 18} + peripherals from zone 2 or 3 only.

Available peripherals (not adjacent to {1,3,9,11,18}, not zone 1):
- Zone 2: 13, 14, 16
- Zone 3: 20, 22, 23, 24

Edges: (13,14), (16,24), (20,23)

Pick 13 and 22: no edge ✓
- 13 not adjacent to any in set ✓
- 22 not adjacent to any in set ✓

Set: {1, 3, 9, 11, 13, 18, 22} = size 7

**Verify all constraints:**

**Independence:**
- 1-3: no edge ✓
- 1-9: no edge ✓
- 1-11: no edge ✓
- 1-13: no edge ✓
- 1-18: no edge ✓
- 1-22: no edge ✓
- 3-9: no edge ✓
- 3-11: no edge ✓
- 3-13: no edge ✓
- 3-18: no edge ✓
- 3-22: no edge ✓
- 9-11: no edge ✓
- 9-13: no edge ✓
- 9-18: no edge ✓
- 9-22: no edge ✓
- 11-13: no edge ✓
- 11-18: no edge ✓
- 11-22: no edge ✓
- 13-18: no edge ✓
- 13-22: no edge ✓
- 18-22: no edge ✓

All independent ✓

**Constraint 2:** Core count = 2 ≤ 2 ✓

**Constraint 3:** 
- Core 1 (zone 1) → support 3 (zone 1) ✓
- Core 9 (zone 2) → support 11 (zone 2) ✓

**Constraint 4:** No peripheral from zone 1 included (13 is zone 2, 22 is zone 3). ✓

**Constraint 5:** Peripheral count = 2 (vertices 13, 22) ≤ core count = 2 ✓

This works! Size = 7.

Let me verify the types:
- Core: 1, 9 ✓
- Support: 3, 11, 18 ✓
- Peripheral: 13, 22 ✓

Wait, 18 is a support vertex. Let me double-check: Support vertices are 2, 3, 10, 11, 18, 19. Yes, 18 is support ✓.

So the solution is:
- independent_set: [1, 3, 9, 11, 13, 18, 22]
- size: 7
- core_vertices: [1, 9]
- support_vertices: [3, 11, 18]
- peripheral_vertices: [13, 22]
- core_count: 2
- support_count: 3
- peripheral_count: 2

```json
{
  "independent_set": [1, 3, 9, 11, 13, 18, 22],
  "size": 7,
  "core_vertices": [1, 9],
  "support_vertices": [3, 11, 18],
  "peripheral_vertices": [13, 22],
  "core_count": 2,
  "support_count": 3,
  "peripheral_count": 2
}
```

### TOKEN USAGE

  Input tokens:  861
  Output tokens: 3,825
  Total tokens:  4,686

COMPLETE

## System 1 Final Answer

```json
I need to find the maximum independent set of size 7 that satisfies all the constraints.

Let me analyze the graph structure:

**Zones:**
- Zone 1: vertices 1-8
- Zone 2: vertices 9-16
- Zone 3: vertices 17-24

**Types:**
- Core: 1, 9, 17
- Support: 2, 3, 10, 11, 18, 19
- Peripheral: 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 20, 21, 22, 23, 24

**Edges:**
(1,2), (1,4), (1,10), (1,17), (2,5), (2,9), (3,6), (4,7), (5,8), (6,7), (8,16), (8,24), (9,10), (9,12), (9,17), (10,14), (11,15), (12,16), (13,14), (16,24), (17,18), (17,20), (18,19), (18,21), (19,22), (20,23), (21,24)

Let me think about the constraints:
1. Standard independence
2. At most 2 core vertices
3. Each core vertex needs at least one support vertex from the same zone
4. If any peripheral from zone 1 is included, no zone 3 vertices
5. Peripheral count ≤ core count

Let me try to find a solution with 2 core vertices.

**Option: Include cores 1 and 9**
- Core 1 (zone 1) needs support from zone 1: 2 or 3
- Core 9 (zone 2) needs support from zone 2: 10 or 11

Let me try: cores {1, 9}, supports {3, 11}

Check independence:
- 1 and 3: no edge ✓
- 1 and 11: no edge ✓
- 9 and 3: no edge ✓
- 9 and 11: no edge ✓
- 3 and 11: no edge ✓

Now I need peripheral vertices. Peripheral count ≤ core count = 2, so at most 2 peripherals.

Available peripherals (not adjacent to {1, 3, 9, 11}):
- 1 is adjacent to: 2, 4, 10, 17
- 3 is adjacent to: 6
- 9 is adjacent to: 10, 12, 17
- 11 is adjacent to: 15

So excluded: 2, 4, 6, 10, 12, 15, 17

Available peripherals: 5, 7, 8, 13, 14, 16, 20, 21, 22, 23, 24

Check edges among these:
- (5,8): edge
- (8,16): edge
- (8,24): edge
- (13,14): edge
- (16,24): edge
- (20,23): edge
- (21,24): edge

I need 2 peripherals with no edge between them and satisfying zone constraint.

If I pick from zone 1 peripherals: 5, 7, 8
If I pick any zone 1 peripheral, I can't have zone 3 vertices.

Let me try without zone 1 peripherals to keep zone 3 options open.

From zone 2: 13, 14, 16
From zone 3: 20, 21, 22, 23, 24

Pick 13 and 22: no edge between them ✓
- 13 not adjacent to {1,3,9,11} ✓
- 22 not adjacent to {1,3,9,11} ✓
- 22 not adjacent to 13 ✓

Set: {1, 3, 9, 11, 13, 22} = size 6

Can I add one more? Peripheral count would be 3 > core count 2. Violates constraint 5.

So with 2 cores, max peripherals = 2, giving total = 2 + 2 + 2 = 6.

**Option: Include cores 1 and 17**
- Core 1 (zone 1) needs support from zone 1: 2 or 3
- Core 17 (zone 3) needs support from zone 3: 18 or 19

Try: cores {1, 17}, supports {3, 18}

Check independence:
- 1 and 3: no edge ✓
- 1 and 18: no edge ✓
- 17 and 3: no edge ✓
- 17 and 18: edge! ✗

Try: cores {1, 17}, supports {3, 19}

- 17 and 19: no edge ✓
- 1 and 19: no edge ✓
- 3 and 19: no edge ✓
- 3 and 17: no edge ✓

Excluded by {1, 3, 17, 19}: 2, 4, 6, 10, 18, 20, 22

Available peripherals: 5, 7, 8, 12, 13, 14, 15, 16, 21, 23, 24

Peripheral count ≤ 2.

If I pick zone 1 peripheral, no zone 3 vertices allowed.

Pick 5 and 13: no edge ✓
- 5 not adjacent to {1,3,17,19} ✓
- 13 not adjacent to {1,3,17,19} ✓

Set: {1, 3, 5, 13, 17, 19} = size 6

Can I add one more peripheral? No, would exceed core count.

**Option: Include cores 9 and 17**
- Core 9 (zone 2) needs support from zone 2: 10 or 11
- Core 17 (zone 3) needs support from zone 3: 18 or 19

Try: cores {9, 17}, supports {11, 19}

Check independence:
- 9 and 11: no edge ✓
- 9 and 19: no edge ✓
- 17 and 11: no edge ✓
- 17 and 19: no edge ✓
- 11 and 19: no edge ✓

Excluded by {9, 11, 17, 19}: 2, 10, 12, 15, 18, 20, 22

Available peripherals: 4, 5, 6, 7, 8, 13, 14, 16, 21, 23, 24

Peripheral count ≤ 2.

If I pick zone 1 peripheral, no zone 3 vertices.

Pick 4 and 13: no edge ✓
- 4 not adjacent to {9,11,17,19} ✓
- 13 not adjacent to {9,11,17,19} ✓

Set: {4, 9, 11, 13, 17, 19} = size 6

Hmm, still 6. Let me think differently.

**What if I use only 1 core vertex?**
Then peripheral count ≤ 1.
Total = 1 + support + peripheral ≤ 1 + support + 1

With 1 core, I need at least 1 support from same zone. So minimum 2 vertices from core+support.

To reach 7, I'd need 5 more vertices, but only 1 can be peripheral. So I'd need 4 more support vertices? But support vertices are limited and may have edges.

Actually wait - the constraint says peripheral count ≤ core count. If core count = 1, peripheral count ≤ 1. But I can have as many support vertices as I want (as long as independent).

Let me reconsider. With 2 cores, I can have 2 peripherals. Total = 2 cores + support + 2 peripherals.

To maximize, I want many support vertices. Let me check if I can include more support vertices.

**Try: cores {1, 9}, supports {3, 11}**
Can I add more support vertices? Other supports: 2, 10, 18, 19
- 2: adjacent to 1 (edge (1,2)) ✗
- 10: adjacent to 1 (edge (1,10)) and 9 (edge (9,10)) ✗
- 18: not adjacent to 1, 3, 9, 11 ✓
- 19: not adjacent to 1, 3, 9, 11 ✓
- 18 and 19: edge (18,19) ✗

So I can add one of {18, 19}. Let's add 18.

Set so far: {1, 3, 9, 11, 18}

Now peripherals ≤ 2. Available peripherals not adjacent to any of {1, 3, 9, 11, 18}:
- 1 adj: 2, 4, 10, 17
- 3 adj: 6
- 9 adj: 10, 12, 17
- 11 adj: 15
- 18 adj: 17, 19, 21

Excluded: 2, 4, 6, 10, 12, 15, 17, 19, 21

Available peripherals: 5, 7, 8, 13, 14, 16, 20, 22, 23, 24

Check edges among these:
- (5,8): edge
- (8,16): edge
- (8,24): edge
- (13,14): edge
- (16,24): edge
- (20,23): edge

I need 2 peripherals with no edge between them.

If I pick zone 1 peripheral (5, 7, or 8), no zone 3 vertices allowed.

Pick 5 and 13: no edge ✓
- 5 not adjacent to {1,3,9,11,18} ✓
- 13 not adjacent to {1,3,9,11,18} ✓

Set: {1, 3, 5, 9, 11, 13, 18} = size 7!

Let me verify all constraints:

**Independence check:**
- 1-3: no edge ✓
- 1-5: no edge ✓
- 1-9: no edge ✓
- 1-11: no edge ✓
- 1-13: no edge ✓
- 1-18: no edge ✓
- 3-5: no edge ✓
- 3-9: no edge ✓
- 3-11: no edge ✓
- 3-13: no edge ✓
- 3-18: no edge ✓
- 5-9: no edge ✓
- 5-11: no edge ✓
- 5-13: no edge ✓
- 5-18: no edge ✓
- 9-11: no edge ✓
- 9-13: no edge ✓
- 9-18: no edge ✓
- 11-13: no edge ✓
- 11-18: no edge ✓
- 13-18: no edge ✓

All good! ✓

**Constraint 2: Core count limit** - cores are {1, 9}, count = 2 ≤ 2 ✓

**Constraint 3: Core-Support Dependency**
- Core 1 (zone 1) → support 3 (zone 1) ✓
- Core 9 (zone 2) → support 11 (zone 2) ✓

**Constraint 4: Conditional Zone Exclusion**
- Peripheral from zone 1: vertex 5 (zone 1) is included
- Zone 3 vertices: vertex 18 is in zone 3!
- This violates constraint 4! ✗

So this doesn't work. I need to either:
1. Not include any zone 1 peripheral, or
2. Not include any zone 3 vertex

Let me try without zone 1 peripherals.

Set: {1, 3, 9, 11, 18} + peripherals from zone 2 or 3 only.

Available peripherals (not adjacent to {1,3,9,11,18}, not zone 1):
- Zone 2: 13, 14, 16
- Zone 3: 20, 22, 23, 24

Edges: (13,14), (16,24), (20,23)

Pick 13 and 22: no edge ✓
- 13 not adjacent to any in set ✓
- 22 not adjacent to any in set ✓

Set: {1, 3, 9, 11, 13, 18, 22} = size 7

**Verify all constraints:**

**Independence:**
- 1-3: no edge ✓
- 1-9: no edge ✓
- 1-11: no edge ✓
- 1-13: no edge ✓
- 1-18: no edge ✓
- 1-22: no edge ✓
- 3-9: no edge ✓
- 3-11: no edge ✓
- 3-13: no edge ✓
- 3-18: no edge ✓
- 3-22: no edge ✓
- 9-11: no edge ✓
- 9-13: no edge ✓
- 9-18: no edge ✓
- 9-22: no edge ✓
- 11-13: no edge ✓
- 11-18: no edge ✓
- 11-22: no edge ✓
- 13-18: no edge ✓
- 13-22: no edge ✓
- 18-22: no edge ✓

All independent ✓

**Constraint 2:** Core count = 2 ≤ 2 ✓

**Constraint 3:** 
- Core 1 (zone 1) → support 3 (zone 1) ✓
- Core 9 (zone 2) → support 11 (zone 2) ✓

**Constraint 4:** No peripheral from zone 1 included (13 is zone 2, 22 is zone 3). ✓

**Constraint 5:** Peripheral count = 2 (vertices 13, 22) ≤ core count = 2 ✓

This works! Size = 7.

Let me verify the types:
- Core: 1, 9 ✓
- Support: 3, 11, 18 ✓
- Peripheral: 13, 22 ✓

Wait, 18 is a support vertex. Let me double-check: Support vertices are 2, 3, 10, 11, 18, 19. Yes, 18 is support ✓.

So the solution is:
- independent_set: [1, 3, 9, 11, 13, 18, 22]
- size: 7
- core_vertices: [1, 9]
- support_vertices: [3, 11, 18]
- peripheral_vertices: [13, 22]
- core_count: 2
- support_count: 3
- peripheral_count: 2

```json
{
  "independent_set": [1, 3, 9, 11, 13, 18, 22],
  "size": 7,
  "core_vertices": [1, 9],
  "support_vertices": [3, 11, 18],
  "peripheral_vertices": [13, 22],
  "core_count": 2,
  "support_count": 3,
  "peripheral_count": 2
}
```
```
