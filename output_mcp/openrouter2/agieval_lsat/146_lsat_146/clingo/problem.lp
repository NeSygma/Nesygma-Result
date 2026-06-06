% Facts
hist(farley). hist(garcia). hist(holden). hist(jiang).

topic(lithographs). topic(oil). topic(sculptures). topic(watercolors).

pos(1). pos(2). pos(3). pos(4).

% Each historian gives exactly one lecture
1 { lecture(H, T, P) : topic(T), pos(P) } 1 :- hist(H).

% Each topic is assigned to exactly one historian
1 { lecture(H, T, P) : hist(H) } 1 :- topic(T).

% Each position has exactly one lecture
1 { lecture(H, T, P) : hist(H), topic(T) } 1 :- pos(P).

% Watercolors lecture is at position 3
1 { lecture(H, watercolors, 3) : hist(H) } 1.

% Constraints
:- lecture(_, oil, P_o), lecture(_, lithographs, P_l), P_o >= P_l.
:- lecture(_, watercolors, P_w), lecture(_, lithographs, P_l), P_w >= P_l.
:- lecture(farley, _, P_f), lecture(_, oil, P_o), P_f >= P_o.
:- lecture(holden, _, P_h), lecture(garcia, _, P_g), P_h >= P_g.
:- lecture(holden, _, P_h), lecture(jiang, _, P_j), P_h >= P_j.

% Options
option(a) :- lecture(farley, watercolors, 3).
option(b) :- lecture(garcia, oil, _).
option(c) :- lecture(garcia, sculptures, _).
option(d) :- lecture(holden, sculptures, _).
option(e) :- lecture(jiang, lithographs, _).

% Ensure exactly one option
:- not option(a), not option(b), not option(c), not option(d), not option(e).
:- option(a), option(b).
:- option(a), option(c).
:- option(a), option(d).
:- option(a), option(e).
:- option(b), option(c).
:- option(b), option(d).
:- option(b), option(e).
:- option(c), option(d).
:- option(c), option(e).
:- option(d), option(e).

#show option/1.