% Heuristics: 
%   Theorem: The conjecture is entailed by the axioms
%   CounterSatisfiable: The conjecture is NOT entailed (counter-model exists)
%   ContradictoryAxioms: The axioms alone are unsatisfiable (flawed setup)
%   Unknown/Timeout/GaveUp/MemoryOut: Inconclusive

% Premises
fof(premise_1, axiom, german(heinrich_schmidt)).
fof(premise_2, axiom, member_of_prussian_parliament(heinrich_schmidt)).
fof(premise_3, axiom, member_of_nazi_reichstag(heinrich_schmidt)).

% Conclusion: Heinrich Schmidt was German or Russian or both
fof(goal, conjecture, german(heinrich_schmidt) | russian(heinrich_schmidt)).