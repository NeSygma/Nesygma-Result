tff(yale_type, type, yale: $tType).
tff(university_type, type, university: $tType).
tff(endowment_type, type, endowment: (university * $real) > $o).

fof(yale_university, axiom, university(yale)).
fof(yale_endowment, axiom, endowment(yale, 42.3)).
fof(endowment_positive, axiom, ! [U: university, E: $real] : (endowment(U, E) => $greater(E, 0.0))).

fof(largest_endowment_def, axiom,
    ! [U: university, E: $real] :
      (largest_endowment(U, E) <=>
       (endowment(U, E) &
        ! [V: university, F: $real] : (endowment(V, F) => $greatereq(E, F))))).

fof(goal_negation, conjecture, ~largest_endowment(yale, 42.3)).