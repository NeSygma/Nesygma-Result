% Transmitters
transmitter(t1). transmitter(t2). transmitter(t3). transmitter(t4).
transmitter(t5). transmitter(t6). transmitter(t7). transmitter(t8).
transmitter(t9). transmitter(t10).

% Frequencies with bands and costs
frequency(101, low, 10). frequency(102, low, 12). frequency(103, low, 15).
frequency(201, mid, 20). frequency(202, mid, 22). frequency(203, mid, 25). frequency(204, mid, 28).
frequency(301, high, 40). frequency(302, high, 45).

% Band restrictions for transmitters
% Low band only
band_restriction(t1, low). band_restriction(t2, low).
% Mid band only
band_restriction(t3, mid). band_restriction(t4, mid). band_restriction(t5, mid).
% High band only
band_restriction(t6, high).
% Low or mid bands
band_restriction(t7, low). band_restriction(t7, mid).
band_restriction(t8, low). band_restriction(t8, mid).
% Mid or high bands
band_restriction(t9, mid). band_restriction(t9, high).
band_restriction(t10, mid). band_restriction(t10, high).

% Interference pairs
interference(t1, t2). interference(t1, t7). interference(t2, t8).
interference(t3, t4). interference(t3, t9). interference(t4, t5).
interference(t4, t7). interference(t5, t8). interference(t5, t10).
interference(t6, t9). interference(t6, t10).

% Choice rule: assign exactly one frequency to each transmitter
{ assign(T, F) : frequency(F, B, C) } :- transmitter(T), band_restriction(T, B).

% Band restriction constraint
:- assign(T, F), not frequency(F, B, _), band_restriction(T, B).

% Same-band interference constraint
% If two interfering transmitters are assigned frequencies in the same band,
% their frequencies must differ by more than 1
:- interference(T1, T2), assign(T1, F1), assign(T2, F2),
   frequency(F1, B, _), frequency(F2, B, _),
   F1 < F2, F2 - F1 =< 1.

% Cross-band interference constraint
% If two interfering transmitters are assigned frequencies in different bands,
% they cannot use the same frequency number
:- interference(T1, T2), assign(T1, F1), assign(T2, F2),
   frequency(F1, B1, _), frequency(F2, B2, _),
   B1 != B2, F1 = F2.

% Calculate total cost
assigned_cost(T, C) :- assign(T, F), frequency(F, _, C).
total_cost(C) :- C = #sum { Cost : assigned_cost(_, Cost) }.

% Minimize total cost
#minimize { C : total_cost(C) }.

% Show the assignments and total cost
#show assign/2.
#show total_cost/1.