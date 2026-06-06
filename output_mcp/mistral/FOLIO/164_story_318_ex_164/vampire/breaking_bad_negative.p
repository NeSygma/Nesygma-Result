fof(premise_1, axiom, ? [Show] : (airs_at_8pm_monday(Show) & gives_out_roses(Show))).
fof(premise_2, axiom, ! [Show] : (gives_out_roses(Show) => is_episode_of_the_bachelor(Show))).
fof(premise_3, axiom, portrays_real_people(the_bachelor)).
fof(premise_4, axiom, ! [Show] : (portrays_real_people(Show) => is_reality_tv(Show))).
fof(premise_5, axiom, is_show(breaking_bad)).
fof(premise_6, axiom, ~is_reality_tv(breaking_bad)).
fof(conclusion, conjecture, ~airs_at_8pm_monday(breaking_bad)).