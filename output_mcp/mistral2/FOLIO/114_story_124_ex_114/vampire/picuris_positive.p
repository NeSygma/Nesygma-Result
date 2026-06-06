fof(picuris_in_nm_or_tx, axiom, mountain_range_in(picuris_mountains, new_mexico) | mountain_range_in(picuris_mountains, texas)).
fof(juan_visited, axiom, visited_by(juan_de_onate, picuris_mountains)).
fof(harding_donated, axiom, located_in(harding_pegmatite_mine, picuris_mountains) & donated(harding_pegmatite_mine)).
fof(no_donated_mines_in_tx, axiom, ! [M] : (mountain_range_in(M, texas) & has_donated_mine(M) => $false)).
fof(harding_in_picuris, axiom, located_in(harding_pegmatite_mine, picuris_mountains)).

fof(harding_in_tx_implies_has_donated_mine, axiom,
    located_in(harding_pegmatite_mine, texas) => has_donated_mine(picuris_mountains)).

fof(picuris_in_tx_implies_harding_in_tx, axiom,
    (mountain_range_in(picuris_mountains, texas) & located_in(harding_pegmatite_mine, picuris_mountains))
    => located_in(harding_pegmatite_mine, texas)).

fof(picuris_in_tx_and_has_donated_mine_implies_false, axiom,
    (mountain_range_in(picuris_mountains, texas) & has_donated_mine(picuris_mountains)) => $false).

fof(conclusion, conjecture, ~located_in(harding_pegmatite_mine, new_mexico)).