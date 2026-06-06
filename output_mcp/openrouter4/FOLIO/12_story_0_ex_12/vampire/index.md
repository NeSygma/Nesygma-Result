# Benchmark Report (MCP): FOLIO - story_0_ex_12

**Provider:** openrouter4
**Model:** deepseek/deepseek-v4-flash
**Solver:** vampire
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: high
**Duration:** 45.63s


 MCP VAMPIRE AGENT - Symbolic Reasoning

### Query
Consider the following logical premises: There are six types of wild turkeys: Eastern wild turkey,

Osceola wild turkey, Gould’s wild turkey, Merriam’s wild turkey, Rio Grande wild turkey, and
Ocellated wild turkey. Tom is not an Eastern wild turkey. Tom is not an Osceola wild turkey. Tom is
not a Gould's wild turkey. Tom is neither a Merriam's wild turkey nor a Rio Grande wild turkey. Tom
is a wild turkey. Conclusion to evaluate: Joey is a wild turkey. Question: Based STRICTLY on the
premises, is the conclusion True, False, or Uncertain? Return your final answer in JSON format like
this: {"Conclusion": "True or False or Uncertain in here"}

  - write_and_run_vampire: Write two TPTP problem files (positive claim and negation) and run Vampire 
on both concurrently to get proof results for both in one iteration.
Returns a dictionary with 'positive' and 'negative' result objects.

## Iteration 1



### Thinking

- Let me analyze this problem carefully.
- We have premises: 1. There are six types of wild turkeys: Eastern, Osceola, Gould's, Merriam's, Rio Grande, and Ocellated. 2. Tom is not an Eastern wild turkey. 3. Tom is not an Osceola wild turkey. 4. Tom is not a Gould's wild turkey. 5. Tom is neither a Merriam's wild turkey nor a Rio Grande wild turkey. 6. Tom is a wild turkey.
- Conclusion: Joey is a wild turkey.
- The problem asks: Based strictly on the premises, is the conclusion True, False, or Uncertain?
- Let me think about what the premises tell us:
- - There are exactly 6 types of wild turkeys. - Tom is a wild turkey. - Tom is not Eastern, not Osceola, not Gould's, not Merriam's, not Rio Grande. - So by elimination, Tom must be an Ocellated wild turkey (since those are the only 6 types and Tom is a wild turkey).
- But crucially, there is NO information about Joey at all in the premises. The premises only talk about Tom and the types of wild turkeys. We cannot infer anything about Joey from these premises.
- So the conclusion "Joey is a wild turkey" is uncertain - we don't have enough information to determine if it's true or false.
- Let me formalize this in TPTP.
- I need predicates: - `wild_turkey(X)` - X is a wild turkey - For the types: `eastern(X)`, `osceola(X)`, `goulds(X)`, `merriams(X)`, `rio_grande(X)`, `ocellated(X)`
- Actually, let me think about this differently. The premise says there are six types of wild turkeys. This means every wild turkey is one of these six types.
- So: 1. Every wild turkey is one of the six types. 2. Tom is a wild turkey. 3. Tom is NOT eastern, osceola, goulds, merriams, rio_grande. 4. Therefore Tom must be ocellated.
- But we have NO info about Joey.
- Let me encode this carefully.
- Actually, I need to think about what the six types means. It means: - If something is a wild turkey, then it is one of these six types. - Each type implies being a wild turkey? Not necessarily - but typically a type of wild turkey IS a wild turkey.
- Let me keep it simple:
- Axioms: 1. `eastern(X) => wild_turkey(X)` etc. (each type implies wild turkey) 2. `wild_turkey(X) => (eastern(X) | osceola(X) | goulds(X) | merriams(X) | rio_grande(X) | ocellated(X))` (every wild turkey is one of the six types) 3. `~eastern(tom)` 4. `~osceola(tom)` 5. `~goulds(tom)` 6. `~merriams(tom)` 7. `~rio_grande(tom)` 8. `wild_turkey(tom)`
- Conclusion: `wild_turkey(joey)`
- The question is: does this conclusion follow from the premises?
- Clearly not - there's no information about Joey. So the conclusion is Uncertain.
- But wait, I also need to think about the negative test. The negation of the conclusion is `~wild_turkey(joey)`. This also doesn't follow from the premises.
- So both the positive and negative should be CounterSatisfiable (or Satisfiable) - the axioms don't entail either claim about Joey.
- Let me also add pairwise distinctness for the types to make it clean.
- Actually, for the types, I need to think if they are mutually exclusive. A wild turkey can only be one type. Let me add that too.
- Let me write the TPTP code now.


