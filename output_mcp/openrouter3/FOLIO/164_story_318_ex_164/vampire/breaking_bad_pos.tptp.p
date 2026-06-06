% Premises
fof(premise_1, axiom, ? [S, T] : (airs_at(S, T) & gives_out_roses(S) & T = monday_8pm)).
fof(premise_2, axiom, ! [S] : (gives_out_roses(S) => is_episode_of_bachelor(S))).
fof(premise_3, axiom, is_episode_of_bachelor(the_bachelor)).
fof(premise_4, axiom, ! [S] : (portrays_real_people(S) => is_reality_tv(S))).
fof(premise_5, axiom, show(breaking_bad)).
fof(premise_6, axiom, ~is_reality_tv(breaking_bad)).
fof(premise_7, axiom, ! [S] : (is_episode_of_bachelor(S) => portrays_real_people(S))).

% Conclusion
fof(goal, conjecture, airs_at(breaking_bad, monday_8pm)).