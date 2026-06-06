% --- Domains ---
transmitter(a; b; c; d; e; f).
frequency(1..5).

% --- Interference graph (undirected) ---
interfere(a, b). interfere(a, c).
interfere(b, a). interfere(b, d). interfere(b, e).
interfere(c, a). interfere(c, d). interfere(c, f).
interfere(d, b). interfere(d, c). interfere(d, e).
interfere(e, b). interfere(e, d). interfere(e, f).
interfere(f, c). interfere(f, e).

% --- Assignment: each transmitter gets exactly one frequency ---
1 { assign(T, F) : frequency(F) } 1 :- transmitter(T).

% --- Constraint 2: Interfering transmitters cannot share the same frequency ---
:- interfere(T1, T2), assign(T1, F), assign(T2, F).

% --- Constraint 3: Interfering transmitters cannot use adjacent frequencies ---
:- interfere(T1, T2), assign(T1, F1), assign(T2, F2), |F1 - F2| = 1.

% --- Objective: minimize total number of distinct frequencies used ---
% Mark a frequency as used if any transmitter is assigned it
used_freq(F) :- assign(_, F).

% Minimize the count of distinct frequencies
#minimize { 1, F : used_freq(F) }.

% --- Output ---
#show assign/2.
#show used_freq/1.