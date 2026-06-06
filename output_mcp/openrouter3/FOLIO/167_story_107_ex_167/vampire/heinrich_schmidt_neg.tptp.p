% Heuristics: 
%   Theorem: The conjecture is entailed by the axioms
%   CounterSatisfiable: The conjecture is NOT entailed (counter-model exists)
%   ContradictoryAxioms: The axioms alone are unsatisfiable (flawed setup)
%   Unknown/Timeout/GaveUp/MemoryOut: Inconclusive

% Premises
fof(premise_1, axiom, german(heinrich_schmidt)).
fof(premise_2, axiom, member_of_prussian_parliament(heinrich_schmidt)).
fof(premise_3, axiom, member_of_nazi_reichstag(heinrich_schmidt)).

% Negated conclusion: Heinrich Schmidt was NOT (German or Russian or both)
% This is equivalent to: NOT German AND NOT Russian
fof(goal_negation, conjecture, ~(german(heinrich_schmidt) | russian(heinrich_schmidt))). 
% Which simplifies to: ~german(heinrich_schmidt) & ~russian(heinrich_schmidt)