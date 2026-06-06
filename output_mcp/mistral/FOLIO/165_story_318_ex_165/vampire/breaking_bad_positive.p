fof(premise_1, axiom, ? [S] : (airs_at_8pm_monday(S) & gives_out_roses(S))).
fof(premise_2, axiom, ! [S] : (gives_out_roses(S) => is_episode_of_the_bachelor(S))).
fof(premise_3, axiom, ! [S] : (is_episode_of_the_bachelor(S) => portrays_real_people(S))).
fof(premise_4, axiom, ! [S] : (portrays_real_people(S) => is_reality_tv(S))).
fof(premise_5, axiom, is_show(breaking_bad)).
fof(premise_6, axiom, ~is_reality_tv(breaking_bad)).
fof(conclusion, conjecture, airs_at_8pm_monday(breaking_bad) & gives_out_roses(breaking_bad)).