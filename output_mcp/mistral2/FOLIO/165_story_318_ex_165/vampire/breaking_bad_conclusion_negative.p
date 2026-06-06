fof(show, axiom, show(bachelor)).
fof(show, axiom, show(breaking_bad)).

fof(airs_at_8pm_monday_and_gives_roses, axiom, ? [X] : (airs_at_8pm_monday(X) & gives_roses(X))).

fof(gives_roses_implies_bachelor, axiom, ! [X] : (gives_roses(X) => is_bachelor_episode(X))).

fof(bachelor_portrays_real_people, axiom, portrays_real_people(bachelor)).

fof(portrays_real_people_implies_reality_tv, axiom, ! [X] : (portrays_real_people(X) => is_reality_tv(X))).

fof(breaking_bad_not_reality_tv, axiom, ~is_reality_tv(breaking_bad)).

fof(distinct_shows, axiom, bachelor != breaking_bad).

fof(conclusion_negation, conjecture, ~(airs_at_8pm_monday(breaking_bad) & gives_roses(breaking_bad))).