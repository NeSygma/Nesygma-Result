% Facts
mountain_range(picuris).
mine_location(harding_pegmatite, picuris).
donated(harding_pegmatite).

% Choice rule for location of picuris
{ location(picuris, new_mexico); location(picuris, texas) } 1.

% Constraint: no donated mine in Texas mountain ranges
:- location(M, texas), mine_location(X, M), donated(X).

% Derive that mine is in a mountain range in New Mexico
mine_in_new_mexico(Mine) :- mine_location(Mine, M), mountain_range(M), location(M, new_mexico).

% Derive conclusion_false if mine is in New Mexico
conclusion_false :- mine_in_new_mexico(harding_pegmatite).

% No rule for conclusion_true

% Answer mapping
answer(true)      :- conclusion_true.
answer(false)     :- conclusion_false.
answer(uncertain) :- not conclusion_true, not conclusion_false.
answer(inconsistent) :- conclusion_true, conclusion_false.

#show answer/1.