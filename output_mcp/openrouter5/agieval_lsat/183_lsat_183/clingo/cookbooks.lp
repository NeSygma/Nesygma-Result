% Define seasons
season(fall; spring).

% Define cookbooks
cookbook(k; l; m; n; o; p).

% Each cookbook is published in exactly one season
1 { pub(C, S) : season(S) } 1 :- cookbook(C).

% Condition 1: M and P cannot be in the same season
:- pub(m, S), pub(p, S).

% Condition 2: K and N must be in the same season
:- pub(k, S1), pub(n, S2), S1 != S2.

% Condition 3: If K is in fall, O must be in fall
:- pub(k, fall), not pub(o, fall).

% Condition 4: If M is in fall, N must be in spring
:- pub(m, fall), not pub(n, spring).

% Now we need to determine which option fully determines the schedule.
% An option fully determines the schedule if adding it as a constraint
% results in exactly one valid assignment.

% Let's enumerate all valid schedules and check each option.

% First, let's find all solutions by just running the base constraints.
#show pub/2.