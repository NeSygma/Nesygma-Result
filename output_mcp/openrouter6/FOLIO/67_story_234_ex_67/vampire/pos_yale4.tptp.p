tff(institution_sort, type, institution: $tType).
tff(yale_decl, type, yale: institution).
tff(other_decl, type, other: institution).
tff(endowment_func, type, endowment: institution > $int).
tff(educational_institution_decl, type, educational_institution: (institution) > $o).
tff(largest_endowment_decl, type, largest_endowment: (institution) > $o).
tff(distinct, axiom, $distinct(yale, other)).
tff(yale_endowment, axiom, endowment(yale) = 42).
tff(other_educational, axiom, educational_institution(other)).
tff(yale_educational, axiom, educational_institution(yale)).
tff(endowment_range, axiom, ! [X: institution] : ($lesseq(endowment(X), 43) & $greatereq(endowment(X), 42))).
tff(largest_endowment_def, axiom, ! [X: institution] : (largest_endowment(X) <=> (educational_institution(X) & ! [Y: institution] : (educational_institution(Y) => (Y = X | $lesseq(endowment(Y), endowment(X))))))).
tff(goal, conjecture, largest_endowment(yale)).