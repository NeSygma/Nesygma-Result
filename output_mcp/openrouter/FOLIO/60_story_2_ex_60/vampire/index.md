# Benchmark Report (MCP): FOLIO - story_2_ex_60

**Provider:** openrouter
**Model:** openai/gpt-oss-120b:free
**Solver:** vampire
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 113.94s


 MCP VAMPIRE AGENT - Symbolic Reasoning

### Query
Consider the following logical premises: Billings is a city in the state of Montana in U.S. The

state of Montana includes the cities of Butte, Helena, and Missoula. White Sulphur Springs and Butte
are cities in the same state in U.S. The city of St Pierre is not in the state of Montana. Any city
in Butte is not in St Pierre. A city can only be in one state in U.S. except for Bristol, Texarkana,
Texhoma and Union City. Conclusion to evaluate: Montana is home to the city of Missoula. Question:
Based STRICTLY on the premises, is the conclusion True, False, or Uncertain? Return your final
answer in JSON format like this: {"Conclusion": "True or False or Uncertain in here"}

  - write_and_run_vampire: Write two TPTP problem files (positive claim and negation) and run Vampire 
on both concurrently to get proof results for both in one iteration.
Returns a dictionary with 'positive' and 'negative' result objects.

## Iteration 1



### Thinking

- We need to translate to TPTP and run both positive and negative conjectures. Premises:
- - Billings is a city in the state of Montana in U.S. - The state of Montana includes the cities of Butte, Helena, and Missoula. - White Sulphur Springs and Butte are cities in the same state in U.S. - The city of St Pierre is not in the state of Montana. - Any city in Butte is not in St Pierre. (Interpretation: any city that is in Butte? Actually "Any city in Butte is not in St Pierre." Might mean any city that is in the city of Butte? That seems odd. Probably means any city that is in the state of Butte? But Butte is a city, not a state. Could be "Any city in Butte is not in St Pierre." Means any city that is in the same state as Butte is not in St Pierre. But we have earlier "White Sulphur Springs and Butte are cities in the same state in U.S." So there is a state that contains both White Sulphur Springs and Butte. So "Any city in Butte is not in St Pierre." Could be interpreted as: any city that is in the same state as Butte is not in St Pierre. We'll model a predicate in_state(City, State). Also a predicate city(C). Also state(S). We'll treat "city in Butte" as "in_state(C, S)" where S is the state that contains Butte. So we need a way to refer to that state. Could use existential: there exists a state S such that in_state(butte, S) and for all C, if in_state(C, S) then not in_state(C, st_pierre). That's a plausible formalization.
- - A city can only be in one state in U.S. except for Bristol, Texarkana, Texhoma and Union City. Means uniqueness of state per city, except those four cities may be in multiple states. We'll ignore those exceptions as they are not involved.
- Goal: Montana is home to the city of Missoula. Means in_state(missoula, montana).
- We need to see if premises entail that. Premise 2 says "The state of Montana includes the cities of Butte, Helena, and Missoula." So directly we have in_state(butte, montana), in_state(helena, montana), in_state(missoula, montana). So conclusion is directly entailed. So should be Theorem.
- We need to encode premises. Also need distinctness axioms for constants.
- We'll use fof.
- Define predicate city(C) maybe not needed. Use in_state(C, S). Also state(S). We'll assert in_state(billings, montana). Also in_state(butte, montana). etc.
- Premise 3: White Sulphur Springs and Butte are cities in the same state. Means there exists a state S such that in_state(white_sulphur_springs, S) & in_state(butte, S). We'll encode as: ? [S] : (in_state(white_sulphur_springs, S) & in_state(butte, S)). This doesn't assert uniqueness but okay.
- Premise 5: Any city in Butte is not in St Pierre. Formalize: ? [S] : (in_state(butte, S) & ! [C] : (in_state(C, S) => ~in_state(C, st_pierre))). This captures that the state containing Butte has no city also in St Pierre.
- Premise 4: ~in_state(st_pierre, montana).
- Premise 6: uniqueness: For all C, S1, S2: (in_state(C,S1) & in_state(C,S2) & C not in exception list) => S1 = S2. We'll add exception list constants.
- We'll need distinctness axioms for all city constants and state constants.
- Cities: billings, butte, helena, missoula, white_sulphur_springs, st_pierre. Also maybe others not needed.
- States: montana, some other state (unknown). We'll just have montana and maybe other_state variable but not needed.
- We'll add distinctness: billings != butte, etc.
- Now create positive TPTP with conjecture: in_state(missoula, montana).
- Negative TPTP with conjecture: ~in_state(missoula, montana).
- Run.




### TOKEN USAGE - Iteration 1

  Input tokens:  4,912
  Output tokens: 1,884
  Total tokens:  6,796

### Tool Call: write_and_run_vampire

  Args: {
  "pos_filename": "pos.p",
  "pos_code": "% Positive version\nfof(distinct_cities, axiom, (billings != butte & billings != helena & billings != missoula & billings != white_sulphur_springs & billings != st_pierre & butte != helena & butte != missoula & butte != white_sulphur_springs & butte != st_pierre & helena != missoula & helena != white_sulphur_springs & helena != st_pierre & missoula != white_sulphur_springs & missoula != st_pierre & white_sulphur_springs != st_pierre)).\nfof(distinct_states, axiom, (montana != other_state)).\nfof(in_state_fact1, axiom, in_state(billings, montana)).\nfof(in_state_fact2, axiom, in_state(butte, montana)).\nfof(in_state_fact3, axiom, in_state(helena, montana)).\nfof(in_state_fact4, axiom, in_state(missoula, montana)).\nfof(same_state_ws_butte, axiom, ? [S] : (in_state(white_sulphur_springs, S) & in_state(butte, S))).\nfof(stpierre_not_montana, axiom, ~in_state(st_pierre, montana)).\nfof(any_city_in_butte_not_stpierre, axiom, ? [S] : (in_state(butte, S) & ! [C] : (in_state(C, S) => ~in_state(C, st_pierre)))).\nfof(uniqueness, axiom, ! [C,S1,S2] : ((in_state(C,S1) & in_state(C,S2) & C != bristol & C != texarkana & C != texhoma & C != union_city) => S1 = S2))).\nfof(goal, conjecture, in_state(missoula, montana)).",
  "neg_filename": "neg.p",
  "neg_code": "% Negative version\nfof(distinct_cities, axiom, (billings != butte & billings != helena & billings != missoula & billings != white_sulphur_springs & billings != st_pierre & butte != helena & butte != missoula & butte != white_sulphur_springs & butte != st_pierre & helena != missoula & helena != white_sulphur_springs & helena != st_pierre & missoula != white_sulphur_springs & missoula != st_pierre & white_sulphur_springs != st_pierre)).\nfof(distinct_states, axiom, (montana != other_state)).\nfof(in_state_fact1, axiom, in_state(billings, montana)).\nfof(in_state_fact2, axiom, in_state(butte, montana)).\nfof(in_state_fact3, axiom, in_state(helena, montana)).\nfof(in_state_fact4, axiom, in_state(missoula, montana)).\nfof(same_state_ws_butte, axiom, ? [S] : (in_state(white_sulphur_springs, S) & in_state(butte, S))).\nfof(stpierre_not_montana, axiom, ~in_state(st_pierre, montana)).\nfof(any_city_in_butte_not_stpierre, axiom, ? [S] : (in_state(butte, S) & ! [C] : (in_state(C, S) => ~in_state(C, st_pierre)))).\nfof(uniqueness, axiom, ! [C,S1,S2] : ((in_state(C,S1) & in_state(C,S2) & C != bristol & C != texarkana & C != texhoma & C != union_city) => S1 = S2))).\nfof(goal, conjecture, ~in_state(missoula, montana))."
}

#### Result

[{'type': 'text', 'text': '{"positive":{"status":"error","szs_status":"Unknown","stdout":"% Failed with\\n% parse error in \\"\\", line 20: . expected (text: ))\\n% Trying SMTLIB2\\nParser exception: unmatched right parenthesis in line 11 at )","stderr":"","returncode":4},"negative":{"status":"error","szs_status":"Unknown","stdout":"% Failed with\\n% parse error in \\"\\", line 20: . expected (text: ))\\n% Trying SMTLIB2\\nParser exception: unmatched right parenthesis in line 11 at )","stderr":"","returncode":4}}', 'id': 'lc_18f5ee92-e38a-45ed-8b1e-9da8fd4e7ec7'}]


## Iteration 2



### Thinking

- The tool returned parse errors due to syntax errors. Need to fix TPTP code.
- Issues: In distinct_cities axiom, we used many != combined with & but need parentheses around each inequality? Actually syntax: (a != b & a != c) is fine. But we used many & inside parentheses; okay.
- But parse error line 20: likely due to extra parentheses or missing period. Let's examine code.
- Positive code:
- ``` % Positive version fof(distinct_cities, axiom, (billings != butte & billings != helena & billings != missoula & billings != white_sulphur_springs & billings != st_pierre & butte != helena & butte != missoula & butte != white_sulphur_springs & butte != st_pierre & helena != missoula & helena != white_sulphur_springs & helena != st_pierre & missoula != white_sulphur_springs & missoula != st_pierre & white_sulphur_springs != st_pierre)). fof(distinct_states, axiom, (montana != other_state)). fof(in_state_fact1, axiom, in_state(billings, montana)). fof(in_state_fact2, axiom, in_state(butte, montana)). fof(in_state_fact3, axiom, in_state(helena, montana)). fof(in_state_fact4, axiom, in_state(missoula, montana)). fof(same_state_ws_butte, axiom, ? [S] : (in_state(white_sulphur_springs, S) & in_state(butte, S))). fof(stpierre_not_montana, axiom, ~in_state(st_pierre, montana)). fof(any_city_in_butte_not_stpierre, axiom, ? [S] : (in_state(butte, S) & ! [C] : (in_state(C, S) => ~in_state(C, st_pierre)))). fof(uniqueness, axiom, ! [C,S1,S2] : ((in_state(C,S1) & in_state(C,S2) & C != bristol & C != texarkana & C != texhoma & C != union_city) => S1 = S2))). fof(goal, conjecture, in_state(missoula, montana)). ```
- I see extra closing parenthesis before period in uniqueness line: we have ... => S1 = S2))) . Actually we have three closing parentheses before period, but opening parentheses count? Let's count: ! [C,S1,S2] : ((in_state(C,S1) & in_state(C,S2) & C != bristol & C != texarkana & C != texhoma & C != union_city) => S1 = S2))) . The outermost fof(...). So we need one closing parenthesis for the formula, then period. The formula starts after comma: ! [C,S1,S2] : ((... ) => S1 = S2) . So we need one closing parenthesis after S2). So we have too many. Should be:
- fof(uniqueness, axiom, ! [C,S1,S2] : ((in_state(C,S1) & in_state(C,S2) & C != bristol & C != texarkana & C != texhoma & C != union_city) => S1 = S2)).
- Also distinct_states maybe unnecessary but fine.
- Also we used distinct_states with other_state not defined; we could drop that or define other_state constant. Could cause unknown constant but okay.
- Also we used "white_sulphur_springs" with underscores; fine.
- Also we used "st_pierre" constant.
- We also used "bristol", "texarkana", "texhoma", "union_city" not defined; but they appear only in uniqueness condition; they are constants; we may need distinctness axioms for them? Not required but okay.
- But we also used "other_state" constant not defined; we can remove distinct_states axiom entirely.
- Simplify: remove distinct_states.
- Also we used "any_city_in_butte_not_stpierre" axiom: we attempted to encode "Any city in Butte is not in St Pierre." Actually premise: "Any city in Butte is not in St Pierre." Means for all city C, if in_state(C, butte) ??? Wait "city in Butte" ambiguous: Butte is a city, not a state. The premise likely means "Any city in the state of Montana that is Butte"? Actually phrase "Any city in Butte is not in St Pierre." Could be interpreted as: For any city C, if C is in the same state as Butte, then C is not in St Pierre. But we already have a rule about same state: "White Sulphur Springs and Butte are cities in the same state in U.S." So they share a state. The premise "Any city in Butte is not in St Pierre." Might be: any city that is in the same state as Butte is not in St Pierre. So we can encode: ! [C] : (in_state(C, S) & in_state(butte, S) => ~in_state(C, st_pierre)). But we need existential for S? Could use: ! [C,S] : ((in_state(C,S) & in_state(butte,S)) => ~in_state(C, st_pierre)). That's simpler.
- Let's encode that.
- Also we need to ensure uniqueness rule: a city can only be in one state except for those four cities. So we encode: ! [C,S1,S2] : ((in_state(C,S1) & in_state(C,S2) & C != bristol & C != texarkana & C != texhoma & C != union_city) => S1 = S2).
- Now we need to include the premise "The state of Montana includes the cities of Butte, Helena, and Missoula." Already encoded via in_state facts.
- Also "White Sulphur Springs and Butte are cities in the same state in U.S." encoded via existence of a state S where both are in S. That's fine.
- Now we need to ensure we have distinctness for cities maybe not needed but okay.
- Now we need to produce both positive and negative versions.
- Let's rewrite both codes correctly.




