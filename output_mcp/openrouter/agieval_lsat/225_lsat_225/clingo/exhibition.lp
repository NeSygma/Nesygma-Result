% Students and types
student(franz). student(greene). student(hidalgo). student(isaacs).
type(oil). type(water).
pos(upper). pos(lower).
wall(1..4).

% Paintings as terms
paint(S,T) :- student(S), type(T).

% Each painting assigned to exactly one wall and position
1 { location(paint(S,T), W, P) : wall(W), pos(P) } 1 :- student(S), type(T).

% Each wall has exactly one upper and one lower painting
1 { location(paint(S,T), W, upper) : student(S), type(T) } 1 :- wall(W).
1 { location(paint(S,T), W, lower) : student(S), type(T) } 1 :- wall(W).

% No wall has only watercolors (must have at least one oil)
oil_on_wall(W) :- location(paint(_, oil), W, _).
:- wall(W), not oil_on_wall(W).

% No wall has both paintings of same student (i.e., oil and water of same student)
:- location(paint(S, oil), W, _), location(paint(S, water), W, _).

% No wall has both Franz and Isaacs paintings
:- location(paint(franz,_), W, _), location(paint(isaacs,_), W, _).

% Greene's watercolor is upper on the wall where Franz's oil is displayed
% Force Greene's watercolor to be upper
:- location(paint(greene, water), _, P), P != upper.
% Same wall as Franz's oil
:- location(paint(greene, water), W, upper), not location(paint(franz, oil), W, _).

% Isaacs's oil is lower on wall 4
location(paint(isaacs, oil), 4, lower).

% Options definitions (possible conditions)
possible_a :- location(paint(franz, water), W, _), location(paint(greene, oil), W, _).
possible_b :- location(paint(franz, water), W, _), location(paint(hidalgo, oil), W, _).
possible_c :- location(paint(greene, oil), _, upper).
possible_d :- location(paint(hidalgo, water), _, lower).
possible_e :- location(paint(isaacs, water), W, _), location(paint(hidalgo, oil), W, _).

% Derive option when the corresponding possibility is impossible
option(a) :- not possible_a.
option(b) :- not possible_b.
option(c) :- not possible_c.
option(d) :- not possible_d.
option(e) :- not possible_e.

#show option/1.