Looking at this problem:

**Premises:**
1. Six types of wild turkeys exist (Eastern, Osceola, Gould's, Merriam's, Rio Grande, Ocellated).
2. Tom is a wild turkey.
3. Tom is not Eastern, not Osceola, not Gould's, not Merriam's, not Rio Grande.
4. (By elimination, Tom must be Ocellated.)

**Conclusion:** Joey is a wild turkey.

**Key observation:** There is zero information about Joey. The conclusion cannot be proven true nor false from the given premises alone. It is **Uncertain**.

Let me encode this in TPTP and test both sides.

### TOKEN USAGE - Iteration 1

  Input tokens:  5,091
  Output tokens: 2,844
  Total tokens:  7,935

### Tool Call: write_and_run_vampire

  Args: {
  "pos_filename": "wild_turkey_pos.p",
  "pos_code": "% Positive test: is \"Joey is a wild turkey\" entailed?\n% Six types of wild turkeys\nfof(type_eastern, axiom, ! [X] : (eastern(X) => wild_turkey(X))).\nfof(type_osceola, axiom, ! [X] : (osceola(X) => wild_turkey(X))).\nfof(type_goulds, axiom, ! [X] : (goulds(X) => wild_turkey(X))).\nfof(type_merriams, axiom, ! [X] : (merriams(X) => wild_turkey(X))).\nfof(type_rio_grande, axiom, ! [X] : (rio_grande(X) => wild_turkey(X))).\nfof(type_ocellated, axiom, ! [X] : (ocellated(X) => wild_turkey(X))).\n\n% Every wild turkey belongs to one of the six types\nfof(wild_turkey_covered, axiom, ! [X] : (wild_turkey(X) =>\n    (eastern(X) | osceola(X) | goulds(X) | merriams(X) | rio_grande(X) | ocellated(X)))).\n\n% The six types are mutually exclusive (a bird is exactly one type)\nfof(mutual_excl_1, axiom, ! [X] : (eastern(X) => ~osceola(X))).\nfof(mutual_excl_2, axiom, ! [X] : (eastern(X) => ~goulds(X))).\nfof(mutual_excl_3, axiom, ! [X] : (eastern(X) => ~merriams(X))).\nfof(mutual_excl_4, axiom, ! [X] : (eastern(X) => ~rio_grande(X))).\nfof(mutual_excl_5, axiom, ! [X] : (eastern(X) => ~ocellated(X))).\nfof(mutual_excl_6, axiom, ! [X] : (osceola(X) => ~goulds(X))).\nfof(mutual_excl_7, axiom, ! [X] : (osceola(X) => ~merriams(X))).\nfof(mutual_excl_8, axiom, ! [X] : (osceola(X) => ~rio_grande(X))).\nfof(mutual_excl_9, axiom, ! [X] : (osceola(X) => ~ocellated(X))).\nfof(mutual_excl_10, axiom, ! [X] : (goulds(X) => ~merriams(X))).\nfof(mutual_excl_11, axiom, ! [X] : (goulds(X) => ~rio_grande(X))).\nfof(mutual_excl_12, axiom, ! [X] : (goulds(X) => ~ocellated(X))).\nfof(mutual_excl_13, axiom, ! [X] : (merriams(X) => ~rio_grande(X))).\nfof(mutual_excl_14, axiom, ! [X] : (merriams(X) => ~ocellated(X))).\nfof(mutual_excl_15, axiom, ! [X] : (rio_grande(X) => ~ocellated(X))).\n\n% Facts about Tom\nfof(tom_not_eastern, axiom, ~eastern(tom)).\nfof(tom_not_osceola, axiom, ~osceola(tom)).\nfof(tom_not_goulds, axiom, ~goulds(tom)).\nfof(tom_not_merriams, axiom, ~merriams(tom)).\nfof(tom_not_rio_grande, axiom, ~rio_grande(tom)).\nfof(tom_is_wild_turkey, axiom, wild_turkey(tom)).\n\n% Conclusion: Joey is a wild turkey\nfof(conclusion, conjecture, wild_turkey(joey)).\n",
  "neg_filename": "wild_turkey_neg.p",
  "neg_code": "% Negative test: is \"Joey is NOT a wild turkey\" entailed?\n% Six types of wild turkeys\nfof(type_eastern, axiom, ! [X] : (eastern(X) => wild_turkey(X))).\nfof(type_osceola, axiom, ! [X] : (osceola(X) => wild_turkey(X))).\nfof(type_goulds, axiom, ! [X] : (goulds(X) => wild_turkey(X))).\nfof(type_merriams, axiom, ! [X] : (merriams(X) => wild_turkey(X))).\nfof(type_rio_grande, axiom, ! [X] : (rio_grande(X) => wild_turkey(X))).\nfof(type_ocellated, axiom, ! [X] : (ocellated(X) => wild_turkey(X))).\n\n% Every wild turkey belongs to one of the six types\nfof(wild_turkey_covered, axiom, ! [X] : (wild_turkey(X) =>\n    (eastern(X) | osceola(X) | goulds(X) | merriams(X) | rio_grande(X) | ocellated(X)))).\n\n% The six types are mutually exclusive\nfof(mutual_excl_1, axiom, ! [X] : (eastern(X) => ~osceola(X))).\nfof(mutual_excl_2, axiom, ! [X] : (eastern(X) => ~goulds(X))).\nfof(mutual_excl_3, axiom, ! [X] : (eastern(X) => ~merriams(X))).\nfof(mutual_excl_4, axiom, ! [X] : (eastern(X) => ~rio_grande(X))).\nfof(mutual_excl_5, axiom, ! [X] : (eastern(X) => ~ocellated(X))).\nfof(mutual_excl_6, axiom, ! [X] : (osceola(X) => ~goulds(X))).\nfof(mutual_excl_7, axiom, ! [X] : (osceola(X) => ~merriams(X))).\nfof(mutual_excl_8, axiom, ! [X] : (osceola(X) => ~rio_grande(X))).\nfof(mutual_excl_9, axiom, ! [X] : (osceola(X) => ~ocellated(X))).\nfof(mutual_excl_10, axiom, ! [X] : (goulds(X) => ~merriams(X))).\nfof(mutual_excl_11, axiom, ! [X] : (goulds(X) => ~rio_grande(X))).\nfof(mutual_excl_12, axiom, ! [X] : (goulds(X) => ~ocellated(X))).\nfof(mutual_excl_13, axiom, ! [X] : (merriams(X) => ~rio_grande(X))).\nfof(mutual_excl_14, axiom, ! [X] : (merriams(X) => ~ocellated(X))).\nfof(mutual_excl_15, axiom, ! [X] : (rio_grande(X) => ~ocellated(X))).\n\n% Facts about Tom\nfof(tom_not_eastern, axiom, ~eastern(tom)).\nfof(tom_not_osceola, axiom, ~osceola(tom)).\nfof(tom_not_goulds, axiom, ~goulds(tom)).\nfof(tom_not_merriams, axiom, ~merriams(tom)).\nfof(tom_not_rio_grande, axiom, ~rio_grande(tom)).\nfof(tom_is_wild_turkey, axiom, wild_turkey(tom)).\n\n% Negated conclusion: Joey is NOT a wild turkey\nfof(neg_conclusion, conjecture, ~wild_turkey(joey)).\n"
}

