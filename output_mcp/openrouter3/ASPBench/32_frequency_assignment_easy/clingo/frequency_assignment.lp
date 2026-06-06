% Frequency Assignment Problem
% Minimize number of distinct frequencies used

% Domain declarations
transmitter(a). transmitter(b). transmitter(c). transmitter(d). transmitter(e). transmitter(f).
frequency(1). frequency(2). frequency(3). frequency(4). frequency(5).

% Interference relationships (symmetric)
interferes(a, b). interferes(b, a).
interferes(a, c). interferes(c, a).
interferes(b, d). interferes(d, b).
interferes(b, e). interferes(e, b).
interferes(c, d). interferes(d, c).
interferes(c, f). interferes(f, c).
interferes(d, e). interferes(e, d).
interferes(e, f). interferes(f, e).

% Choice rule: Each transmitter gets exactly one frequency
1 { assign(T, F) : frequency(F) } 1 :- transmitter(T).

% Constraint: Interfering transmitters cannot use the same frequency
:- assign(T1, F), assign(T2, F), interferes(T1, T2), T1 != T2.

% Constraint: Interfering transmitters cannot use adjacent frequencies
% Adjacent means |F1 - F2| = 1
:- assign(T1, F1), assign(T2, F2), interferes(T1, T2), T1 != T2, |F1 - F2| = 1.

% Define which frequencies are used
used(F) :- assign(_, F).

% Count distinct frequencies used
freq_count(N) :- N = #count { F : used(F) }.

% Objective: Minimize the number of distinct frequencies used
#minimize { 1, F : used(F) }.

% Show the assignments and frequency count
#show assign/2.
#show freq_count/1.