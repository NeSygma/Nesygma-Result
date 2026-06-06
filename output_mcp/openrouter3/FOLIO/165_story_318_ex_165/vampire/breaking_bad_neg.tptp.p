% Premises
fof(premise_1, axiom, ? [X] : (show(X) & airs_at_8pm_monday(X) & gives_out_roses(X))).
fof(premise_2, axiom, ! [X] : (gives_out_roses(X) => is_episode_of_bachelor(X))).
fof(premise_3, axiom, is_episode_of_bachelor(bachelor)).
fof(premise_3b, axiom, portrays_real_people(bachelor)).
fof(premise_4, axiom, ! [X] : (portrays_real_people(X) => is_reality_tv(X))).
fof(premise_5, axiom, show(breaking_bad)).
fof(premise_6, axiom, ~is_reality_tv(breaking_bad)).

% Negated conclusion
fof(goal_neg, conjecture, ~(show(breaking_bad) & airs_at_8pm_monday(breaking_bad) & gives_out_roses(breaking_bad))).