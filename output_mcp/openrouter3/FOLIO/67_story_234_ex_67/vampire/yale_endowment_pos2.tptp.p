% Yale University Endowment Problem - Positive Version
% Using tff for typed arithmetic

tff(university_type, type, university: $tType).
tff(endowment_type, type, endowment_value: (university, $int) > $o).

tff(yale_decl, type, yale: university).
tff(yale_endowment_val, axiom, endowment_value(yale, 42300000000)).

% Define what it means to have the largest endowment
% For all universities U and values V, if U has endowment V, then Yale's endowment >= V
tff(largest_endowment_def, axiom,
    ! [U: university, V: $int] : 
        (endowment_value(U, V) => $greatereq(42300000000, V))).

% Conclusion: Yale has the largest endowment
fof(goal, conjecture, largest_endowment(yale)).