### TOKEN USAGE - Iteration 2

  Input tokens:  6,042
  Output tokens: 2,254
  Total tokens:  8,296

### Tool Call: write_and_run_vampire

  Args: {
  "pos_filename": "pos.p",
  "pos_code": "% Positive version\nfof(distinct_cities, axiom, (billings != butte & billings != helena & billings != missoula & billings != white_sulphur_springs & billings != st_pierre & butte != helena & butte != missoula & butte != white_sulphur_springs & butte != st_pierre & helena != missoula & helena != white_sulphur_springs & helena != st_pierre & missoula != white_sulphur_springs & missoula != st_pierre & white_sulphur_springs != st_pierre)).\nfof(in_state_fact1, axiom, in_state(billings, montana)).\nfof(in_state_fact2, axiom, in_state(butte, montana)).\nfof(in_state_fact3, axiom, in_state(helena, montana)).\nfof(in_state_fact4, axiom, in_state(missoula, montana)).\nfof(same_state_ws_butte, axiom, ? [S] : (in_state(white_sulphur_springs, S) & in_state(butte, S))).\nfof(stpierre_not_montana, axiom, ~in_state(st_pierre, montana)).\nfof(any_city_in_butte_not_stpierre, axiom, ! [C,S] : ((in_state(C,S) & in_state(butte,S)) => ~in_state(C, st_pierre))).\nfof(uniqueness, axiom, ! [C,S1,S2] : ((in_state(C,S1) & in_state(C,S2) & C != bristol & C != texarkana & C != texhoma & C != union_city) => S1 = S2)).\nfof(goal, conjecture, in_state(missoula, montana)).",
  "neg_filename": "neg.p",
  "neg_code": "% Negative version\nfof(distinct_cities, axiom, (billings != butte & billings != helena & billings != missoula & billings != white_sulphur_springs & billings != st_pierre & butte != helena & butte != missoula & butte != white_sulphur_springs & butte != st_pierre & helena != missoula & helena != white_sulphur_springs & helena != st_pierre & missoula != white_sulphur_springs & missoula != st_pierre & white_sulphur_springs != st_pierre)).\nfof(in_state_fact1, axiom, in_state(billings, montana)).\nfof(in_state_fact2, axiom, in_state(butte, montana)).\nfof(in_state_fact3, axiom, in_state(helena, montana)).\nfof(in_state_fact4, axiom, in_state(missoula, montana)).\nfof(same_state_ws_butte, axiom, ? [S] : (in_state(white_sulphur_springs, S) & in_state(butte, S))).\nfof(stpierre_not_montana, axiom, ~in_state(st_pierre, montana)).\nfof(any_city_in_butte_not_stpierre, axiom, ! [C,S] : ((in_state(C,S) & in_state(butte,S)) => ~in_state(C, st_pierre))).\nfof(uniqueness, axiom, ! [C,S1,S2] : ((in_state(C,S1) & in_state(C,S2) & C != bristol & C != texarkana & C != texhoma & C != union_city) => S1 = S2)).\nfof(goal, conjecture, ~in_state(missoula, montana))."
}

