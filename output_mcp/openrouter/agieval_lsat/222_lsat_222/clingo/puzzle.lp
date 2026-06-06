% Domains
student(franz). student(greene). student(hidalgo). student(isaacs).
type(oil). type(watercolor).
wall(1). wall(2). wall(3). wall(4).
pos(upper). pos(lower).

% Assignment: each painting to exactly one slot
1 { loc(S,T,W,P) : wall(W), pos(P) } 1 :- student(S), type(T).
% each slot gets exactly one painting
1 { loc(S,T,W,P) : student(S), type(T) } 1 :- wall(W), pos(P).

% Constraints
% No wall has only watercolors (i.e., each wall must have at least one oil)
oil_on_wall(W) :- loc(_, oil, W, _).
:- wall(W), not oil_on_wall(W).

% No wall has work of only one student (must have at least two distinct students)
two_students_on_wall(W) :- loc(S1,_,W,_), loc(S2,_,W,_), S1 != S2.
:- wall(W), not two_students_on_wall(W).

% No wall has both Franz and Isaacs
:- wall(W), loc(franz,_,W,_), loc(isaacs,_,W,_).

% Greene's watercolor is upper and same wall as Franz's oil (which must be lower)
% Force Greene watercolor not lower
:- loc(greene, watercolor, _, lower).
% Ensure Franz oil lower on same wall as Greene watercolor upper
:- loc(greene, watercolor, W, upper), not loc(franz, oil, W, lower).

% Isaacs oil lower wall 4
:- not loc(isaacs, oil, 4, lower).

% Scenario condition: Greene oil same wall as Franz watercolor
same_wall_condition :- loc(greene, oil, W, _), loc(franz, watercolor, W, _).
:- not same_wall_condition.

% Options
option(a) :- loc(greene, oil, _, upper).
option(b) :- loc(hidalgo, watercolor, W, _), loc(isaacs, watercolor, W, _).
option(c) :- loc(hidalgo, oil, _, upper).
option(d) :- loc(hidalgo, oil, W, _), loc(isaacs, watercolor, W, _).
option(e) :- loc(isaacs, watercolor, _, lower).

% Exactly one option must hold
1 { option(a); option(b); option(c); option(d); option(e) } 1.

#show option/1.