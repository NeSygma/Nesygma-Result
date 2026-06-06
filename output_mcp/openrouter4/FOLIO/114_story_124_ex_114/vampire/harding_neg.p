% Negative file: negated conjecture
% Negation: The Harding Pegmatite Mine IS located in a mountain range in New Mexico.
% i.e., ?[R] : (mountain_range(R) & in_state(R, new_mexico) & located_in(harding_pegmatite_mine, R))

fof(premise1_part1, axiom, mountain_range(picuris_mountains)).
fof(premise1_part2, axiom,
    ( in_state(picuris_mountains, new_mexico)
    | in_state(picuris_mountains, texas) )).

fof(premise2, axiom, visited(juan_de_onate, picuris_mountains)).

fof(premise3_part1, axiom, mine(harding_pegmatite_mine)).
fof(premise3_part2, axiom, located_in(harding_pegmatite_mine, picuris_mountains)).
fof(premise3_part3, axiom, donated(harding_pegmatite_mine)).

fof(premise4, axiom,
    ! [R] :
        ( ( mountain_range(R)
          & in_state(R, texas) )
       => ~ ? [M] :
              ( mine(M)
              & located_in(M, R)
              & donated(M) ) )).

fof(goal, conjecture,
    ? [R] :
        ( mountain_range(R)
        & in_state(R, new_mexico)
        & located_in(harding_pegmatite_mine, R) )).