#### Result

[{'type': 'text', 'text': '{"positive":{"status":"success","szs_status":"Theorem","stdout":"% Refutation found. Thanks to Tanya!\\n% SZS status Theorem for pos\\n% SZS output start Proof for pos\\n5. in_state(missoula,montana) [input(axiom)]\\n10. in_state(missoula,montana) [input(conjecture)]\\n11. ~in_state(missoula,montana) [negated conjecture 10]\\n12. ~in_state(missoula,montana) [flattening 11]\\n37. in_state(missoula,montana) [cnf transformation 5]\\n43. ~in_state(missoula,montana) [cnf transformation 12]\\n44. $false [forward subsumption resolution 37,43]\\n% SZS output end Proof for pos\\n% Termination reason: Refutation","stderr":null,"returncode":0},"negative":{"status":"success","szs_status":"CounterSatisfiable","stdout":"% SZS status CounterSatisfiable for neg\\n% SZS output start Saturation.\\ncnf(u59,axiom,\\n    white_sulphur_springs = texhoma).\\n\\ncnf(u74,axiom,\\n    butte != union_city).\\n\\ncnf(u78,axiom,\\n    butte != texhoma).\\n\\ncnf(u83,axiom,\\n    butte = texarkana).\\n\\ncnf(u94,negated_conjecture,\\n    missoula != union_city).\\n\\ncnf(u98,negated_conjecture,\\n    missoula != texhoma).\\n\\ncnf(u102,negated_conjecture,\\n    missoula != texarkana).\\n\\ncnf(u107,negated_conjecture,\\n    missoula = bristol).\\n\\ncnf(u114,axiom,\\n    helena != union_city).\\n\\ncnf(u118,axiom,\\n    helena != texhoma).\\n\\ncnf(u122,axiom,\\n    helena != texarkana).\\n\\ncnf(u126,axiom,\\n    helena != bristol).\\n\\ncnf(u130,axiom,\\n    ~in_state(helena,X0) | montana = X0).\\n\\ncnf(u139,axiom,\\n    billings = union_city).\\n\\ncnf(u33,axiom,\\n    billings != butte).\\n\\ncnf(u30,axiom,\\n    billings != white_sulphur_springs).\\n\\ncnf(u23,axiom,\\n    helena != white_sulphur_springs).\\n\\ncnf(u42,axiom,\\n    ~in_state(X0,X2) | ~in_state(X0,X1) | X1 = X2 | bristol = X0 | texarkana = X0 | texhoma = X0 | union_city = X0).\\n\\ncnf(u35,axiom,\\n    in_state(butte,montana)).\\n\\ncnf(u24,axiom,\\n    helena != missoula).\\n\\ncnf(u45,axiom,\\n    ~in_state(X0,sK0) | ~in_state(X0,st_pierre)).\\n\\ncnf(u26,axiom,\\n    butte != white_sulphur_springs).\\n\\ncnf(u19,axiom,\\n    white_sulphur_springs != st_pierre).\\n\\ncnf(u36,axiom,\\n    in_state(helena,montana)).\\n\\ncnf(u29,axiom,\\n    billings != st_pierre).\\n\\ncnf(u212,axiom,\\n    ~in_state(billings,st_pierre)).\\n\\ncnf(u41,axiom,\\n    ~in_state(butte,X1) | ~in_state(X0,X1) | ~in_state(X0,st_pierre)).\\n\\ncnf(u38,axiom,\\n    in_state(butte,sK0)).\\n\\ncnf(u31,axiom,\\n    billings != missoula).\\n\\ncnf(u217,axiom,\\n    ~in_state(white_sulphur_springs,st_pierre)).\\n\\ncnf(u214,axiom,\\n    ~in_state(helena,st_pierre)).\\n\\ncnf(u20,axiom,\\n    missoula != st_pierre).\\n\\ncnf(u43,negated_conjecture,\\n    in_state(missoula,montana)).\\n\\ncnf(u32,axiom,\\n    billings != helena).\\n\\ncnf(u25,axiom,\\n    butte != st_pierre).\\n\\ncnf(u22,axiom,\\n    helena != st_pierre).\\n\\ncnf(u34,axiom,\\n    in_state(billings,montana)).\\n\\ncnf(u27,axiom,\\n    butte != missoula).\\n\\ncnf(u44,axiom,\\n    ~in_state(X0,montana) | ~in_state(X0,st_pierre)).\\n\\ncnf(u213,axiom,\\n    ~in_state(butte,st_pierre)).\\n\\ncnf(u39,axiom,\\n    in_state(white_sulphur_springs,sK0)).\\n\\ncnf(u28,axiom,\\n    butte != helena).\\n\\ncnf(u21,axiom,\\n    missoula != white_sulphur_springs).\\n\\ncnf(u40,axiom,\\n    ~in_state(st_pierre,montana)).\\n\\ncnf(u215,negated_conjecture,\\n    ~in_state(missoula,st_pierre)).\\n\\n% SZS output end Saturation.\\n% SZS output start Definitions and Model Updates.\\n% SZS output end Definitions and Model Updates.\\n% Termination reason: Satisfiable","stderr":null,"returncode":0}}', 'id': 'lc_51368efe-f6ec-4c05-af04-c191960b54fc'}]


