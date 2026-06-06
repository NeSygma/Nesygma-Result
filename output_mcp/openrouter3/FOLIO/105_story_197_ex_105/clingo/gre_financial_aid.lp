% Logical Premises about GRE Financial Aid

% Domain declarations
person(tom).
test(gre).

% Cost facts
cost(gre, 205).
cost(gre, 300).  % This is the comparison point

% Financial aid rule: ETS provides financial aid to those who prove economic hardship
% We need to model "proves economic hardship" as a condition
% Economic hardship can be proven by: living in single-parent family OR having few resources
% Tom satisfies both conditions

% Facts about Tom
lives_in_single_parent_family(tom).
has_few_resources(tom).
dad_out_of_work(tom).  % This supports the "few resources" condition
applying_for_test(tom, gre).

% Economic hardship proof conditions
% A person proves economic hardship if they live in single-parent family OR have few resources
proves_economic_hardship(P) :- lives_in_single_parent_family(P).
proves_economic_hardship(P) :- has_few_resources(P).

% Financial aid provision rule
% ETS provides financial aid to those who prove economic hardship
provides_financial_aid(P) :- proves_economic_hardship(P).

% Conclusion evaluation
% The conclusion is: "ETS provides financial aid to Tom"
conclusion_true :- provides_financial_aid(tom).
conclusion_false :- not provides_financial_aid(tom).

% Answer mapping following the theorem proving pattern
answer(true) :- conclusion_true.
answer(false) :- conclusion_false.
answer(uncertain) :- not conclusion_true, not conclusion_false.
answer(inconsistent) :- conclusion_true, conclusion_false.

% Show relevant predicates
#show person/1.
#show test/1.
#show cost/2.
#show lives_in_single_parent_family/1.
#show has_few_resources/1.
#show proves_economic_hardship/1.
#show provides_financial_aid/1.
#show conclusion_true/0.
#show conclusion_false/0.
#show answer/1.