% Positive version: original conclusion as conjecture
% Juan de Onate visited a mountain range in Texas.

% Predicates:
% mountain_range_in(X, Y) - X is a mountain range in Y (Y is a state)
% visited(X, Y) - X visited Y
% located_in(X, Y) - X is located in Y
% mine(X) - X is a mine
% donated(X) - X was donated

% Constants:
% picuris_mountains - the Picuris Mountains
% juan_de_onate - Juan de Onate
% harding_pegmatite_mine - the Harding Pegmatite Mine
% new_mexico - New Mexico
% texas - Texas

fof(distinct_states, axiom, new_mexico != texas).

fof(premise1, axiom,
    mountain_range_in(picuris_mountains, new_mexico)
    | mountain_range_in(picuris_mountains, texas)).

fof(premise2, axiom, visited(juan_de_onate, picuris_mountains)).

fof(premise3, axiom, located_in(harding_pegmatite_mine, picuris_mountains)).
fof(premise4, axiom, mine(harding_pegmatite_mine)).
fof(premise5, axiom, donated(harding_pegmatite_mine)).

fof(premise6, axiom,
    ! [R, M] : (
        (mountain_range_in(R, texas) & mine(M) & located_in(M, R) & donated(M))
        => $false
    )).

% Equivalently: There are no mountain ranges in Texas that have mines that have been donated.
% So: ~? [R, M] : (mountain_range_in(R, texas) & mine(M) & located_in(M, R) & donated(M))
% Which is: ! [R, M] : ~(mountain_range_in(R, texas) & mine(M) & located_in(M, R) & donated(M))

fof(goal, conjecture,
    ? [R] : (mountain_range_in(R, texas) & visited(juan_de_onate, R))).