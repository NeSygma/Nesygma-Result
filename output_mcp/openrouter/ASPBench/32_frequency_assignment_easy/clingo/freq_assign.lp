% Domains
transmitter(a;b;c;d;e;f).
freq(1..5).

% Interference edges (undirected, each pair once)
edge(a,b).
edge(a,c).
edge(b,d).
edge(b,e).
edge(c,d).
edge(c,f).
edge(d,e).
edge(e,f).

% Assignment: exactly one frequency per transmitter
1 { assign(T,F) : freq(F) } 1 :- transmitter(T).

% Used frequencies
used(F) :- assign(_,F).

% Constraints: interfering transmitters cannot have same or adjacent frequencies
:- assign(X,F), assign(Y,F), edge(X,Y).            % same frequency
:- assign(X,F), assign(Y,G), edge(X,Y), F = G + 1. % F is one higher than G
:- assign(X,F), assign(Y,G), edge(X,Y), G = F + 1. % G is one higher than F

% Minimize number of distinct frequencies used
#minimize { 1,F : used(F) }.

% Compute total distinct frequencies used
frequencies_used(N) :- N = #count{F : used(F)}.

#show assign/2.
#show frequencies_used/1.