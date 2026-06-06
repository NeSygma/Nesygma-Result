% --- Domains ---
transmitter(a; b; c; d; e; f).
frequency(1..5).

% --- Interference Graph ---
interferes(a, b). interferes(b, a).
interferes(a, c). interferes(c, a).
interferes(b, d). interferes(d, b).
interferes(b, e). interferes(e, b).
interferes(c, d). interferes(d, c).
interferes(c, f). interferes(f, c).
interferes(d, e). interferes(e, d).
interferes(e, f). interferes(f, e).

% --- Assignment ---
% Each transmitter must be assigned exactly one frequency
1 { assigned(T, F) : frequency(F) } 1 :- transmitter(T).

% --- Constraints ---
% 1. Interfering transmitters cannot use the same frequency
:- assigned(T1, F), assigned(T2, F), interferes(T1, T2).

% 2. Interfering transmitters cannot use adjacent frequencies
:- assigned(T1, F1), assigned(T2, F2), interferes(T1, T2), F1 = F2 + 1.
:- assigned(T1, F1), assigned(T2, F2), interferes(T1, T2), F2 = F1 + 1.

% --- Objective ---
% Minimize the number of distinct frequencies used
used(F) :- assigned(_, F).
num_used(N) :- N = #count { F : used(F) }.

#minimize { N : num_used(N) }.

% --- Output ---
#show assigned/2.
#show num_used/1.