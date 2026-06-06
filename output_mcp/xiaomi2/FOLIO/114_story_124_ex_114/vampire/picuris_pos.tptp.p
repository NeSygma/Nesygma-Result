fof(p1, axiom,
    ( mountain_range(picuris_mountains)
    & ( in_state(picuris_mountains, new_mexico)
      | in_state(picuris_mountains, texas) ) )).

fof(p2, axiom,
    visited(juan_de_onate, picuris_mountains)).

fof(p3, axiom,
    ( mine(harding_pegmatite_mine)
    & located_in(harding_pegmatite_mine, picuris_mountains)
    & donated(harding_pegmatite_mine) )).

fof(p4, axiom,
    ! [X, Y] : ~(
        mountain_range(X)
      & in_state(X, texas)
      & mine(Y)
      & located_in(Y, X)
      & donated(Y) )).

fof(distinct, axiom,
    new_mexico != texas).

% Conclusion: The Harding Pegmatite Mine is NOT located in a mountain range in New Mexico.
fof(goal, conjecture,
    ~ ? [X] : (
        located_in(harding_pegmatite_mine, X)
      & mountain_range(X)
      & in_state(X, new_mexico) )).