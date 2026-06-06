fof(picuris_is_mountain_range, axiom, mountain_range(picuris_mountains)).

fof(picuris_in_nm_or_tx, axiom,
    (in_state(picuris_mountains, new_mexico) | in_state(picuris_mountains, texas))).

fof(juan_visited_picuris, axiom, visited(juan_de_onate, picuris_mountains)).

fof(harding_is_mine, axiom, mine(harding_pegmatite_mine)).

fof(harding_in_picuris, axiom, in_state(harding_pegmatite_mine, picuris_mountains)).

fof(harding_donated, axiom, donated(harding_pegmatite_mine)).

fof(no_tx_mountain_with_donated_mine, axiom,
    ! [X, Y] : ((mountain_range(X) & in_state(X, texas) & mine(Y) & in_state(Y, X) & donated(Y)) => $false)).

fof(goal, conjecture,
    ~? [X] : (mountain_range(X) & in_state(X, texas) & visited(juan_de_onate, X))).