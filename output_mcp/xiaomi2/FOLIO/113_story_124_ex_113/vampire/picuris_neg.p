fof(picuris_is_range, axiom, mountain_range(picuris_mountains)).
fof(picuris_in_nm_or_tx, axiom,
    (in_state(picuris_mountains, new_mexico) | in_state(picuris_mountains, texas))).
fof(onate_visited_picuris, axiom, visited(juan_de_onate, picuris_mountains)).
fof(harding_is_mine, axiom, mine(harding_pegmatite_mine)).
fof(harding_in_picuris, axiom, located_in(harding_pegmatite_mine, picuris_mountains)).
fof(harding_donated, axiom, donated(harding_pegmatite_mine)).
fof(no_tx_range_with_donated_mine, axiom,
    ! [X, M] : ~((mountain_range(X) & in_state(X, texas) & mine(M) & located_in(M, X) & donated(M)))).
fof(conclusion_negated, conjecture,
    ~? [X] : (mountain_range(X) & in_state(X, texas) & visited(juan_de_onate, X))).