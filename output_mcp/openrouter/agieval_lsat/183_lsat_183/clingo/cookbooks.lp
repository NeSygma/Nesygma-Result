% Books
book(k). book(l). book(m). book(n). book(o). book(p).

% Choice of season for each book (first assignment)
{season(B, fall); season(B, spring)} 1 :- book(B).
% Choice of season for each book (second assignment for uniqueness check)
{season2(B, fall); season2(B, spring)} 1 :- book(B).

% Base constraints (apply to both assignments)
% M and P cannot be same season
:- season(m, S), season(p, S).
:- season2(m, S), season2(p, S).
% K and N must be same season
:- season(k, S1), season(n, S2), S1 != S2.
:- season2(k, S1), season2(n, S2), S1 != S2.
% If K fall then O fall
:- season(k, fall), season(o, spring).
:- season2(k, fall), season2(o, spring).
% If M fall then N spring (i.e., N cannot be fall)
:- season(m, fall), season(n, fall).
:- season2(m, fall), season2(n, fall).

% Exactly one option assumption
1 {assume_a; assume_b; assume_c; assume_d; assume_e} 1.

% Option A: K fall, L spring
season(k, fall) :- assume_a.
season(l, spring) :- assume_a.
season2(k, fall) :- assume_a.
season2(l, spring) :- assume_a.

% Option B: O fall, P spring
season(o, fall) :- assume_b.
season(p, spring) :- assume_b.
season2(o, fall) :- assume_b.
season2(p, spring) :- assume_b.

% Option C: P fall, L spring
season(p, fall) :- assume_c.
season(l, spring) :- assume_c.
season2(p, fall) :- assume_c.
season2(l, spring) :- assume_c.

% Option D: K and L spring
season(k, spring) :- assume_d.
season(l, spring) :- assume_d.
season2(k, spring) :- assume_d.
season2(l, spring) :- assume_d.

% Option E: M and L fall
season(m, fall) :- assume_e.
season(l, fall) :- assume_e.
season2(m, fall) :- assume_e.
season2(l, fall) :- assume_e.

% Uniqueness constraint: for the chosen option, the two assignments must not differ
:- assume_a, season(B,S), season2(B,S2), S != S2.
:- assume_b, season(B,S), season2(B,S2), S != S2.
:- assume_c, season(B,S), season2(B,S2), S != S2.
:- assume_d, season(B,S), season2(B,S2), S != S2.
:- assume_e, season(B,S), season2(B,S2), S != S2.

% Derive the selected option
option(a) :- assume_a.
option(b) :- assume_b.
option(c) :- assume_c.
option(d) :- assume_d.
option(e) :- assume_e.

#show option/1.