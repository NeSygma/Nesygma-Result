% ===== DOMAIN =====
transmitter(a). transmitter(b). transmitter(c).
transmitter(d). transmitter(e). transmitter(f).

frequency(1). frequency(2). frequency(3). frequency(4). frequency(5).

% ===== INTERFERENCE GRAPH (symmetric, listed once per pair) =====
interferes(a, b). interferes(a, c).
interferes(b, d). interferes(b, e).
interferes(c, d). interferes(c, f).
interferes(d, e).
interferes(e, f).

% Make it symmetric
interferes(X, Y) :- interferes(Y, X).

% ===== ASSIGNMENT =====
% Each transmitter gets exactly one frequency
1 { assign(T, F) : frequency(F) } 1 :- transmitter(T).

% ===== CONSTRAINTS =====
% Interfering transmitters cannot use the same frequency
:- interferes(T1, T2), assign(T1, F), assign(T2, F).

% Interfering transmitters cannot use adjacent frequencies (differ by 1)
:- interferes(T1, T2), assign(T1, F1), assign(T2, F2), |F1 - F2| = 1.

% ===== OPTIMIZATION =====
% Track which frequencies are used
used(F) :- assign(_, F).

% Minimize the number of distinct frequencies used
#minimize { 1, F : used(F) }.

% ===== OUTPUT =====
#show assign/2.
#show used/1.