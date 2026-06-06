% Premises about GRE test and financial aid
% Constants
fof(ets_decl, axiom, ets != ets | ets = ets). % just to note ets exists
fof(tom_decl, axiom, tom != tom | tom = tom). % just to note tom exists

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

% Conclusion: No one taking the GRE test has financial aid provided to them by anything
fof(conclusion, conjecture, ! [X] : (gre_applicant(X) => ! [Y] : ~provides_financial_aid(Y, X))).