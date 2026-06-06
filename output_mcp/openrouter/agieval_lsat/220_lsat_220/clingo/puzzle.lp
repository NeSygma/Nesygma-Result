% Students and types
student(franz). student(greene). student(hidalgo). student(isaacs).

type(oil). type(watercolor).

wall(1..4).
pos(upper; lower).

% Each painting placed exactly once (exactly one wall and position)
1 { placed(S,T,W,P) : wall(W), pos(P) } 1 :- student(S), type(T).
% Each wall position has exactly one painting
1 { placed(S,T,W,P) : student(S), type(T) } 1 :- wall(W), pos(P).

% No wall has only watercolors (must have at least one oil)
 oil_on_wall(W) :- placed(_, oil, W, _).
:- wall(W), not oil_on_wall(W).

% No wall has work of only one student (must have at least two distinct students)
 two_students_on_wall(W) :- placed(S1,_,W,_), placed(S2,_,W,_), S1 != S2.
:- wall(W), not two_students_on_wall(W).

% No wall has both Franz and Isaacs
:- placed(franz,_,W,_), placed(isaacs,_,W,_).

% Greene's watercolor is upper on same wall as Franz's oil
placed(greene, watercolor, W, upper) :- placed(franz, oil, W, _).
% Ensure Greene's watercolor not elsewhere (derived placement ensures uniqueness via exactly-one rule)

% Isaacs's oil lower on wall 4
placed(isaacs, oil, 4, lower).

% Scenario facts: Isaacs's watercolor on wall 2, Franz's oil on wall 3
:- not placed(isaacs, watercolor, 2, _).
:- not placed(franz, oil, 3, _).

% Map options for wall 1
option(a) :- placed(franz, watercolor, 1, _).
option(b) :- placed(greene, oil, 1, _).
option(c) :- placed(greene, watercolor, 1, _).
option(d) :- placed(hidalgo, oil, 1, _).
option(e) :- placed(hidalgo, watercolor, 1, _).

#show option/1.