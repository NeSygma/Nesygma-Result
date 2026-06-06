% Negative version: negated conclusion as conjecture
% Original conclusion: ~? [X, Y] : (takes_gre(X) & provides_financial_aid(Y, X))
% Negated: ~~? [X, Y] : (takes_gre(X) & provides_financial_aid(Y, X))
% Which simplifies to: ? [X, Y] : (takes_gre(X) & provides_financial_aid(Y, X))

fof(distinct, axiom, (tom != ets & tom != dad & ets != dad)).

% Premise: ETS provides financial aid to those GRE applicants who prove economic hardship.
fof(rule_1, axiom, ! [X] : ((takes_gre(X) & proves_economic_hardship(X)) => provides_financial_aid(ets, X))).

% Premise: Those living in single-parent families or having few resources available to them can prove economic hardship.
fof(rule_2, axiom, ! [X] : ((lives_single_parent_family(X) | has_few_resources(X)) => proves_economic_hardship(X))).

% Premise: Tom lives in a single-parent family.
fof(fact_1, axiom, lives_single_parent_family(tom)).

% Premise: Tom's dad has been out of work, and Tom has few resources available to them.
fof(fact_2, axiom, has_few_resources(tom)).

% Premise: Tom is applying to take the GRE test.
fof(fact_3, axiom, takes_gre(tom)).

% Negated conclusion: There exists someone taking the GRE who has financial aid provided by something.
fof(goal_neg, conjecture, ? [X, Y] : (takes_gre(X) & provides_financial_aid(Y, X))).