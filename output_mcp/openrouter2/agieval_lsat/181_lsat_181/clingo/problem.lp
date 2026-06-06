% Domain facts
cookbook(k). cookbook(l). cookbook(m). cookbook(n). cookbook(o). cookbook(p).
season_name(fall). season_name(spring).

% Each cookbook has exactly one season
1 { season(C, S) : season_name(S) } 1 :- cookbook(C).

% Constraints
% M and P cannot be same season
:- season(m, S), season(p, S).

% K and N same season
:- season(k, S1), season(n, S2), S1 != S2.

% If K fall then O fall
:- season(k, fall), not season(o, fall).

% If M fall then N spring
:- season(m, fall), not season(n, spring).

% M must be fall
:- not season(m, fall).

% Option mapping
option(a) :- season(k, fall), season(o, fall).
option(b) :- season(l, fall), season(n, fall).
option(c) :- season(l, fall), season(o, fall).
option(d) :- season(n, fall), season(p, fall).
option(e) :- season(o, fall), season(p, fall).

% Enforce uniqueness: only option(c) can be true
:- option(a).
:- option(b).
:- option(d).
:- option(e).
:- not option(c).

#show option/1.