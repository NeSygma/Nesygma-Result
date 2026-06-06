fof(show_breaking_bad, axiom, show(breaking_bad)).
fof(not_reality_tv_breaking_bad, axiom, ~is_reality_tv(breaking_bad)).

fof(some_show_airs_roses, axiom, ? [X] : (airs_at(X, monday_8pm) & gives_roses(X))).

fof(gives_roses_implies_bachelor, axiom, ! [X] : (gives_roses(X) => is_bachelor_episode(X))).
fof(bachelor_episode_implies_real_people, axiom, ! [X] : (is_bachelor_episode(X) => portrays_real_people(X))).
fof(real_people_implies_reality_tv, axiom, ! [X] : (portrays_real_people(X) => is_reality_tv(X))).

fof(conclusion, conjecture, airs_at(breaking_bad, monday_8pm)).