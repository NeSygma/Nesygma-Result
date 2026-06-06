% Premises about GRE test and financial aid
% Premise 2: ETS provides financial aid to GRE applicants who prove economic hardship
fof(premise_2, axiom, ! [X] : ((gre_applicant(X) & proves_hardship(X)) => provides_financial_aid(ets, X))).

% Premise 3: Those in single-parent families or with few resources can prove hardship
fof(premise_3, axiom, ! [X] : ((single_parent_family(X) | few_resources(X)) => proves_hardship(X))).

% Premise 4: Tom lives in a single-parent family
fof(premise_4, axiom, single_parent_family(tom)).

% Premise 5: Tom has few resources available
fof(premise_5, axiom, few_resources(tom)).

% Premise 6: Tom is applying to take the GRE test
fof(premise_6, axiom, gre_applicant(tom)).

% Negated conclusion: There exists someone taking the GRE who has financial aid from something
fof(conclusion_neg, conjecture, ? [X] : ? [Y] : (gre_applicant(X) & provides_financial_aid(Y, X))).