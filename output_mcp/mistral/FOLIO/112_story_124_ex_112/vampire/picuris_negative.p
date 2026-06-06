fof(picuris_in_nm_or_tx, axiom, (mountain_range_in(picuris_mountains, new_mexico) | mountain_range_in(picuris_mountains, texas))).
fof(juan_visited_picuris, axiom, visited(juan_de_onate, picuris_mountains)).
fof(harding_mine_in_picuris, axiom, mine_in(harding_pegmatite_mine, picuris_mountains)).
fof(harding_mine_donated, axiom, donated(harding_pegmatite_mine)).
fof(no_donated_mines_in_tx_ranges, axiom, ! [M, Mine] : ((mountain_range_in(M, texas) & mine_in(Mine, M) & donated(Mine)) => false)).
fof(conclusion_negation, conjecture, ~(? [M] : (visited(juan_de_onate, M) & mountain_range_in(M, new_mexico)))).