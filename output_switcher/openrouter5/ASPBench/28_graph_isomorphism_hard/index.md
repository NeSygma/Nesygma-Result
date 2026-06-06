# Benchmark Report (SWITCHER): ASPBench - 28_graph_isomorphism_hard

**Provider:** openrouter5
**Model:** deepseek/deepseek-v4-flash
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 30.67s

## System 1 Execution Context

```json
We can see that both graphs have the same structure:  
- Two red-blue pairs connected internally with weights 10 and 20.  
- A cross connection between the two pairs with weight 30 between red vertices and 40 between blue vertices.  
- Special vertex is a red vertex in both (1 in G1, a in G2).  

The natural mapping is:  
1 → a, 2 → b, 3 → c, 4 → d, 5 → e, 6 → f, 7 → g, 8 → h.  

Now check the forbidden subgraph condition:  
A 3-cycle involving the special vertex (a) with total weight exactly 60.  
Possible triangles with a:  
- a-c-e: weights 10 + 30 + ? (c-e doesn’t exist) → no triangle.  
- a-d-e: 20 + 30 + ? (d-e doesn’t exist) → no triangle.  
- a-c-g: 10 + 40 + ? (a-g doesn’t exist) → no triangle.  
- a-d-h: 20 + 40 + ? (a-h doesn’t exist) → no triangle.  

No triangle with special vertex a exists at all, so condition is automatically satisfied.  

Thus the mapping is valid.

```json
{
  "is_isomorphic": true,
  "mapping": {
    "1": "a",
    "2": "b",
    "3": "c",
    "4": "d",
    "5": "e",
    "6": "f",
    "7": "g",
    "8": "h"
  },
  "preserved_weighted_edges": [
    [["1", "3", 10], ["a", "c", 10]],
    [["1", "4", 20], ["a", "d", 20]],
    [["1", "5", 30], ["a", "e", 30]],
    [["2", "3", 20], ["b", "c", 20]],
    [["2", "4", 10], ["b", "d", 10]],
    [["2", "6", 30], ["b", "f", 30]],
    [["3", "7", 40], ["c", "g", 40]],
    [["4", "8", 40], ["d", "h", 40]],
    [["5", "7", 10], ["e", "g", 10]],
    [["5", "8", 20], ["e", "h", 20]],
    [["6", "7", 20], ["f", "g", 20]],
    [["6", "8", 10], ["f", "h", 10]]
  ]
}
```
```

## Switcher Execution


 SWITCHER META EVALUATOR AGENT

 Query: PROBLEM:
# Problem Statement

Determine if two weighted, colored graphs are isomorphic while avoiding forbidden subgraph patterns. An isomorphism must preserve vertex colors, edge weights, special vertex properties, and must not create any 3-cycle involving a special vertex with total edge weight of exactly 60.

## Instance Data

**Graph G1:**
- Vertices: 1, 2, 3, 4, 5, 6, 7, 8
- Colors:
  - Red vertices: 1, 2, 5, 6
  - Blue vertices: 3, 4, 7, 8
- Special vertices: 1
- Edges (undirected, with weights):
  - (1,3,10), (1,4,20), (2,3,20), (2,4,10)
  - (5,7,10), (5,8,20), (6,7,20), (6,8,10)
  - (1,5,30), (2,6,30), (3,7,40), (4,8,40)

**Graph G2:**
- Vertices: a, b, c, d, e, f, g, h
- Colors:
  - Red vertices: a, b, e, f
  - Blue vertices: c, d, g, h
- Special vertices: a
- Edges (undirected, with weights):
  - (a,c,10), (a,d,20), (b,c,20), (b,d,10)
  - (e,g,10), (e,h,20), (f,g,20), (f,h,10)
  - (a,e,30), (b,f,30), (c,g,40), (d,h,40)

## Constraints

1. **Bijection**: The mapping f: V1 → V2 must be one-to-one and onto
2. **Color Preservation**: Color of vertex v in G1 must equal color of f(v) in G2
3. **Special Vertex Preservation**: Vertex v is special in G1 if and only if f(v) is special in G2
4. **Edge and Weight Preservation**: Edge (u,v) with weight w exists in G1 if and only if edge (f(u),f(v)) with weight w exists in G2
5. **Forbidden Subgraph**: The mapping is invalid if it creates a 3-cycle (triangle) in G2 that involves a special vertex and has total edge weight exactly 60