#### Result

[{'type': 'text', 'text': '{"positive":{"status":"success","szs_status":"CounterSatisfiable","stdout":"% SZS status CounterSatisfiable for wild_turkey_pos\\n% SZS output start Saturation.\\ncnf(u61,axiom,\\n    ~wild_turkey(X0) | osceola(X0) | goulds(X0) | merriams(X0) | rio_grande(X0) | ocellated(X0) | eastern(X0)).\\n\\ncnf(u74,axiom,\\n    ~rio_grande(X0) | ~merriams(X0)).\\n\\ncnf(u67,axiom,\\n    ~goulds(X0) | ~osceola(X0)).\\n\\ncnf(u63,axiom,\\n    ~goulds(X0) | ~eastern(X0)).\\n\\ncnf(u77,axiom,\\n    ~eastern(tom)).\\n\\ncnf(u89,axiom,\\n    ocellated(tom)).\\n\\ncnf(u57,axiom,\\n    ~goulds(X0) | wild_turkey(X0)).\\n\\ncnf(u79,axiom,\\n    ~goulds(tom)).\\n\\ncnf(u68,axiom,\\n    ~merriams(X0) | ~osceola(X0)).\\n\\ncnf(u73,axiom,\\n    ~ocellated(X0) | ~goulds(X0)).\\n\\ncnf(u80,axiom,\\n    ~merriams(tom)).\\n\\ncnf(u59,axiom,\\n    ~rio_grande(X0) | wild_turkey(X0)).\\n\\ncnf(u70,axiom,\\n    ~ocellated(X0) | ~osceola(X0)).\\n\\ncnf(u82,axiom,\\n    wild_turkey(tom)).\\n\\ncnf(u75,axiom,\\n    ~ocellated(X0) | ~merriams(X0)).\\n\\ncnf(u64,axiom,\\n    ~merriams(X0) | ~eastern(X0)).\\n\\ncnf(u66,axiom,\\n    ~ocellated(X0) | ~eastern(X0)).\\n\\ncnf(u60,axiom,\\n    ~ocellated(X0) | wild_turkey(X0)).\\n\\ncnf(u76,axiom,\\n    ~ocellated(X0) | ~rio_grande(X0)).\\n\\ncnf(u69,axiom,\\n    ~rio_grande(X0) | ~osceola(X0)).\\n\\ncnf(u62,axiom,\\n    ~osceola(X0) | ~eastern(X0)).\\n\\ncnf(u55,axiom,\\n    ~eastern(X0) | wild_turkey(X0)).\\n\\ncnf(u81,axiom,\\n    ~rio_grande(tom)).\\n\\ncnf(u56,axiom,\\n    ~osceola(X0) | wild_turkey(X0)).\\n\\ncnf(u78,axiom,\\n    ~osceola(tom)).\\n\\ncnf(u71,axiom,\\n    ~merriams(X0) | ~goulds(X0)).\\n\\ncnf(u72,axiom,\\n    ~rio_grande(X0) | ~goulds(X0)).\\n\\ncnf(u83,negated_conjecture,\\n    ~wild_turkey(joey)).\\n\\ncnf(u58,axiom,\\n    ~merriams(X0) | wild_turkey(X0)).\\n\\ncnf(u65,axiom,\\n    ~rio_grande(X0) | ~eastern(X0)).\\n\\n% SZS output end Saturation.\\n% SZS output start Definitions and Model Updates.\\n% SZS output end Definitions and Model Updates.\\n% Termination reason: Satisfiable","stderr":null,"returncode":0},"negative":{"status":"success","szs_status":"CounterSatisfiable","stdout":"% SZS status CounterSatisfiable for wild_turkey_neg\\n% SZS output start Saturation.\\ncnf(u89,negated_conjecture,\\n    ~eastern(joey)).\\n\\ncnf(u94,negated_conjecture,\\n    ocellated(joey)).\\n\\ncnf(u97,negated_conjecture,\\n    ~rio_grande(joey)).\\n\\ncnf(u101,negated_conjecture,\\n    ~merriams(joey)).\\n\\ncnf(u105,negated_conjecture,\\n    ~goulds(joey)).\\n\\ncnf(u109,negated_conjecture,\\n    ~osceola(joey)).\\n\\ncnf(u61,axiom,\\n    ~wild_turkey(X0) | osceola(X0) | goulds(X0) | merriams(X0) | rio_grande(X0) | ocellated(X0) | eastern(X0)).\\n\\ncnf(u74,axiom,\\n    ~rio_grande(X0) | ~merriams(X0)).\\n\\ncnf(u67,axiom,\\n    ~goulds(X0) | ~osceola(X0)).\\n\\ncnf(u63,axiom,\\n    ~goulds(X0) | ~eastern(X0)).\\n\\ncnf(u77,axiom,\\n    ~eastern(tom)).\\n\\ncnf(u57,axiom,\\n    ~goulds(X0) | wild_turkey(X0)).\\n\\ncnf(u79,axiom,\\n    ~goulds(tom)).\\n\\ncnf(u68,axiom,\\n    ~merriams(X0) | ~osceola(X0)).\\n\\ncnf(u73,axiom,\\n    ~ocellated(X0) | ~goulds(X0)).\\n\\ncnf(u80,axiom,\\n    ~merriams(tom)).\\n\\ncnf(u59,axiom,\\n    ~rio_grande(X0) | wild_turkey(X0)).\\n\\ncnf(u70,axiom,\\n    ~ocellated(X0) | ~osceola(X0)).\\n\\ncnf(u82,axiom,\\n    wild_turkey(tom)).\\n\\ncnf(u75,axiom,\\n    ~ocellated(X0) | ~merriams(X0)).\\n\\ncnf(u64,axiom,\\n    ~merriams(X0) | ~eastern(X0)).\\n\\ncnf(u115,axiom,\\n    ocellated(tom)).\\n\\ncnf(u66,axiom,\\n    ~ocellated(X0) | ~eastern(X0)).\\n\\ncnf(u60,axiom,\\n    ~ocellated(X0) | wild_turkey(X0)).\\n\\ncnf(u76,axiom,\\n    ~ocellated(X0) | ~rio_grande(X0)).\\n\\ncnf(u69,axiom,\\n    ~rio_grande(X0) | ~osceola(X0)).\\n\\ncnf(u62,axiom,\\n    ~osceola(X0) | ~eastern(X0)).\\n\\ncnf(u55,axiom,\\n    ~eastern(X0) | wild_turkey(X0)).\\n\\ncnf(u81,axiom,\\n    ~rio_grande(tom)).\\n\\ncnf(u56,axiom,\\n    ~osceola(X0) | wild_turkey(X0)).\\n\\ncnf(u78,axiom,\\n    ~osceola(tom)).\\n\\ncnf(u71,axiom,\\n    ~merriams(X0) | ~goulds(X0)).\\n\\ncnf(u72,axiom,\\n    ~rio_grande(X0) | ~goulds(X0)).\\n\\ncnf(u83,negated_conjecture,\\n    wild_turkey(joey)).\\n\\ncnf(u58,axiom,\\n    ~merriams(X0) | wild_turkey(X0)).\\n\\ncnf(u65,axiom,\\n    ~rio_grande(X0) | ~eastern(X0)).\\n\\n% SZS output end Saturation.\\n% SZS output start Definitions and Model Updates.\\n% SZS output end Definitions and Model Updates.\\n% Termination reason: Satisfiable","stderr":null,"returncode":0}}', 'id': 'lc_e4c78170-6180-4cb8-96c3-0383d34b9032'}]


