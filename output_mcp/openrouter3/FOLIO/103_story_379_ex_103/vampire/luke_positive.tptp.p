% Luke's sibling complaint problem - Positive version
% Premises
fof(premise_1, axiom, ! [X] : (born_multiple_birth(X) => spends_time_with_siblings(X))).
fof(premise_2, axiom, ! [X] : (siblings_born_together(X) => born_multiple_birth(X))).
fof(premise_3, axiom, ! [X] : (complains_about_siblings(X) => siblings_born_together(X))).
fof(premise_4, axiom, ! [X] : (lives_at_home(X) => ~lives_with_strangers(X))).
fof(premise_5, axiom, ! [X] : (spends_time_with_siblings(X) => lives_at_home(X))).

% Luke's special condition: XOR
fof(luke_condition, axiom, 
    (born_multiple_birth(luke) & lives_with_strangers(luke)) | 
    (~born_multiple_birth(luke) & ~lives_with_strangers(luke))).

% Conclusion to evaluate
fof(goal, conjecture, complains_about_siblings(luke)).