## Objective

Find a valid isomorphism mapping between G1 and G2, or determine that no such mapping exists.

**Field Descriptions:**
- `is_isomorphic`: Boolean indicating if graphs are isomorphic
- `mapping`: Object mapping G1 vertex (as string) to G2 vertex (as string), or null if not isomorphic
- `preserved_weighted_edges`: Array of edge mappings showing [[G1_edge], [G2_edge]] pairs, where edges are normalized (sorted vertices)

SYSTEM 1 ANSWER (For Evaluation):
We can see that both graphs have the same structure:  
- Two red-blue pairs connected internally with weights 10 and 20.  
- A cross connection between the two pairs with weight 30 between red vertices and 40 between blue vertices.  
- Special vertex is a red vertex in both (1 in G1, a in G2).  

The natural mapping is:  
1 → a, 2 → b, 3 → c, 4 → d, 5 → e, 6 → f, 7 → g, 8 → h.  

Now check the forbidden subgraph condition:  
A 3-cycle involving the special vertex (a) with total weight exactly 60.  
Possible triangles with a:  
- a-c-e: weights 10 + 30 + ? (c-e doesn’t exist) → no triangle.  
- a-d-e: 20 + 30 + ? (d-e doesn’t exist) → no triangle.  
- a-c-g: 10 + 40 + ? (a-g doesn’t exist) → no triangle.  
- a-d-h: 20 + 40 + ? (a-h doesn’t exist) → no triangle.  

No triangle with special vertex a exists at all, so condition is automatically satisfied.  

Thus the mapping is valid.

```json
{
  "is_isomorphic": true,
  "mapping": {
    "1": "a",
    "2": "b",
    "3": "c",
    "4": "d",
    "5": "e",
    "6": "f",
    "7": "g",
    "8": "h"
  },
  "preserved_weighted_edges": [
    [["1", "3", 10], ["a", "c", 10]],
    [["1", "4", 20], ["a", "d", 20]],
    [["1", "5", 30], ["a", "e", 30]],
    [["2", "3", 20], ["b", "c", 20]],
    [["2", "4", 10], ["b", "d", 10]],
    [["2", "6", 30], ["b", "f", 30]],
    [["3", "7", 40], ["c", "g", 40]],
    [["4", "8", 40], ["d", "h", 40]],
    [["5", "7", 10], ["e", "g", 10]],
    [["5", "8", 20], ["e", "h", 20]],
    [["6", "7", 20], ["f", "g", 20]],
    [["6", "8", 10], ["f", "h", 10]]
  ]
}
```

ANTI-ANCHORING REMINDER: Do NOT let the System 1 Answer above bias your independent reasoning in Stage 2. You MUST complete your own derivation from the premises alone before comparing against the System 1 Answer. Treat the System 1 Answer as a hypothesis to be verified, not as a guide.

Follow your system instructions to complete all 5 Metacognitive stages evaluating the provided SYSTEM 1 ANSWER.
Apply the three cognitive de-biasing checks (anchoring, confirmation, and overconfidence) at each relevant stage as instructed.
After completing all stages, output your confidence score in EXACTLY this format on a new line:
Confidence: <number between 0 and 100>%

# Metacognitive Evaluation of System 1 Answer

## Stage 1 — Comprehension & Formalization

**Premises Restated:**
- G1: 8 vertices (1-8), G2: 8 vertices (a-h)
- Color mapping: Red={1,2,5,6}↔{a,b,e,f}, Blue={3,4,7,8}↔{c,d,g,h}
- Special vertex: 1 in G1, a in G2
- Edge sets are structurally identical with weights: internal red-blue pairs (10,20), cross connections (30 between reds, 40 between blues)
- Forbidden: any 3-cycle involving special vertex with total weight exactly 60

**System 1's Claim:**
- Mapping: 1→a, 2→b, 3→c, 4→d, 5→e, 6→f, 7→g, 8→h
- No forbidden triangle exists → mapping is valid
- Final answer: isomorphic with that mapping

**Potential Issues to Flag:**
- System 1 only checked triangles involving vertex a directly. Need to verify ALL triangles that could involve the special vertex after mapping.

## Stage 2 — Independent Reasoning (Anti-Anchoring)

