% Frequency assignment problem

% Domains
transmitter(a). transmitter(b). transmitter(c). transmitter(d). transmitter(e). transmitter(f).
frequency(1). frequency(2). frequency(3). frequency(4). frequency(5).

% Interference graph (undirected, encode both directions for simplicity)
interferes(a,b). interferes(b,a).
interferes(a,c). interferes(c,a).
interferes(b,d). interferes(d,b).
interferes(b,e). interferes(e,b).
interferes(c,d). interferes(d,c).
interferes(c,f). interferes(f,c).
interferes(d,e). interferes(e,d).
interferes(e,f). interferes(f,e).

% Each transmitter assigned exactly one frequency
1 { assignment(T, F) : frequency(F) } 1 :- transmitter(T).

% Interfering transmitters cannot use same frequency
:- assignment(T1, F), assignment(T2, F), interferes(T1, T2).

% Interfering transmitters cannot use adjacent frequencies (difference = 1)
:- assignment(T1, F1), assignment(T2, F2), interferes(T1, T2), F1 - F2 = 1.
:- assignment(T1, F1), assignment(T2, F2), interferes(T1, T2), F2 - F1 = 1.

% Compute used frequencies
used(F) :- assignment(_, F).

% Count distinct frequencies used
distinct_count(N) :- N = #count{ F : used(F) }.

% Minimize number of distinct frequencies used
#minimize { N : distinct_count(N) }.

% Output
frequencies_used(N) :- distinct_count(N).
solution_exists.

#show assignment/2.
#show frequencies_used/1.
#show solution_exists.