% Negative version: negated conclusion as conjecture
% Juan de Onate did NOT visit a mountain range in Texas.

fof(distinct_states, axiom, new_mexico != texas).

fof(premise1, axiom,
    mountain_range_in(picuris_mountains, new_mexico)
    | mountain_range_in(picuris_mountains, texas)).

fof(premise2, axiom, visited(juan_de_onate, picuris_mountains)).

fof(premise3, axiom, located_in(harding_pegmatite_mine, picuris_mountains)).
fof(premise4, axiom, mine(harding_pegmatite_mine)).
fof(premise5, axiom, donated(harding_pegmatite_mine)).

fof(premise6, axiom,
    ! [R, M] : (
        (mountain_range_in(R, texas) & mine(M) & located_in(M, R) & donated(M))
        => $false
    )).

fof(goal_neg, conjecture,
    ~ ? [R] : (mountain_range_in(R, texas) & visited(juan_de_onate, R))).