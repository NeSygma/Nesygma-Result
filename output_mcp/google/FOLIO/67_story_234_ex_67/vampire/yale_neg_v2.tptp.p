tff(university_type, type, university: $tType).
tff(yale_uni, type, yale_uni: university).
tff(endowment, type, endowment: (university * $int) > $o).
tff(is_largest, type, is_largest: university > $o).
tff(fact_endowment, axiom, endowment(yale_uni, 42300000000)).
tff(goal, conjecture, ~is_largest(yale_uni)).