% Positive claim: Juan visited a Texas mountain range
fof(mountain_range_picuris, axiom, mountain_range(picuris_mountains)).
fof(location_picuris, axiom, location(picuris_mountains, new_mexico) | location(picuris_mountains, texas)).
fof(juan_visited_picuris, axiom, visited(juan_de_onate, picuris_mountains)).
fof(harding_mine, axiom, mine(harding_pegmatite_mine)).
fof(harding_located, axiom, located_in(harding_pegmatite_mine, picuris_mountains)).
fof(harding_donated, axiom, donated(harding_pegmatite_mine)).
% No Texas mountain range has a donated mine
fof(no_texas_range_with_donated_mine, axiom, ![M,N] : ((mountain_range(M) & location(M, texas) & mine(N) & located_in(N, M) & donated(N)) => $false)).
% Distinctness of locations
fof(distinct_locations, axiom, new_mexico != texas).
% Goal: there exists a Texas mountain range visited by Juan
fof(goal, conjecture, ?[M] : (mountain_range(M) & location(M, texas) & visited(juan_de_onate, M))).