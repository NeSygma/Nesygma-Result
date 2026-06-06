fof(multiple_birth_implies_spends_time, axiom,
    ! [X] : (multiple_birth_sibling(X) => spends_time_with_siblings(X))).

fof(born_together_implies_multiple_birth, axiom,
    ! [X] : (born_together_siblings(X) => multiple_birth_sibling(X))).

fof(complains_implies_born_together, axiom,
    ! [X] : (complains_about_siblings(X) => born_together_siblings(X))).

fof(lives_at_home_implies_not_strangers, axiom,
    ! [X] : (lives_at_home(X) => ~lives_with_strangers(X))).

fof(spends_time_implies_lives_at_home, axiom,
    ! [X] : (spends_time_with_siblings(X) => lives_at_home(X))).

fof(luke_situation, axiom,
    (multiple_birth_sibling(luke) & lives_with_strangers(luke)) |
    (~multiple_birth_sibling(luke) & ~lives_with_strangers(luke))).

fof(conclusion_negation, conjecture,
    ~complains_about_siblings(luke)).