% Positive file: original conclusion as conjecture
% Conclusion: John does not have a larger family => ~larger_family(john)

% Predicates:
% engaged(X) - X is engaged
% makes_wedding_plans(X) - X makes wedding plans
% invites_ceremony(X) - X invites others to come to their ceremony
% well_attended_wedding(X) - X has a well-attended wedding
% larger_family(X) - X has a larger family
% invites_friends(X) - X invites friends to their ceremony

% Premise 1: All people who make wedding plans are people who are engaged.
fof(premise1, axiom, ! [X] : (makes_wedding_plans(X) => engaged(X))).

% Premise 2: All people who invite others to come to their ceremony make wedding plans.
fof(premise2, axiom, ! [X] : (invites_ceremony(X) => makes_wedding_plans(X))).

% Premise 3: Anyone who has a well-attended wedding invites others to come to their ceremony.
fof(premise3, axiom, ! [X] : (well_attended_wedding(X) => invites_ceremony(X))).

% Premise 4: Some people that have well-attended weddings have larger families.
fof(premise4, axiom, ? [X] : (well_attended_wedding(X) & larger_family(X))).

% Premise 5: If John is engaged, then John does not invite friends to their ceremony and make wedding plans.
fof(premise5, axiom, (engaged(john) => (~invites_friends(john) & makes_wedding_plans(john)))).

% Premise 6: If John has a larger family, then either John has a well-attended wedding or invites friends to their ceremony.
fof(premise6, axiom, (larger_family(john) => (well_attended_wedding(john) | invites_friends(john)))).

% Conclusion: John does not have a larger family.
fof(conclusion, conjecture, ~larger_family(john)).