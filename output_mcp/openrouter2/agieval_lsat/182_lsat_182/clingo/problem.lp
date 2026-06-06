% Facts: books and seasons
book(k). book(l). book(m). book(n). book(o). book(p).
season(fall). season(spring).

% Each book assigned to exactly one season
1 { season_of(Book, S) : season(S) } 1 :- book(Book).

% Constraints
% M and P not same season
:- season_of(m, S), season_of(p, S).

% K and N same season
:- season_of(k, S1), season_of(n, S2), S1 != S2.

% If K fall then O fall
:- season_of(k, fall), not season_of(o, fall).

% If M fall then N spring
:- season_of(m, fall), not season_of(n, spring).

% N is fall
season_of(n, fall).

% Force L fall to show option B could be true
season_of(l, fall).

% Option mapping
option(a) :- season_of(k, spring).
option(b) :- season_of(l, fall).
option(c) :- season_of(m, fall).
option(d) :- season_of(o, spring).
option(e) :- season_of(p, spring).

#show option/1.