Let me derive my own solution from scratch.

**Graph Structure Analysis:**

G1 has two isomorphic "blocks":
- Block A: {1,2,3,4} with edges: (1,3,10), (1,4,20), (2,3,20), (2,4,10), plus cross edges (1,5,30), (2,6,30), (3,7,40), (4,8,40)
- Block B: {5,6,7,8} with edges: (5,7,10), (5,8,20), (6,7,20), (6,8,10)

G2 has identical structure with {a,b,c,d} and {e,f,g,h}.

**Color constraints force:**
- Red vertices {1,2,5,6} must map to {a,b,e,f}
- Blue vertices {3,4,7,8} must map to {c,d,g,h}
- Special vertex 1 must map to special vertex a

**Edge constraints force the internal structure:**
- Vertex 1 (red, special) connects to: 3(blue,10), 4(blue,20), 5(red,30)
- Vertex a (red, special) connects to: c(blue,10), d(blue,20), e(red,30)
- So 1→a forces: {3,4}→{c,d} and 5→e (since 5 is red and connects to 1 with weight 30, and only e connects to a with weight 30)

**Continuing the forced mapping:**
- Vertex 2 (red) connects to: 3(blue,20), 4(blue,10), 6(red,30)
- Vertex b (red) connects to: c(blue,20), d(blue,10), f(red,30)
- Since {3,4}→{c,d}, we get 2→b and 6→f

**Blue vertices:**
- Vertex 3 (blue) connects to: 1(red,10), 2(red,20), 7(blue,40)
- Vertex c (blue) connects to: a(red,10), b(red,20), g(blue,40)
- Since 1→a, 2→b, we get 3→c and 7→g

- Vertex 4 (blue) connects to: 1(red,20), 2(red,10), 8(blue,40)
- Vertex d (blue) connects to: a(red,20), b(red,10), h(blue,40)
- Since 1→a, 2→b, we get 4→d and 8→h

**The mapping is uniquely forced:** 1→a, 2→b, 3→c, 4→d, 5→e, 6→f, 7→g, 8→h

**Forbidden Subgraph Check (my independent analysis):**

I need to check ALL 3-cycles in G2 that involve vertex a (the special vertex).

Possible triangles with vertex a:
- a-c-e: edges (a,c,10), (a,e,30), (c,e) — does (c,e) exist? No. Not a triangle.
- a-c-g: edges (a,c,10), (c,g,40), (a,g) — does (a,g) exist? No. Not a triangle.
- a-d-e: edges (a,d,20), (a,e,30), (d,e) — does (d,e) exist? No. Not a triangle.
- a-d-h: edges (a,d,20), (d,h,40), (a,h) — does (a,h) exist? No. Not a triangle.
- a-c-b: edges (a,c,10), (a,b) — does (a,b) exist? No. Not a triangle.
- a-d-b: edges (a,d,20), (a,b) — does (a,b) exist? No. Not a triangle.
- a-e-b: edges (a,e,30), (a,b) — does (a,b) exist? No. Not a triangle.

**No triangle involving vertex a exists at all in G2.** Therefore the forbidden condition is vacuously satisfied.

**My Independent Conclusion:** The graphs are isomorphic with the uniquely forced mapping. System 1's answer is correct.

## Stage 3 — Critical Deductive Evaluation (Anti-Confirmation)

**Attempting to falsify System 1's conclusion:**

Could there be an alternative mapping that also satisfies constraints? Let me check if any other mapping is possible.

The constraints are so tight that the mapping is uniquely determined:
- 1→a (special vertex constraint)
- 5→e (only red vertex connected to a with weight 30)
- 2→b (only remaining red vertex that connects to the blue vertices mapped from {3,4})
- 6→f (only remaining red vertex)
- 3→c, 4→d (blue vertices connected to 1 with weights 10 and 20 respectively)
- 7→g, 8→h (remaining blue vertices)

Wait — could 3→d and 4→c? Let me check:
- If 3→d: edge (1,3,10) maps to (a,d,20) — weight mismatch! 10≠20. Invalid.
- If 4→c: edge (1,4,20) maps to (a,c,10) — weight mismatch! 20≠10. Invalid.

So the mapping is uniquely forced. No alternative exists.

