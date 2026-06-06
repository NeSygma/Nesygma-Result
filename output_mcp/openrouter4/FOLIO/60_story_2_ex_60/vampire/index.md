# Benchmark Report (MCP): FOLIO - story_2_ex_60

**Provider:** openrouter4
**Model:** deepseek/deepseek-v4-flash
**Solver:** vampire
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: high
**Duration:** 77.71s


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

- Let me analyze the problem carefully.
- First, let me understand the premises:
- 1. Billings is a city in the state of Montana in U.S. 2. The state of Montana includes the cities of Butte, Helena, and Missoula. 3. White Sulphur Springs and Butte are cities in the same state in U.S. 4. The city of St Pierre is not in the state of Montana. 5. Any city in Butte is not in St Pierre.  (This one is weird - "Any city in Butte" - Butte is a city, so this might mean something like "any city located in Butte" or it could be a typo. Let me re-read... "Any city in Butte is not in St Pierre." - This probably means "Butte is not in St Pierre" or "any city that is Butte is not St Pierre." Actually, I think this means Butte is not the same city as St Pierre.)
- Wait, let me re-read: "Any city in Butte is not in St Pierre." This is confusing. Butte is a city, so "city in Butte" doesn't make sense unless Butte is also a region. Let me think... maybe "Any city in Butte" means "any city named Butte" or "the city Butte is not in St Pierre" - meaning Butte is not located within St Pierre. But that also doesn't make much sense since they're both cities.
- Actually, I think the most natural reading is: "The city of Butte is not the same city as St Pierre" or "Butte is not located in St Pierre." Let me go with: Butte and St Pierre are distinct cities, and Butte is not in St Pierre.
- Hmm, actually maybe a simpler reading: "Any city in Butte is not in St Pierre" could mean "a city that is in Butte (the city) is not in St Pierre (the city)" - which doesn't make geographic sense for cities.
- I think the most reasonable interpretation is: "Butte is not St Pierre" - i.e., they're different cities. Actually on re-reading, I think "Any city in Butte" is awkward English and might mean "The city of Butte is not St Pierre."
- Let me look at premise 5 again: "Any city in Butte is not in St Pierre." - I think this means "No city that is located in [the area of] Butte is located in St Pierre" or more simply "Butte and St Pierre are different cities and one is not contained in the other."
- Actually, the simplest reading that makes sense: "The city of Butte is not the city of St Pierre" - they are distinct cities. Let me go with this interpretation.
- 6. A city can only be in one state in U.S. except for Bristol, Texarkana, Texhoma and Union City.
- Conclusion: Montana is home to the city of Missoula.
- So the premises explicitly say: "The state of Montana includes the cities of Butte, Helena, and Missoula."
- This directly says Missoula is in Montana. So the conclusion "Montana is home to the city of Missoula" is True based on premise 2.
- But wait, premise 6 says a city can only be in one state except for four specific cities. Since Missoula is not one of those exceptions, Missoula can only be in one state. And premise 2 says Montana includes Missoula.
- So the conclusion seems straightforwardly true.
- Let me formalize this in TPTP.
- Predicates: - city(X) - X is a city - state(X) - X is a state - in_state(X, Y) - city X is in state Y - in_us(X) - X is in U.S.
- Constants: - billings, butte, helena, missoula, white_sulphur_springs, st_pierre - cities - montana - state - bristol, texarkana, texhoma, union_city - the exception cities
- Wait, actually some of the premises talk about "cities in the same state" and such. Let me think about what predicates I need.
- Actually, let me simplify. The premises are:
- 1. in_state(billings, montana) & in_us(billings) 2. in_state(butte, montana) & in_state(helena, montana) & in_state(missoula, montana) 3. white_sulphur_springs and butte are in the same state in U.S. - so there exists a state S such that in_state(white_sulphur_springs, S) and in_state(butte, S) and in_us(S). But we already know butte is in montana, so this just tells us white_sulphur_springs is also in montana (or possibly in another state with butte, but since butte is in montana... wait, a city can only be in one state, so butte is only in montana. So white_sulphur_springs must also be in montana. 4. ~in_state(st_pierre, montana) 5. Any city in Butte is not in St Pierre - I'll interpret this as butte != st_pierre or ~in_city(butte, st_pierre) or something. Hmm, this is tricky.
- Actually, let me reconsider premise 5. "Any city in Butte is not in St Pierre." - Maybe this means "Any city that is located in Butte [the city] is not located in St Pierre [the city]." But that's weird because cities aren't typically inside other cities.
- Alternatively, maybe "Any city in Butte" is a parsing error and it means "The city of Butte is not in St Pierre" meaning Butte ≠ St Pierre. But that's trivial if they're different names.
- Actually, I think premise 5 might be trying to say: "Butte is not in St Pierre" - meaning the city of Butte is not located within the city of St Pierre, or more likely, "Butte and St Pierre are different cities."
- Let me just treat premise 5 as: butte != st_pierre (they are distinct cities). This is needed because otherwise Vampire could assume they're the same.
- Actually wait - premise 4 says St Pierre is not in Montana. Premise 2 says Butte is in Montana. If Butte = St Pierre, then Butte would be both in Montana (premise 2) and not in Montana (premise 4), which would be contradictory. So premise 5 just reinforces that they're different cities. But with the distinctness axiom we need anyway, this might be redundant.
- Let me think about what we need:
- Premises (formalized): 1. in_state(billings, montana) 2. in_state(butte, montana) 3. in_state(helena, montana) 4. in_state(missoula, montana) 5. in_us(montana) - implied by premise 1 6. ? [S: state] : (in_state(white_sulphur_springs, S) & in_state(butte, S) & in_us(S)) 7. ~in_state(st_pierre, montana) 8. butte != st_pierre (from premise 5) 9. ! [C, S1, S2] : ((in_state(C, S1) & in_state(C, S2) & city(C) & state(S1) & state(S2) & ~exception(C)) => S1 = S2) where exception cities are bristol, texarkana, texhoma, union_city
- Wait, but I'm not sure "in_us" is really needed. Let me simplify.
- Actually, for the conclusion "Montana is home to the city of Missoula" which means in_state(missoula, montana), this is directly stated in premise 2. So the conclusion is trivially true.
- But I need to be careful - could there be any interpretation where this doesn't hold? Let me check if there's any contradiction or exception.
- Premise 6 says a city can only be in one state except for four specific cities. Missoula is not among those exceptions. So if Missoula were in two states, that would be a problem. But premise 2 says it's in Montana, so that's fine.
- The conclusion seems straightforwardly True.
- Let me write the TPTP code.
- Actually, I need to be careful about what "in Butte" means in premise 5. Let me just interpret it as: butte and st_pierre are different cities (they're not the same city). I'll add butte != st_pierre as a distinctness axiom.
- Let me also think about what other distinctness axioms I need. I should say all the named cities are distinct from each other.
- And states... well, we only have one state mentioned (Montana), so no need for state distinctness.
- Let me write the TPTP code now.
- For the positive version (conclusion: Montana is home to Missoula → in_state(missoula, montana)): - The conjecture is in_state(missoula, montana)
- For the negative version: - The conjecture is ~in_state(missoula, montana)
- Premise 6 about "a city can only be in one state" - I'll model this as: ! [C, S1, S2] : ((in_state(C, S1) & in_state(C, S2) & ~exception_city(C)) => S1 = S2)
- Where exception_city is defined for bristol, texarkana, texhoma, union_city.
- Let me write the code.
- Actually, I also need to model premise 3: "White Sulphur Springs and Butte are cities in the same state in U.S."
- This means there exists some state S such that both are in S. Since Butte is in Montana (premise 2), and a city can only be in one state (premise 6, and Butte is not an exception), White Sulphur Springs must also be in Montana.
- But to be safe, I could just say: ? [S] : (in_state(white_sulphur_springs, S) & in_state(butte, S)). But since butte is in montana and cities can only be in one state, this implies white_sulphur_springs is in montana too. However, the problem doesn't ask about White Sulphur Springs, so this is just supporting context.
- Let me write it out.
- Actually, I realize I need to think about what predicates to use. Let me use:
- - `in_state(City, State)` - City is in State - `city(C)` - C is a city - `state(S)` - S is a state - `exception_city(C)` - C is an exception city (can be in multiple states)
- Constants: billings, butte, helena, missoula, white_sulphur_springs, st_pierre (cities) Constants: montana (state) Constants: bristol, texarkana, texhoma, union_city (exception cities - also cities)
- Let me write the code.
- Actually, I need to think about whether I need types. Let me use fof since this is simple predicate logic.
- For premise 5: "Any city in Butte is not in St Pierre." - I'll interpret this as: Butte and St Pierre are distinct cities, so butte != st_pierre.
- Let me just add all distinctness axioms for all city names.
- Actually, let me reconsider premise 5 more carefully. "Any city in Butte is not in St Pierre" - could this mean "No city that is in Butte [as a location] is in St Pierre"? That seems too complicated. Or could it mean "The city of Butte is not located in St Pierre"? That also seems odd.
- I think the intended meaning is simply that Butte and St Pierre are different cities. Let me go with that.
- Here's my plan:
- Positive file: - Axioms for all premises - Conjecture: in_state(missoula, montana)
- Negative file: - Same axioms - Conjecture: ~in_state(missoula, montana)
- Let me write it.
- Actually, wait. I should also think about whether premise 1 says anything about Billings being in US vs. just being in Montana. "Billings is a city in the state of Montana in U.S." - this just means Billings is in Montana and Montana is a US state.
- Let me also add that Montana is a state.
- Let me write the code now.
- Actually, thinking about it more, I don't need `city` and `state` predicates unless they're needed for the reasoning. Let me keep it minimal.
- Premises: 1. in_state(billings, montana) 2. in_state(butte, montana) & in_state(helena, montana) & in_state(missoula, montana) 3. ? [S] : (in_state(white_sulphur_springs, S) & in_state(butte, S)) 4. ~in_state(st_pierre, montana) 5. butte != st_pierre (interpreting "any city in Butte is not in St Pierre" as distinctness) 6. ! [C, S1, S2] : ((in_state(C, S1) & in_state(C, S2) & ~exception_city(C)) => S1 = S2) exception_city(bristol), exception_city(texarkana), exception_city(texhoma), exception_city(union_city)
- And distinctness: all cities are distinct.
- Let me write it.




### TOKEN USAGE - Iteration 1

  Input tokens:  5,107
  Output tokens: 4,872
  Total tokens:  9,979

### Tool Call: write_and_run_vampire

  Args: {
  "pos_filename": "montana_missoula_pos.p",
  "pos_code": "% Positive version: conjecture is \"Montana is home to Missoula\"\n% i.e., in_state(missoula, montana)\n\n% Distinct city names (all named cities are pairwise distinct)\nfof(distinct_cities, axiom,\n    (billings != butte & billings != helena & billings != missoula &\n     billings != white_sulphur_springs & billings != st_pierre &\n     billings != bristol & billings != texarkana & billings != texhoma &\n     billings != union_city &\n     butte != helena & butte != missoula & butte != white_sulphur_springs &\n     butte != st_pierre & butte != bristol & butte != texarkana &\n     butte != texhoma & butte != union_city &\n     helena != missoula & helena != white_sulphur_springs &\n     helena != st_pierre & helena != bristol & helena != texarkana &\n     helena != texhoma & helena != union_city &\n     missoula != white_sulphur_springs & missoula != st_pierre &\n     missoula != bristol & missoula != texarkana & missoula != texhoma &\n     missoula != union_city &\n     white_sulphur_springs != st_pierre &\n     white_sulphur_springs != bristol & white_sulphur_springs != texarkana &\n     white_sulphur_springs != texhoma & white_sulphur_springs != union_city &\n     st_pierre != bristol & st_pierre != texarkana &\n     st_pierre != texhoma & st_pierre != union_city &\n     bristol != texarkana & bristol != texhoma & bristol != union_city &\n     texarkana != texhoma & texarkana != union_city &\n     texhoma != union_city)).\n\n% Premise 1: Billings is a city in the state of Montana in U.S.\nfof(premise_1, axiom, in_state(billings, montana)).\n\n% Premise 2: The state of Montana includes the cities of Butte, Helena, and Missoula.\nfof(premise_2, axiom,\n    (in_state(butte, montana) & in_state(helena, montana) & in_state(missoula, montana))).\n\n% Premise 3: White Sulphur Springs and Butte are cities in the same state in U.S.\nfof(premise_3, axiom,\n    ? [S] : (in_state(white_sulphur_springs, S) & in_state(butte, S))).\n\n% Premise 4: The city of St Pierre is not in the state of Montana.\nfof(premise_4, axiom, ~in_state(st_pierre, montana)).\n\n% Premise 5: Any city in Butte is not in St Pierre.\n% Interpreted as: Butte and St Pierre are distinct cities.\n% (Already covered by distinctness axiom above, but stated explicitly)\nfof(premise_5, axiom, butte != st_pierre).\n\n% Premise 6: A city can only be in one state in U.S. except for Bristol, Texarkana, Texhoma and Union City.\nfof(exception_bristol, axiom, exception_city(bristol)).\nfof(exception_texarkana, axiom, exception_city(texarkana)).\nfof(exception_texhoma, axiom, exception_city(texhoma)).\nfof(exception_union_city, axiom, exception_city(union_city)).\n\nfof(one_state_per_city, axiom,\n    ! [C, S1, S2] :\n        ((in_state(C, S1) & in_state(C, S2) & ~exception_city(C)) => S1 = S2)).\n\n% Conjecture: Montana is home to the city of Missoula.\nfof(conjecture, conjecture, in_state(missoula, montana)).\n",
  "neg_filename": "montana_missoula_neg.p",
  "neg_code": "% Negative version: conjecture is the negation of \"Montana is home to Missoula\"\n% i.e., ~in_state(missoula, montana)\n\n% Distinct city names (all named cities are pairwise distinct)\nfof(distinct_cities, axiom,\n    (billings != butte & billings != helena & billings != missoula &\n     billings != white_sulphur_springs & billings != st_pierre &\n     billings != bristol & billings != texarkana & billings != texhoma &\n     billings != union_city &\n     butte != helena & butte != missoula & butte != white_sulphur_springs &\n     butte != st_pierre & butte != bristol & butte != texarkana &\n     butte != texhoma & butte != union_city &\n     helena != missoula & helena != white_sulphur_springs &\n     helena != st_pierre & helena != bristol & helena != texarkana &\n     helena != texhoma & helena != union_city &\n     missoula != white_sulphur_springs & missoula != st_pierre &\n     missoula != bristol & missoula != texarkana & missoula != texhoma &\n     missoula != union_city &\n     white_sulphur_springs != st_pierre &\n     white_sulphur_springs != bristol & white_sulphur_springs != texarkana &\n     white_sulphur_springs != texhoma & white_sulphur_springs != union_city &\n     st_pierre != bristol & st_pierre != texarkana &\n     st_pierre != texhoma & st_pierre != union_city &\n     bristol != texarkana & bristol != texhoma & bristol != union_city &\n     texarkana != texhoma & texarkana != union_city &\n     texhoma != union_city)).\n\n% Premise 1: Billings is a city in the state of Montana in U.S.\nfof(premise_1, axiom, in_state(billings, montana)).\n\n% Premise 2: The state of Montana includes the cities of Butte, Helena, and Missoula.\nfof(premise_2, axiom,\n    (in_state(butte, montana) & in_state(helena, montana) & in_state(missoula, montana))).\n\n% Premise 3: White Sulphur Springs and Butte are cities in the same state in U.S.\nfof(premise_3, axiom,\n    ? [S] : (in_state(white_sulphur_springs, S) & in_state(butte, S))).\n\n% Premise 4: The city of St Pierre is not in the state of Montana.\nfof(premise_4, axiom, ~in_state(st_pierre, montana)).\n\n% Premise 5: Any city in Butte is not in St Pierre.\n% Interpreted as: Butte and St Pierre are distinct cities.\n% (Already covered by distinctness axiom above, but stated explicitly)\nfof(premise_5, axiom, butte != st_pierre).\n\n% Premise 6: A city can only be in one state in U.S. except for Bristol, Texarkana, Texhoma and Union City.\nfof(exception_bristol, axiom, exception_city(bristol)).\nfof(exception_texarkana, axiom, exception_city(texarkana)).\nfof(exception_texhoma, axiom, exception_city(texhoma)).\nfof(exception_union_city, axiom, exception_city(union_city)).\n\nfof(one_state_per_city, axiom,\n    ! [C, S1, S2] :\n        ((in_state(C, S1) & in_state(C, S2) & ~exception_city(C)) => S1 = S2)).\n\n% Conjecture: Negation - Montana is NOT home to the city of Missoula.\nfof(conjecture, conjecture, ~in_state(missoula, montana)).\n"
}

#### Result

[{'type': 'text', 'text': '{"positive":{"status":"success","szs_status":"Theorem","stdout":"% Refutation found. Thanks to Tanya!\\n% SZS status Theorem for montana_missoula_pos\\n% SZS output start Proof for montana_missoula_pos\\n3. in_state(butte,montana) & in_state(helena,montana) & in_state(missoula,montana) [input(axiom)]\\n12. in_state(missoula,montana) [input(conjecture)]\\n13. ~in_state(missoula,montana) [negated conjecture 12]\\n14. ~in_state(missoula,montana) [flattening 13]\\n68. in_state(missoula,montana) [cnf transformation 3]\\n75. ~in_state(missoula,montana) [cnf transformation 14]\\n76. $false [forward subsumption resolution 68,75]\\n% SZS output end Proof for montana_missoula_pos\\n% Termination reason: Refutation","stderr":null,"returncode":0},"negative":{"status":"success","szs_status":"CounterSatisfiable","stdout":"% SZS status CounterSatisfiable for montana_missoula_neg\\n% SZS output start Saturation.\\ncnf(u61,axiom,\\n    billings != bristol).\\n\\ncnf(u42,axiom,\\n    missoula != white_sulphur_springs).\\n\\ncnf(u35,axiom,\\n    white_sulphur_springs != bristol).\\n\\ncnf(u24,axiom,\\n    texarkana != texhoma).\\n\\ncnf(u57,axiom,\\n    butte != helena).\\n\\ncnf(u47,axiom,\\n    helena != st_pierre).\\n\\ncnf(u73,axiom,\\n    ~in_state(st_pierre,montana)).\\n\\ncnf(u36,axiom,\\n    white_sulphur_springs != st_pierre).\\n\\ncnf(u29,axiom,\\n    st_pierre != texhoma).\\n\\ncnf(u70,axiom,\\n    in_state(butte,montana)).\\n\\ncnf(u50,axiom,\\n    butte != union_city).\\n\\ncnf(u66,axiom,\\n    billings != butte).\\n\\ncnf(u43,axiom,\\n    helena != union_city).\\n\\ncnf(u32,axiom,\\n    white_sulphur_springs != union_city).\\n\\ncnf(u25,axiom,\\n    bristol != union_city).\\n\\ncnf(u22,axiom,\\n    texhoma != union_city).\\n\\ncnf(u62,axiom,\\n    billings != st_pierre).\\n\\ncnf(u55,axiom,\\n    butte != white_sulphur_springs).\\n\\ncnf(u44,axiom,\\n    helena != texhoma).\\n\\ncnf(u37,axiom,\\n    missoula != union_city).\\n\\ncnf(u71,axiom,\\n    in_state(butte,sK0)).\\n\\ncnf(u58,axiom,\\n    billings != union_city).\\n\\ncnf(u51,axiom,\\n    butte != texhoma).\\n\\ncnf(u40,axiom,\\n    missoula != bristol).\\n\\ncnf(u74,axiom,\\n    butte != st_pierre).\\n\\ncnf(u33,axiom,\\n    white_sulphur_springs != texhoma).\\n\\ncnf(u30,axiom,\\n    st_pierre != texarkana).\\n\\ncnf(u23,axiom,\\n    texarkana != union_city).\\n\\ncnf(u67,axiom,\\n    in_state(billings,montana)).\\n\\ncnf(u63,axiom,\\n    billings != white_sulphur_springs).\\n\\ncnf(u52,axiom,\\n    butte != texarkana).\\n\\ncnf(u45,axiom,\\n    helena != texarkana).\\n\\ncnf(u26,axiom,\\n    bristol != texhoma).\\n\\ncnf(u59,axiom,\\n    billings != texhoma).\\n\\ncnf(u48,axiom,\\n    helena != white_sulphur_springs).\\n\\ncnf(u41,axiom,\\n    missoula != st_pierre).\\n\\ncnf(u38,axiom,\\n    missoula != texhoma).\\n\\ncnf(u31,axiom,\\n    st_pierre != bristol).\\n\\ncnf(u75,negated_conjecture,\\n    in_state(missoula,montana)).\\n\\ncnf(u64,axiom,\\n    billings != missoula).\\n\\ncnf(u60,axiom,\\n    billings != texarkana).\\n\\ncnf(u53,axiom,\\n    butte != bristol).\\n\\ncnf(u34,axiom,\\n    white_sulphur_springs != texarkana).\\n\\ncnf(u27,axiom,\\n    bristol != texarkana).\\n\\ncnf(u69,axiom,\\n    in_state(helena,montana)).\\n\\ncnf(u56,axiom,\\n    butte != missoula).\\n\\ncnf(u72,axiom,\\n    in_state(white_sulphur_springs,sK0)).\\n\\ncnf(u49,axiom,\\n    helena != missoula).\\n\\ncnf(u46,axiom,\\n    helena != bristol).\\n\\ncnf(u39,axiom,\\n    missoula != texarkana).\\n\\ncnf(u28,axiom,\\n    st_pierre != union_city).\\n\\ncnf(u65,axiom,\\n    billings != helena).\\n\\n% SZS output end Saturation.\\n% SZS output start Definitions and Model Updates.\\nfor all inputs,\\n    define exception_city(X0) := $true\\n% SZS output end Definitions and Model Updates.\\n% Termination reason: Satisfiable","stderr":null,"returncode":0}}', 'id': 'lc_cc3ba8d9-5d0f-4216-ba24-542b157e5ae8'}]


[NOTE] Skipping Answer Phase for FOLIO benchmark as solver returns verdict directly.

TOKEN USAGE SUMMARY
  Total input tokens:  5,107
  Total output tokens: 4,872
  Total tokens:        9,979

COMPLETE

## Final Answer

```json
[{'type': 'text', 'text': '{"positive":{"status":"success","szs_status":"Theorem","stdout":"% Refutation found. Thanks to Tanya!\\n% SZS status Theorem for montana_missoula_pos\\n% SZS output start Proof for montana_missoula_pos\\n3. in_state(butte,montana) & in_state(helena,montana) & in_state(missoula,montana) [input(axiom)]\\n12. in_state(missoula,montana) [input(conjecture)]\\n13. ~in_state(missoula,montana) [negated conjecture 12]\\n14. ~in_state(missoula,montana) [flattening 13]\\n68. in_state(missoula,montana) [cnf transformation 3]\\n75. ~in_state(missoula,montana) [cnf transformation 14]\\n76. $false [forward subsumption resolution 68,75]\\n% SZS output end Proof for montana_missoula_pos\\n% Termination reason: Refutation","stderr":null,"returncode":0},"negative":{"status":"success","szs_status":"CounterSatisfiable","stdout":"% SZS status CounterSatisfiable for montana_missoula_neg\\n% SZS output start Saturation.\\ncnf(u61,axiom,\\n    billings != bristol).\\n\\ncnf(u42,axiom,\\n    missoula != white_sulphur_springs).\\n\\ncnf(u35,axiom,\\n    white_sulphur_springs != bristol).\\n\\ncnf(u24,axiom,\\n    texarkana != texhoma).\\n\\ncnf(u57,axiom,\\n    butte != helena).\\n\\ncnf(u47,axiom,\\n    helena != st_pierre).\\n\\ncnf(u73,axiom,\\n    ~in_state(st_pierre,montana)).\\n\\ncnf(u36,axiom,\\n    white_sulphur_springs != st_pierre).\\n\\ncnf(u29,axiom,\\n    st_pierre != texhoma).\\n\\ncnf(u70,axiom,\\n    in_state(butte,montana)).\\n\\ncnf(u50,axiom,\\n    butte != union_city).\\n\\ncnf(u66,axiom,\\n    billings != butte).\\n\\ncnf(u43,axiom,\\n    helena != union_city).\\n\\ncnf(u32,axiom,\\n    white_sulphur_springs != union_city).\\n\\ncnf(u25,axiom,\\n    bristol != union_city).\\n\\ncnf(u22,axiom,\\n    texhoma != union_city).\\n\\ncnf(u62,axiom,\\n    billings != st_pierre).\\n\\ncnf(u55,axiom,\\n    butte != white_sulphur_springs).\\n\\ncnf(u44,axiom,\\n    helena != texhoma).\\n\\ncnf(u37,axiom,\\n    missoula != union_city).\\n\\ncnf(u71,axiom,\\n    in_state(butte,sK0)).\\n\\ncnf(u58,axiom,\\n    billings != union_city).\\n\\ncnf(u51,axiom,\\n    butte != texhoma).\\n\\ncnf(u40,axiom,\\n    missoula != bristol).\\n\\ncnf(u74,axiom,\\n    butte != st_pierre).\\n\\ncnf(u33,axiom,\\n    white_sulphur_springs != texhoma).\\n\\ncnf(u30,axiom,\\n    st_pierre != texarkana).\\n\\ncnf(u23,axiom,\\n    texarkana != union_city).\\n\\ncnf(u67,axiom,\\n    in_state(billings,montana)).\\n\\ncnf(u63,axiom,\\n    billings != white_sulphur_springs).\\n\\ncnf(u52,axiom,\\n    butte != texarkana).\\n\\ncnf(u45,axiom,\\n    helena != texarkana).\\n\\ncnf(u26,axiom,\\n    bristol != texhoma).\\n\\ncnf(u59,axiom,\\n    billings != texhoma).\\n\\ncnf(u48,axiom,\\n    helena != white_sulphur_springs).\\n\\ncnf(u41,axiom,\\n    missoula != st_pierre).\\n\\ncnf(u38,axiom,\\n    missoula != texhoma).\\n\\ncnf(u31,axiom,\\n    st_pierre != bristol).\\n\\ncnf(u75,negated_conjecture,\\n    in_state(missoula,montana)).\\n\\ncnf(u64,axiom,\\n    billings != missoula).\\n\\ncnf(u60,axiom,\\n    billings != texarkana).\\n\\ncnf(u53,axiom,\\n    butte != bristol).\\n\\ncnf(u34,axiom,\\n    white_sulphur_springs != texarkana).\\n\\ncnf(u27,axiom,\\n    bristol != texarkana).\\n\\ncnf(u69,axiom,\\n    in_state(helena,montana)).\\n\\ncnf(u56,axiom,\\n    butte != missoula).\\n\\ncnf(u72,axiom,\\n    in_state(white_sulphur_springs,sK0)).\\n\\ncnf(u49,axiom,\\n    helena != missoula).\\n\\ncnf(u46,axiom,\\n    helena != bristol).\\n\\ncnf(u39,axiom,\\n    missoula != texarkana).\\n\\ncnf(u28,axiom,\\n    st_pierre != union_city).\\n\\ncnf(u65,axiom,\\n    billings != helena).\\n\\n% SZS output end Saturation.\\n% SZS output start Definitions and Model Updates.\\nfor all inputs,\\n    define exception_city(X0) := $true\\n% SZS output end Definitions and Model Updates.\\n% Termination reason: Satisfiable","stderr":null,"returncode":0}}', 'id': 'lc_cc3ba8d9-5d0f-4216-ba24-542b157e5ae8'}]
```
