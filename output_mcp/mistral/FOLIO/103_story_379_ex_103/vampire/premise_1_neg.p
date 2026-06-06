fof(multiple_birth_implies_spend_time, axiom, 
    ! [P] : (multiple_birth_with_siblings(P) => spend_time_with_siblings(P))).

fof(siblings_born_together_implies_multiple_birth, axiom, 
    ! [P] : (siblings_born_together(P) => multiple_birth_with_siblings(P))).

fof(complains_implies_siblings_born_together, axiom, 
    ! [P] : (complains_about_siblings(P) => siblings_born_together(P))).

fof(lives_at_home_implies_not_lives_with_strangers, axiom, 
    ! [P] : (lives_at_home(P) => ~lives_with_strangers(P))).

fof(spend_time_implies_lives_at_home, axiom, 
    ! [P] : (spend_time_with_siblings(P) => lives_at_home(P))).

fof(luke_alternative, axiom, 
    (is_baby_multiple_birth(luke) & lives_with_strangers(luke)) |
    (~is_baby_multiple_birth(luke) & ~lives_with_strangers(luke))).

fof(conclusion_negation, conjecture, 
    ~complains_about_siblings(luke)).