**Could there be a triangle I missed?** Let me exhaustively list all 3-vertex subsets containing vertex a in G2:
{a,b,c}, {a,b,d}, {a,b,e}, {a,b,f}, {a,b,g}, {a,b,h}
{a,c,d}, {a,c,e}, {a,c,f}, {a,c,g}, {a,c,h}
{a,d,e}, {a,d,f}, {a,d,g}, {a,d,h}
{a,e,f}, {a,e,g}, {a,e,h}
{a,f,g}, {a,f,h}
{a,g,h}

For each, check if all three edges exist:
- {a,c,e}: edges (a,c,10), (a,e,30) exist, but (c,e) does NOT exist. Not a triangle.
- {a,c,g}: edges (a,c,10), (c,g,40) exist, but (a,g) does NOT exist. Not a triangle.
- {a,d,e}: edges (a,d,20), (a,e,30) exist, but (d,e) does NOT exist. Not a triangle.
- {a,d,h}: edges (a,d,20), (d,h,40) exist, but (a,h) does NOT exist. Not a triangle.

All other sets lack at least two edges. **No triangle with vertex a exists.**

**Falsification attempt FAILED** — System 1's conclusion withstands scrutiny.

## Stage 4 — Decision Confirmation

System 1's conclusion that the graphs are isomorphic with the given mapping is **strictly entailed by the premises**. The mapping is uniquely forced by the constraints, and the forbidden subgraph condition is vacuously satisfied since no triangle involving the special vertex exists in G2.

**Alternative interpretation check:** Could "creates a 3-cycle" mean the mapping itself creates a triangle that wasn't there before? No — the condition says "creates a 3-cycle in G2 that involves a special vertex." Since G2's edge set is fixed, we check existing triangles in G2. No ambiguity.

## Stage 5 — Confidence & Soundness Assessment

**Step-Type Classification:**

1. **Step 1: Special vertex mapping** (1→a) — Type A (Forced Entailment, directly from constraint 3). Penalty: 0%.

2. **Step 2: Color-constrained mapping** (red→red, blue→blue) — Type A (Forced Entailment from constraint 2). Penalty: 0%.

3. **Step 3: Edge-weight forced mapping** (5→e, 2→b, 6→f, 3→c, 4→d, 7→g, 8→h) — Type A (Forced Entailment via modus ponens on edge preservation constraints). Each sub-step is uniquely determined. Penalty: 0%.

4. **Step 4: Triangle check** — Type A (Exhaustive enumeration of all 3-vertex subsets containing vertex a; each is verified to lack at least one edge). No unverified branches. Penalty: 0%.

**Total accumulated penalty: 0%**

**Self-Doubt (Red Teaming) Check:**
1. **Possibility of misreading the forbidden condition**: Could "creates a 3-cycle" mean the mapping induces a triangle in the *combined* structure that wasn't there before? No — the condition explicitly says "in G2," and G2's edge set is fixed.
2. **Possibility of missing an edge in G2**: Did I verify all edges? Yes — the edge list is complete and symmetric. No edge (a,g), (a,h), (c,e), (d,e), etc. exist.
3. **Possibility of alternative valid mapping**: Could there be a different bijection that also satisfies constraints? I proved the mapping is uniquely forced by edge weights and colors. No alternative exists.

**Anchoring Check:** System 1's answer matched my independent derivation. I completed Stage 2 before comparing, so no anchoring influence. No penalty.

**Confirmation Check:** I actively attempted to falsify System 1's conclusion by searching for alternative mappings and missed triangles. The falsification attempt failed. No penalty.

**Final Confidence:** System 1's answer is provably correct. The mapping is uniquely forced, and the forbidden condition is vacuously satisfied. Every step is Type A (Forced Entailment). Confidence is 100%.

Confidence: 100%

### TOKEN USAGE

  Input tokens:  4,075
  Output tokens: 2,445
  Total tokens:  6,520

COMPLETE

### Switcher Final Answer

