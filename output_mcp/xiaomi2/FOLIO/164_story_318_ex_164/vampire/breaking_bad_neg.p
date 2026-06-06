fof(show_some, axiom, ? [X] : (show(X) & airing_at_8pm_monday(X) & gives_out_roses(X))).
fof(roses_bachelor, axiom, ! [X] : (gives_out_roses(X) => episode_of_bachelor(X))).
fof(bachelor_real, axiom, ! [X] : (episode_of_bachelor(X) => portrays_real_people(X))).
fof(real_reality, axiom, ! [X] : (portrays_real_people(X) => reality_tv_show(X))).
fof(bb_show, axiom, show(breaking_bad)).
fof(bb_not_reality, axiom, ~reality_tv_show(breaking_bad)).
fof(goal, conjecture, ~airing_at_8pm_monday(breaking_bad)).