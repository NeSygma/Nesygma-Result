% Negative version (negated conjecture)
fof(distinct_const, axiom, breaking_bad != the_bachelor).
fof(exist_show, axiom, ? [S] : (airs_at(S, time_8pm, monday) & gives_roses(S))).
fof(gives_implies_episode, axiom, ! [S] : (gives_roses(S) => episode_of_the_bachelor(S))).
fof(bachelor_real, axiom, portrays_real_people(the_bachelor)).
fof(real_implies_reality, axiom, ! [S] : (portrays_real_people(S) => reality_tv(S))).
fof(breaking_bad_show, axiom, show(breaking_bad)).
fof(breaking_bad_not_reality, axiom, ~reality_tv(breaking_bad)).
fof(goal_neg, conjecture, ~airs_at(breaking_bad, time_8pm, monday)).