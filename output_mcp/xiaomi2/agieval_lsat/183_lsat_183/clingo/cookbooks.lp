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

% For each option, count how many valid assignments satisfy its condition
% Option A: K=fall, L=spring
cnt_a(N) :- N = #count { K,L,M,N2,O,P : 
    season(k,K), season(l,L), season(m,M), season(n,N2), season(o,O), season(p,P),
    K=fall, L=spring }.

% Option B: O=fall, P=spring
cnt_b(N) :- N = #count { K,L,M,N2,O,P : 
    season(k,K), season(l,L), season(m,M), season(n,N2), season(o,O), season(p,P),
    O=fall, P=spring }.

% Option C: P=fall, L=spring
cnt_c(N) :- N = #count { K,L,M,N2,O,P : 
    season(k,K), season(l,L), season(m,M), season(n,N2), season(o,O), season(p,P),
    P=fall, L=spring }.

% Option D: K=spring, L=spring
cnt_d(N) :- N = #count { K,L,M,N2,O,P : 
    season(k,K), season(l,L), season(m,M), season(n,N2), season(o,O), season(p,P),
    K=spring, L=spring }.

% Option E: M=fall, L=fall
cnt_e(N) :- N = #count { K,L,M,N2,O,P : 
    season(k,K), season(l,L), season(m,M), season(n,N2), season(o,O), season(p,P),
    M=fall, L=fall }.

% An option fully determines the schedule if exactly 1 assignment satisfies it
option(a) :- cnt_a(1).
option(b) :- cnt_b(1).
option(c) :- cnt_c(1).
option(d) :- cnt_d(1).
option(e) :- cnt_e(1).

#show option/1.