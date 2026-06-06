fof(show_exists, axiom, ? [S] : (show(S) & airs_at_time(S, monday_8pm) & roses_on_tv(S))).
fof(roses_implies_bachelor, axiom, ! [S] : (roses_on_tv(S) => episode_of_bachelor(S))).
fof(bachelor_portrays_real, axiom, ! [S] : (episode_of_bachelor(S) => portrays_real_people(S))).
fof(reality_tv_implies_reality, axiom, ! [S] : (portrays_real_people(S) => is_reality_tv(S))).
fof(breaking_bad_is_show, axiom, show(breaking_bad)).
fof(breaking_bad_not_reality, axiom, ~is_reality_tv(breaking_bad)).
fof(conclusion_negation, conjecture, ~(roses_on_tv(breaking_bad) => airs_at_time(breaking_bad, monday_8pm))).