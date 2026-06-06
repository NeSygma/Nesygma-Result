fof(picuris_is_range, axiom,
    mountain_range(picuris_mountains)).

fof(picuris_nm_or_tx, axiom,
    (in_location(picuris_mountains, new_mexico) | in_location(picuris_mountains, texas))).

fof(onate_visited, axiom,
    visited(juan_de_onate, picuris_mountains)).

fof(harding_is_mine, axiom,
    mine(harding_pegmatite_mine)).

fof(harding_in_picuris, axiom,
    in_location(harding_pegmatite_mine, picuris_mountains)).

fof(harding_donated, axiom,
    donated(harding_pegmatite_mine)).

fof(no_donated_mine_in_tx_range, axiom,
    ! [X, Y] : ~((mountain_range(X) & in_location(X, texas) & mine(Y) & in_location(Y, X) & donated(Y)))).

fof(goal, conjecture,
    ~? [X] : (mountain_range(X) & in_location(X, new_mexico) & visited(juan_de_onate, X))).