[NOTE] Skipping Answer Phase for FOLIO benchmark as solver returns verdict directly.

TOKEN USAGE SUMMARY
  Total input tokens:  5,091
  Total output tokens: 2,844
  Total tokens:        7,935

COMPLETE

## Final Answer

```json
[{'type': 'text', 'text': '{"positive":{"status":"success","szs_status":"CounterSatisfiable","stdout":"% SZS status CounterSatisfiable for wild_turkey_pos\\n% SZS output start Saturation.\\ncnf(u61,axiom,\\n    ~wild_turkey(X0) | osceola(X0) | goulds(X0) | merriams(X0) | rio_grande(X0) | ocellated(X0) | eastern(X0)).\\n\\ncnf(u74,axiom,\\n    ~rio_grande(X0) | ~merriams(X0)).\\n\\ncnf(u67,axiom,\\n    ~goulds(X0) | ~osceola(X0)).\\n\\ncnf(u63,axiom,\\n    ~goulds(X0) | ~eastern(X0)).\\n\\ncnf(u77,axiom,\\n    ~eastern(tom)).\\n\\ncnf(u89,axiom,\\n    ocellated(tom)).\\n\\ncnf(u57,axiom,\\n    ~goulds(X0) | wild_turkey(X0)).\\n\\ncnf(u79,axiom,\\n    ~goulds(tom)).\\n\\ncnf(u68,axiom,\\n    ~merriams(X0) | ~osceola(X0)).\\n\\ncnf(u73,axiom,\\n    ~ocellated(X0) | ~goulds(X0)).\\n\\ncnf(u80,axiom,\\n    ~merriams(tom)).\\n\\ncnf(u59,axiom,\\n    ~rio_grande(X0) | wild_turkey(X0)).\\n\\ncnf(u70,axiom,\\n    ~ocellated(X0) | ~osceola(X0)).\\n\\ncnf(u82,axiom,\\n    wild_turkey(tom)).\\n\\ncnf(u75,axiom,\\n    ~ocellated(X0) | ~merriams(X0)).\\n\\ncnf(u64,axiom,\\n    ~merriams(X0) | ~eastern(X0)).\\n\\ncnf(u66,axiom,\\n    ~ocellated(X0) | ~eastern(X0)).\\n\\ncnf(u60,axiom,\\n    ~ocellated(X0) | wild_turkey(X0)).\\n\\ncnf(u76,axiom,\\n    ~ocellated(X0) | ~rio_grande(X0)).\\n\\ncnf(u69,axiom,\\n    ~rio_grande(X0) | ~osceola(X0)).\\n\\ncnf(u62,axiom,\\n    ~osceola(X0) | ~eastern(X0)).\\n\\ncnf(u55,axiom,\\n    ~eastern(X0) | wild_turkey(X0)).\\n\\ncnf(u81,axiom,\\n    ~rio_grande(tom)).\\n\\ncnf(u56,axiom,\\n    ~osceola(X0) | wild_turkey(X0)).\\n\\ncnf(u78,axiom,\\n    ~osceola(tom)).\\n\\ncnf(u71,axiom,\\n    ~merriams(X0) | ~goulds(X0)).\\n\\ncnf(u72,axiom,\\n    ~rio_grande(X0) | ~goulds(X0)).\\n\\ncnf(u83,negated_conjecture,\\n    ~wild_turkey(joey)).\\n\\ncnf(u58,axiom,\\n    ~merriams(X0) | wild_turkey(X0)).\\n\\ncnf(u65,axiom,\\n    ~rio_grande(X0) | ~eastern(X0)).\\n\\n% SZS output end Saturation.\\n% SZS output start Definitions and Model Updates.\\n% SZS output end Definitions and Model Updates.\\n% Termination reason: Satisfiable","stderr":null,"returncode":0},"negative":{"status":"success","szs_status":"CounterSatisfiable","stdout":"% SZS status CounterSatisfiable for wild_turkey_neg\\n% SZS output start Saturation.\\ncnf(u89,negated_conjecture,\\n    ~eastern(joey)).\\n\\ncnf(u94,negated_conjecture,\\n    ocellated(joey)).\\n\\ncnf(u97,negated_conjecture,\\n    ~rio_grande(joey)).\\n\\ncnf(u101,negated_conjecture,\\n    ~merriams(joey)).\\n\\ncnf(u105,negated_conjecture,\\n    ~goulds(joey)).\\n\\ncnf(u109,negated_conjecture,\\n    ~osceola(joey)).\\n\\ncnf(u61,axiom,\\n    ~wild_turkey(X0) | osceola(X0) | goulds(X0) | merriams(X0) | rio_grande(X0) | ocellated(X0) | eastern(X0)).\\n\\ncnf(u74,axiom,\\n    ~rio_grande(X0) | ~merriams(X0)).\\n\\ncnf(u67,axiom,\\n    ~goulds(X0) | ~osceola(X0)).\\n\\ncnf(u63,axiom,\\n    ~goulds(X0) | ~eastern(X0)).\\n\\ncnf(u77,axiom,\\n    ~eastern(tom)).\\n\\ncnf(u57,axiom,\\n    ~goulds(X0) | wild_turkey(X0)).\\n\\ncnf(u79,axiom,\\n    ~goulds(tom)).\\n\\ncnf(u68,axiom,\\n    ~merriams(X0) | ~osceola(X0)).\\n\\ncnf(u73,axiom,\\n    ~ocellated(X0) | ~goulds(X0)).\\n\\ncnf(u80,axiom,\\n    ~merriams(tom)).\\n\\ncnf(u59,axiom,\\n    ~rio_grande(X0) | wild_turkey(X0)).\\n\\ncnf(u70,axiom,\\n    ~ocellated(X0) | ~osceola(X0)).\\n\\ncnf(u82,axiom,\\n    wild_turkey(tom)).\\n\\ncnf(u75,axiom,\\n    ~ocellated(X0) | ~merriams(X0)).\\n\\ncnf(u64,axiom,\\n    ~merriams(X0) | ~eastern(X0)).\\n\\ncnf(u115,axiom,\\n    ocellated(tom)).\\n\\ncnf(u66,axiom,\\n    ~ocellated(X0) | ~eastern(X0)).\\n\\ncnf(u60,axiom,\\n    ~ocellated(X0) | wild_turkey(X0)).\\n\\ncnf(u76,axiom,\\n    ~ocellated(X0) | ~rio_grande(X0)).\\n\\ncnf(u69,axiom,\\n    ~rio_grande(X0) | ~osceola(X0)).\\n\\ncnf(u62,axiom,\\n    ~osceola(X0) | ~eastern(X0)).\\n\\ncnf(u55,axiom,\\n    ~eastern(X0) | wild_turkey(X0)).\\n\\ncnf(u81,axiom,\\n    ~rio_grande(tom)).\\n\\ncnf(u56,axiom,\\n    ~osceola(X0) | wild_turkey(X0)).\\n\\ncnf(u78,axiom,\\n    ~osceola(tom)).\\n\\ncnf(u71,axiom,\\n    ~merriams(X0) | ~goulds(X0)).\\n\\ncnf(u72,axiom,\\n    ~rio_grande(X0) | ~goulds(X0)).\\n\\ncnf(u83,negated_conjecture,\\n    wild_turkey(joey)).\\n\\ncnf(u58,axiom,\\n    ~merriams(X0) | wild_turkey(X0)).\\n\\ncnf(u65,axiom,\\n    ~rio_grande(X0) | ~eastern(X0)).\\n\\n% SZS output end Saturation.\\n% SZS output start Definitions and Model Updates.\\n% SZS output end Definitions and Model Updates.\\n% Termination reason: Satisfiable","stderr":null,"returncode":0}}', 'id': 'lc_e4c78170-6180-4cb8-96c3-0383d34b9032'}]
```
