% Negative version: negated conclusion as conjecture
% It is NOT the case that Juan de Onate visited a mountain range in New Mexico.

fof(premise1, axiom,
    mountain_range_in(picuris_mountains, new_mexico) | mountain_range_in(picuris_mountains, texas)).

fof(premise2, axiom,
    visited(juan_de_onate, picuris_mountains)).

fof(premise3, axiom,
    (mine(harding_pegmatite_mine) & located_in(harding_pegmatite_mine, picuris_mountains) & donated(harding_pegmatite_mine))).

fof(premise4, axiom,
    ! [R, M] : ((mountain_range_in(R, texas) & mine(M) & located_in(M, R) & donated(M)) => $false)).

fof(negated_conclusion, conjecture,
    ~ ? [R] : (mountain_range_in(R, new_mexico) & visited(juan_de_onate, R))).