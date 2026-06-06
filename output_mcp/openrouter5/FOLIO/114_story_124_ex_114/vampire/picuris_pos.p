% Positive version: original conclusion as conjecture
% Conclusion: The Harding Pegmatite Mine is not located in a mountain range in New Mexico.

% Predicates:
% mountain_range_in(X, Y) - X is a mountain range in Y (Y is a state/region)
% visited(X, Y) - X visited Y
% located_in(X, Y) - X is located in Y
% mine(X) - X is a mine
% donated(X) - X was donated

% Constants:
% picuris_mountains - the Picuris Mountains
% new_mexico - New Mexico
% texas - Texas
% juan_de_onate - Juan de Onate
% harding_pegmatite_mine - the Harding Pegmatite Mine

% Premise 1: The Picuris Mountains are a mountain range in New Mexico or Texas.
fof(premise1, axiom,
    mountain_range_in(picuris_mountains, new_mexico) | mountain_range_in(picuris_mountains, texas)).

% Premise 2: Juan de Onate visited the Picuris Mountains.
fof(premise2, axiom, visited(juan_de_onate, picuris_mountains)).

% Premise 3: The Harding Pegmatite Mine, located in the Picuris Mountains, was donated.
fof(premise3, axiom, located_in(harding_pegmatite_mine, picuris_mountains) & donated(harding_pegmatite_mine)).

% Premise 4: There are no mountain ranges in Texas that have mines that have been donated.
fof(premise4, axiom,
    ! [R, M] : ((mountain_range_in(R, texas) & located_in(M, R) & mine(M) & donated(M)) => $false)).
% Equivalently: ~? [R, M] : (mountain_range_in(R, texas) & located_in(M, R) & mine(M) & donated(M))

% The Harding Pegmatite Mine is a mine.
fof(mine_fact, axiom, mine(harding_pegmatite_mine)).

% Conclusion: The Harding Pegmatite Mine is not located in a mountain range in New Mexico.
% i.e., ~? [R] : (mountain_range_in(R, new_mexico) & located_in(harding_pegmatite_mine, R))
fof(conclusion, conjecture,
    ~? [R] : (mountain_range_in(R, new_mexico) & located_in(harding_pegmatite_mine, R))).