```
# Metacognitive Evaluation of System 1 Answer

## Stage 1 — Comprehension & Formalization

**Premises Restated:**
- G1: 8 vertices (1-8), G2: 8 vertices (a-h)
- Color mapping: Red={1,2,5,6}↔{a,b,e,f}, Blue={3,4,7,8}↔{c,d,g,h}
- Special vertex: 1 in G1, a in G2
- Edge sets are structurally identical with weights: internal red-blue pairs (10,20), cross connections (30 between reds, 40 between blues)
- Forbidden: any 3-cycle involving special vertex with total weight exactly 60

**System 1's Claim:**
- Mapping: 1→a, 2→b, 3→c, 4→d, 5→e, 6→f, 7→g, 8→h
- No forbidden triangle exists → mapping is valid
- Final answer: isomorphic with that mapping

**Potential Issues to Flag:**
- System 1 only checked triangles involving vertex a directly. Need to verify ALL triangles that could involve the special vertex after mapping.

## Stage 2 — Independent Reasoning (Anti-Anchoring)

Let me derive my own solution from scratch.

**Graph Structure Analysis:**

G1 has two isomorphic "blocks":
- Block A: {1,2,3,4} with edges: (1,3,10), (1,4,20), (2,3,20), (2,4,10), plus cross edges (1,5,30), (2,6,30), (3,7,40), (4,8,40)
- Block B: {5,6,7,8} with edges: (5,7,10), (5,8,20), (6,7,20), (6,8,10)

G2 has identical structure with {a,b,c,d} and {e,f,g,h}.

**Color constraints force:**
- Red vertices {1,2,5,6} must map to {a,b,e,f}
- Blue vertices {3,4,7,8} must map to {c,d,g,h}
- Special vertex 1 must map to special vertex a

**Edge constraints force the internal structure:**
- Vertex 1 (red, special) connects to: 3(blue,10), 4(blue,20), 5(red,30)
- Vertex a (red, special) connects to: c(blue,10), d(blue,20), e(red,30)
- So 1→a forces: {3,4}→{c,d} and 5→e (since 5 is red and connects to 1 with weight 30, and only e connects to a with weight 30)

**Continuing the forced mapping:**
- Vertex 2 (red) connects to: 3(blue,20), 4(blue,10), 6(red,30)
- Vertex b (red) connects to: c(blue,20), d(blue,10), f(red,30)
- Since {3,4}→{c,d}, we get 2→b and 6→f

**Blue vertices:**
- Vertex 3 (blue) connects to: 1(red,10), 2(red,20), 7(blue,40)
- Vertex c (blue) connects to: a(red,10), b(red,20), g(blue,40)
- Since 1→a, 2→b, we get 3→c and 7→g

- Vertex 4 (blue) connects to: 1(red,20), 2(red,10), 8(blue,40)
- Vertex d (blue) connects to: a(red,20), b(red,10), h(blue,40)
- Since 1→a, 2→b, we get 4→d and 8→h

**The mapping is uniquely forced:** 1→a, 2→b, 3→c, 4→d, 5→e, 6→f, 7→g, 8→h

**Forbidden Subgraph Check (my independent analysis):**

I need to check ALL 3-cycles in G2 that involve vertex a (the special vertex).

Possible triangles with vertex a:
- a-c-e: edges (a,c,10), (a,e,30), (c,e) — does (c,e) exist? No. Not a triangle.
- a-c-g: edges (a,c,10), (c,g,40), (a,g) — does (a,g) exist? No. Not a triangle.
- a-d-e: edges (a,d,20), (a,e,30), (d,e) — does (d,e) exist? No. Not a triangle.
- a-d-h: edges (a,d,20), (d,h,40), (a,h) — does (a,h) exist? No. Not a triangle.
- a-c-b: edges (a,c,10), (a,b) — does (a,b) exist? No. Not a triangle.
- a-d-b: edges (a,d,20), (a,b) — does (a,b) exist? No. Not a triangle.
- a-e-b: edges (a,e,30), (a,b) — does (a,b) exist? No. Not a triangle.

**No triangle involving vertex a exists at all in G2.** Therefore the forbidden condition is vacuously satisfied.

**My Independent Conclusion:** The graphs are isomorphic with the uniquely forced mapping. System 1's answer is correct.

## Stage 3 — Critical Deductive Evaluation (Anti-Confirmation)

**Attempting to falsify System 1's conclusion:**

Could there be an alternative mapping that also satisfies constraints? Let me check if any other mapping is possible.

The constraints are so tight that the mapping is uniquely determined:
- 1→a (special vertex constraint)
- 5→e (only red vertex connected to a with weight 30)
- 2→b (only remaining red vertex that connects to the blue vertices mapped from {3,4})
- 6→f (only remaining red vertex)
- 3→c, 4→d (blue vertices connected to 1 with weights 10 and 20 respectively)
- 7→g, 8→h (remaining blue vertices)

Wait — could 3→d and 4→c? Let me check:
- If 3→d: edge (1,3,10) maps to (a,d,20) — weight mismatch! 10≠20. Invalid.
- If 4→c: edge (1,4,20) maps to (a,c,10) — weight mismatch! 20≠10. Invalid.

So the mapping is uniquely forced. No alternative exists.

**Could there be a triangle I missed?** Let me exhaustively list all 3-vertex subsets containing vertex a in G2:
{a,b,c}, {a,b,d}, {a,b,e}, {a,b,f}, {a,b,g}, {a,b,h}
{a,c,d}, {a,c,e}, {a,c,f}, {a,c,g}, {a,c,h}
{a,d,e}, {a,d,f}, {a,d,g}, {a,d,h}
{a,e,f}, {a,e,g}, {a,e,h}
{a,f,g}, {a,f,h}
{a,g,h}

For each, check if all three edges exist:
- {a,c,e}: edges (a,c,10), (a,e,30) exist, but (c,e) does NOT exist. Not a triangle.
- {a,c,g}: edges (a,c,10), (c,g,40) exist, but (a,g) does NOT exist. Not a triangle.
- {a,d,e}: edges (a,d,20), (a,e,30) exist, but (d,e) does NOT exist. Not a triangle.
- {a,d,h}: edges (a,d,20), (d,h,40) exist, but (a,h) does NOT exist. Not a triangle.

All other sets lack at least two edges. **No triangle with vertex a exists.**

**Falsification attempt FAILED** — System 1's conclusion withstands scrutiny.

## Stage 4 — Decision Confirmation

System 1's conclusion that the graphs are isomorphic with the given mapping is **strictly entailed by the premises**. The mapping is uniquely forced by the constraints, and the forbidden subgraph condition is vacuously satisfied since no triangle involving the special vertex exists in G2.

**Alternative interpretation check:** Could "creates a 3-cycle" mean the mapping itself creates a triangle that wasn't there before? No — the condition says "creates a 3-cycle in G2 that involves a special vertex." Since G2's edge set is fixed, we check existing triangles in G2. No ambiguity.

## Stage 5 — Confidence & Soundness Assessment

**Step-Type Classification:**

1. **Step 1: Special vertex mapping** (1→a) — Type A (Forced Entailment, directly from constraint 3). Penalty: 0%.

2. **Step 2: Color-constrained mapping** (red→red, blue→blue) — Type A (Forced Entailment from constraint 2). Penalty: 0%.

3. **Step 3: Edge-weight forced mapping** (5→e, 2→b, 6→f, 3→c, 4→d, 7→g, 8→h) — Type A (Forced Entailment via modus ponens on edge preservation constraints). Each sub-step is uniquely determined. Penalty: 0%.

4. **Step 4: Triangle check** — Type A (Exhaustive enumeration of all 3-vertex subsets containing vertex a; each is verified to lack at least one edge). No unverified branches. Penalty: 0%.

**Total accumulated penalty: 0%**

**Self-Doubt (Red Teaming) Check:**
1. **Possibility of misreading the forbidden condition**: Could "creates a 3-cycle" mean the mapping induces a triangle in the *combined* structure that wasn't there before? No — the condition explicitly says "in G2," and G2's edge set is fixed.
2. **Possibility of missing an edge in G2**: Did I verify all edges? Yes — the edge list is complete and symmetric. No edge (a,g), (a,h), (c,e), (d,e), etc. exist.
3. **Possibility of alternative valid mapping**: Could there be a different bijection that also satisfies constraints? I proved the mapping is uniquely forced by edge weights and colors. No alternative exists.

**Anchoring Check:** System 1's answer matched my independent derivation. I completed Stage 2 before comparing, so no anchoring influence. No penalty.

**Confirmation Check:** I actively attempted to falsify System 1's conclusion by searching for alternative mappings and missed triangles. The falsification attempt failed. No penalty.

**Final Confidence:** System 1's answer is provably correct. The mapping is uniquely forced, and the forbidden condition is vacuously satisfied. Every step is Type A (Forced Entailment). Confidence is 100%.

Confidence: 100%
```
