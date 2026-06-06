fof(picuris_in_nm_or_tx, axiom,
    is_mountain_range_in(picuris_mountains, new_mexico) |
    is_mountain_range_in(picuris_mountains, texas)).

fof(juan_visited_picuris, axiom,
    visited(juan_de_onate, picuris_mountains)).

fof(harding_mine_donated, axiom,
    located_in(harding_pegmatite_mine, picuris_mountains) &
    donated(harding_pegmatite_mine)).

fof(no_donated_mine_in_tx, axiom,
    ~(is_mountain_range_in(picuris_mountains, texas) &
      located_in(harding_pegmatite_mine, picuris_mountains) &
      donated(harding_pegmatite_mine))).

fof(conclusion, conjecture,
    ? [M] : (visited(juan_de_onate, M) & is_mountain_range_in(M, new_mexico))).