% Domain facts
transmitter(a). transmitter(b). transmitter(c). transmitter(d). transmitter(e). transmitter(f).
freq(1). freq(2). freq(3). freq(4). freq(5).

% Interference graph (bidirectional)
interferes(a,b). interferes(b,a).
interferes(a,c). interferes(c,a).
interferes(b,d). interferes(d,b).
interferes(b,e). interferes(e,b).
interferes(c,d). interferes(d,c).
interferes(c,f). interferes(f,c).
interferes(d,e). interferes(e,d).
interferes(e,f). interferes(f,e).

% Assignment: each transmitter gets exactly one frequency
{assign(T,F) : freq(F)} 1 :- transmitter(T).

% Used frequencies
used(F) :- assign(_,F).

% Frequency used count
freq_used_count(N) :- N = #count{F : used(F)}.

% Constraints: no same frequency for interfering transmitters
:- assign(T1,F), assign(T2,F), interferes(T1,T2).

% Constraints: no adjacent frequencies for interfering transmitters
:- assign(T1,F1), assign(T2,F2), interferes(T1,T2), F1 = F2+1.
:- assign(T1,F1), assign(T2,F2), interferes(T1,T2), F1 = F2-1.

% Objective: minimize number of distinct frequencies used
#minimize {1@1, used(F) : used(F)}.

% Secondary objective: minimize sum of frequencies assigned (lexicographic tie-breaker)
#minimize {F@2, assign(T,F) : assign(T,F)}.

% Show assignments and frequency count
#show assign/2.
#show freq_used_count/1.