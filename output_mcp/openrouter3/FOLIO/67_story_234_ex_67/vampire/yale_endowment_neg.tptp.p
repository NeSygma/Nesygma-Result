% Yale University Endowment Problem - Negative Version
% Using tff for typed arithmetic

tff(university_type, type, university: $tType).
tff(endowment_type, type, endowment_value: (university * $int) > $o).

tff(yale_decl, type, yale: university).
tff(yale_endowment_val, axiom, endowment_value(yale, 42300000000)).

% Define what it means to have the largest endowment
% For all universities U, if U has an endowment, then Yale's endowment >= U's endowment
tff(largest_endowment_def, axiom,
    ! [U: university] : 
        (endowment_value(U, V) => $greatereq(42300000000, V))).

% Negated conclusion: Yale does NOT have the largest endowment
fof(goal_neg, conjecture, ~largest_endowment(yale)).