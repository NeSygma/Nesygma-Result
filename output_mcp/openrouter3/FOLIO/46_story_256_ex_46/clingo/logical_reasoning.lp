% Logical Reasoning: Cats, Mammals, and Pets

% Domain: A small set of possible entities
entity(1). entity(2). entity(3).

% Open relations - what we don't know from premises
{ cat(X) } :- entity(X).
{ mammal(X) } :- entity(X).
{ pet(X) } :- entity(X).

% Premise 1: All cats are mammals
% If something is a cat, it must be a mammal
:- cat(X), not mammal(X).

% Premise 2: Some pets are not mammals
% There exists at least one pet that is not a mammal
% We'll enforce this with a constraint that requires at least one such entity
:- #count{ X : pet(X), not mammal(X) } = 0.

% Conclusion: No pets are cats
% This means: For all X, if pet(X) then not cat(X)
% conclusion_true holds if there is no entity that is both a pet and a cat
conclusion_true :- #count{ X : pet(X), cat(X) } = 0.

% conclusion_false holds if there exists at least one entity that is both a pet and a cat
conclusion_false :- #count{ X : pet(X), cat(X) } > 0.

% Final Answer Mapping
answer(true) :- conclusion_true.
answer(false) :- conclusion_false.
answer(uncertain) :- not conclusion_true, not conclusion_false.
answer(inconsistent) :- conclusion_true, conclusion_false.

% Show directives
#show cat/1.
#show mammal/1.
#show pet/1.
#show conclusion_true/0.
#show conclusion_false/0.
#show answer/1.