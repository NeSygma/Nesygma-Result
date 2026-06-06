fof(show_exists, axiom,
    ? [X] : (show(X) & airs_at_8pm_monday(X) & gives_roses(X))).

fof(roses_bachelor, axiom,
    ! [X] : (gives_roses(X) => bachelor_episode(X))).

fof(bachelor_real_lives, axiom,
    ! [X] : (bachelor_episode(X) => portrays_real_lives(X))).

fof(bachelor_portrays, axiom,
    portrays_real_lives(bachelor)).

fof(real_lives_reality, axiom,
    ! [X] : (portrays_real_lives(X) => reality_tv(X))).

fof(bb_show, axiom,
    show(breaking_bad)).

fof(bb_not_reality, axiom,
    ~reality_tv(breaking_bad)).

fof(goal, conjecture,
    gives_roses(breaking_bad) => airs_at_8pm_monday(breaking_bad)).