% --- Domain Definitions ---
transmitter(a; b; c; d; e; f).
frequency(1..5).

% --- Interference Graph ---
interfere(a, b). interfere(a, c).
interfere(b, a). interfere(b, d). interfere(b, e).
interfere(c, a). interfere(c, d). interfere(c, f).
interfere(d, b). interfere(d, c). interfere(d, e).
interfere(e, b). interfere(e, d). interfere(e, f).
interfere(f, c). interfere(f, e).

% --- Symmetric interference ---
interfere(X, Y) :- interfere(Y, X).

% --- Assignment: each transmitter gets exactly one frequency ---
1 { assign(T, F) : frequency(F) } 1 :- transmitter(T).

% --- Constraint 2: Interfering transmitters cannot use the same frequency ---
:- interfere(T1, T2), assign(T1, F), assign(T2, F).

% --- Constraint 3: Interfering transmitters cannot use adjacent frequencies ---
:- interfere(T1, T2), assign(T1, F1), assign(T2, F2), |F1 - F2| = 1.

% --- Objective: Minimize the total number of distinct frequencies used ---
used_freq(F) :- assign(_, F).
num_frequencies_used(N) :- N = #count { F : used_freq(F) }.

#minimize { N : num_frequencies_used(N) }.

% --- Output ---
#show assign/2.
#show num_frequencies_used/1.