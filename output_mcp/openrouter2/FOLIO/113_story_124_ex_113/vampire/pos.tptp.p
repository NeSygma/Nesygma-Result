fof(distinct, axiom, (picuris != new_mexico & picuris != texas & new_mexico != texas & jde_onate != picuris & jde_onate != new_mexico & jde_onate != texas & harding_pegmatite != picuris & harding_pegmatite != new_mexico & harding_pegmatite != texas & harding_pegmatite != jde_onate)).
fof(mountain_range_picuris, axiom, mountain_range(picuris)).
fof(visited_jde_onate_picuris, axiom, visited(jde_onate, picuris)).
fof(mine_harding_pegmatite, axiom, mine(harding_pegmatite)).
fof(located_harding_pegmatite_picuris, axiom, located_in(harding_pegmatite, picuris)).
fof(donated_harding_pegmatite, axiom, donated(harding_pegmatite)).
fof(picuris_in_state, axiom, (in_state(picuris, new_mexico) | in_state(picuris, texas))).
fof(no_donated_mines_in_texas, axiom, ! [M] : (in_state(M, texas) => ! [N] : ((mine(N) & located_in(N, M) & donated(N)) => false))).
fof(conjecture, conjecture, ? [M] : (visited(jde_onate, M) & in_state(M, texas) & mountain_range(M))).