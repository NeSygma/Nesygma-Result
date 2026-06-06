fof(picuris_is_mountain_range, axiom,
    mountain_range(picuris_mountains)).

fof(picuris_in_nm_or_tx, axiom,
    in_state(picuris_mountains, new_mexico) | in_state(picuris_mountains, texas)).

fof(juan_visited_picuris, axiom,
    visited(juan_de_onate, picuris_mountains)).

fof(harding_in_picuris, axiom,
    located_in(harding_pegmatite_mine, picuris_mountains)).

fof(harding_donated, axiom,
    donated(harding_pegmatite_mine)).

fof(no_donated_mines_in_tx, axiom,
    ! [R, M] : ((mountain_range(R) & in_state(R, texas) & located_in(M, R) & donated(M)) => $false)).

% Conclusion: Harding Pegmatite Mine is NOT located in a mountain range in New Mexico.
fof(goal, conjecture,
    ~? [R] : (mountain_range(R) & in_state(R, new_mexico) & located_in(harding_pegmatite_mine, R))).