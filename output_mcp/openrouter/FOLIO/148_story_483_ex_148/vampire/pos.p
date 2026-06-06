% Positive version
fof(distinct_constants, axiom, ekaterina != vladimir).

% Premise 1
fof(premise1, axiom, ! [X] : (can_register(X) => can_participate(X))).
% Premise 2
fof(premise2, axiom, ! [X] : (us_citizen(X) => can_register(X))).
% Premise 3 (inclusive or)
fof(premise3, axiom, ! [X] : (us_citizen(X) | tw_citizen(X))).
% Premise 4
fof(premise4, axiom, ! [X] : (russian_official(X) => ~tw_citizen(X))).
% Premise 5 (Vladimir)
fof(premise5, axiom, (~tw_citizen(vladimir) & ~manager_gazprom(vladimir))).
% Premise 6 (Ekaterina)
fof(premise6, axiom, (can_register(ekaterina) | russian_official(ekaterina))).

% Conjecture
fof(goal, conjecture, (can_participate(ekaterina) | manager_gazprom(vladimir))).