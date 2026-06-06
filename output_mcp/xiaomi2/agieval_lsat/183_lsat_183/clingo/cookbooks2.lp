% Domain definitions
cookbook(k). cookbook(l). cookbook(m). cookbook(n). cookbook(o). cookbook(p).
season(fall). season(spring).

% Each cookbook is assigned to exactly one season
{ season(C, S) : season(S) } 1 :- cookbook(C).

% Base constraints
:- season(m, S), season(p, S).                     % M and P cannot be in the same season
:- season(k, S1), season(n, S2), S1 != S2.         % K and N must be in the same season
:- season(k, fall), not season(o, fall).           % If K is fall then O must be fall
:- season(m, fall), not season(n, spring).         % If M is fall then N must be spring

% Show all season assignments
#show season/2.