[NOTE] Skipping Answer Phase for FOLIO benchmark as solver returns verdict directly.

TOKEN USAGE SUMMARY
  Total input tokens:  10,954
  Total output tokens: 4,138
  Total tokens:        15,092

COMPLETE

## Final Answer

```json
[{'type': 'text', 'text': '{"positive":{"status":"success","szs_status":"Theorem","stdout":"% Refutation found. Thanks to Tanya!\\n% SZS status Theorem for pos\\n% SZS output start Proof for pos\\n5. in_state(missoula,montana) [input(axiom)]\\n10. in_state(missoula,montana) [input(conjecture)]\\n11. ~in_state(missoula,montana) [negated conjecture 10]\\n12. ~in_state(missoula,montana) [flattening 11]\\n37. in_state(missoula,montana) [cnf transformation 5]\\n43. ~in_state(missoula,montana) [cnf transformation 12]\\n44. $false [forward subsumption resolution 37,43]\\n% SZS output end Proof for pos\\n% Termination reason: Refutation","stderr":null,"returncode":0},"negative":{"status":"success","szs_status":"CounterSatisfiable","stdout":"% SZS status CounterSatisfiable for neg\\n% SZS output start Saturation.\\ncnf(u59,axiom,\\n    white_sulphur_springs = texhoma).\\n\\ncnf(u74,axiom,\\n    butte != union_city).\\n\\ncnf(u78,axiom,\\n    butte != texhoma).\\n\\ncnf(u83,axiom,\\n    butte = texarkana).\\n\\ncnf(u94,negated_conjecture,\\n    missoula != union_city).\\n\\ncnf(u98,negated_conjecture,\\n    missoula != texhoma).\\n\\ncnf(u102,negated_conjecture,\\n    missoula != texarkana).\\n\\ncnf(u107,negated_conjecture,\\n    missoula = bristol).\\n\\ncnf(u114,axiom,\\n    helena != union_city).\\n\\ncnf(u118,axiom,\\n    helena != texhoma).\\n\\ncnf(u122,axiom,\\n    helena != texarkana).\\n\\ncnf(u126,axiom,\\n    helena != bristol).\\n\\ncnf(u130,axiom,\\n    ~in_state(helena,X0) | montana = X0).\\n\\ncnf(u139,axiom,\\n    billings = union_city).\\n\\ncnf(u33,axiom,\\n    billings != butte).\\n\\ncnf(u30,axiom,\\n    billings != white_sulphur_springs).\\n\\ncnf(u23,axiom,\\n    helena != white_sulphur_springs).\\n\\ncnf(u42,axiom,\\n    ~in_state(X0,X2) | ~in_state(X0,X1) | X1 = X2 | bristol = X0 | texarkana = X0 | texhoma = X0 | union_city = X0).\\n\\ncnf(u35,axiom,\\n    in_state(butte,montana)).\\n\\ncnf(u24,axiom,\\n    helena != missoula).\\n\\ncnf(u45,axiom,\\n    ~in_state(X0,sK0) | ~in_state(X0,st_pierre)).\\n\\ncnf(u26,axiom,\\n    butte != white_sulphur_springs).\\n\\ncnf(u19,axiom,\\n    white_sulphur_springs != st_pierre).\\n\\ncnf(u36,axiom,\\n    in_state(helena,montana)).\\n\\ncnf(u29,axiom,\\n    billings != st_pierre).\\n\\ncnf(u212,axiom,\\n    ~in_state(billings,st_pierre)).\\n\\ncnf(u41,axiom,\\n    ~in_state(butte,X1) | ~in_state(X0,X1) | ~in_state(X0,st_pierre)).\\n\\ncnf(u38,axiom,\\n    in_state(butte,sK0)).\\n\\ncnf(u31,axiom,\\n    billings != missoula).\\n\\ncnf(u217,axiom,\\n    ~in_state(white_sulphur_springs,st_pierre)).\\n\\ncnf(u214,axiom,\\n    ~in_state(helena,st_pierre)).\\n\\ncnf(u20,axiom,\\n    missoula != st_pierre).\\n\\ncnf(u43,negated_conjecture,\\n    in_state(missoula,montana)).\\n\\ncnf(u32,axiom,\\n    billings != helena).\\n\\ncnf(u25,axiom,\\n    butte != st_pierre).\\n\\ncnf(u22,axiom,\\n    helena != st_pierre).\\n\\ncnf(u34,axiom,\\n    in_state(billings,montana)).\\n\\ncnf(u27,axiom,\\n    butte != missoula).\\n\\ncnf(u44,axiom,\\n    ~in_state(X0,montana) | ~in_state(X0,st_pierre)).\\n\\ncnf(u213,axiom,\\n    ~in_state(butte,st_pierre)).\\n\\ncnf(u39,axiom,\\n    in_state(white_sulphur_springs,sK0)).\\n\\ncnf(u28,axiom,\\n    butte != helena).\\n\\ncnf(u21,axiom,\\n    missoula != white_sulphur_springs).\\n\\ncnf(u40,axiom,\\n    ~in_state(st_pierre,montana)).\\n\\ncnf(u215,negated_conjecture,\\n    ~in_state(missoula,st_pierre)).\\n\\n% SZS output end Saturation.\\n% SZS output start Definitions and Model Updates.\\n% SZS output end Definitions and Model Updates.\\n% Termination reason: Satisfiable","stderr":null,"returncode":0}}', 'id': 'lc_51368efe-f6ec-4c05-af04-c191960b54fc'}]
```
