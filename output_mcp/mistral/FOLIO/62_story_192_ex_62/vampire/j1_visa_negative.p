fof(premise1, axiom,
    ! [X] : (international_student_in_us(X) =>
             (has_f1_visa(X) | has_j1_visa(X)))).

fof(premise2, axiom,
    ! [X] : ((international_student_in_us(X) &
              has_f1_visa(X) &
              wants_to_work(X)) =>
             (needs_cpt(X) | needs_opt(X)))).

fof(premise3, axiom,
    international_student_in_us(mike)).

fof(premise4, axiom,
    (wants_to_work(mike) => needs_cpt(mike))).

fof(conjecture, conjecture,
    ~has_j1_visa(mike)).