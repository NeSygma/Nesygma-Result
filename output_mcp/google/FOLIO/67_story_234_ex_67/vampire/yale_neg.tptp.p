tff(university_type, type, university: $tType).
tff(yale_uni, type, yale_uni: university).
tff(endowment, type, endowment: (university * $int) > $o).
tff(is_largest, type, is_largest: university > $o).
tff(fact_endowment, axiom, endowment(yale_uni, 42300000000)).
tff(is_largest_def, axiom, ! [U: university] : (is_largest(U) <=> ! [V: university] : ((V != U) => ? [E_u: $int, E_v: $int] : (endowment(U, E_u) & endowment(V, E_v) & $greater(E_u, E_v))))).
tff(goal, conjecture, ~is_largest(yale_uni)).