% --- Domain Definitions ---
transmitter(t1;t2;t3;t4;t5;t6;t7;t8;t9;t10).

% Frequencies with bands and costs
% freq(ID, Band, Cost)
freq(101, low, 10).
freq(102, low, 12).
freq(103, low, 15).
freq(201, mid, 20).
freq(202, mid, 22).
freq(203, mid, 25).
freq(204, mid, 28).
freq(301, high, 40).
freq(302, high, 45).

% Band definitions
band(low;mid;high).

% Frequency numbers (for cross-band conflict check)
freq_num(101;102;103;201;202;203;204;301;302).

% --- Transmitter Band Restrictions ---
% Low band only: t1, t2
allowed(t1, low).
allowed(t2, low).

% Mid band only: t3, t4, t5
allowed(t3, mid).
allowed(t4, mid).
allowed(t5, mid).

% High band only: t6
allowed(t6, high).

% Low or mid bands: t7, t8
allowed(t7, low).
allowed(t7, mid).
allowed(t8, low).
allowed(t8, mid).

% Mid or high bands: t9, t10
allowed(t9, mid).
allowed(t9, high).
allowed(t10, mid).
allowed(t10, high).

% --- Interference Pairs ---
interfere(t1,t2). interfere(t1,t7). interfere(t2,t8).
interfere(t3,t4). interfere(t3,t9). interfere(t4,t5).
interfere(t4,t7). interfere(t5,t8). interfere(t5,t10).
interfere(t6,t9). interfere(t6,t10).

% Make interference symmetric
interfere(X,Y) :- interfere(Y,X).

% --- Frequency Band Mapping ---
freq_band(F, B) :- freq(F, B, _).

% --- Assignment: Each transmitter gets exactly one frequency ---
% Choice rule: assign a frequency to a transmitter if allowed
{ assign(T, F) : freq(F, B, _), allowed(T, B) } 1 :- transmitter(T).

% Constraint: Every transmitter must have exactly one assignment
:- transmitter(T), not assign(T, _).

% --- Constraint 2: Same-Band Interference ---
% If two interfering transmitters use frequencies from the same band,
% their frequencies must differ by more than 1.
:- interfere(T1, T2), assign(T1, F1), assign(T2, F2),
   freq_band(F1, B), freq_band(F2, B),
   |F1 - F2| <= 1.

% --- Constraint 3: Cross-Band Interference ---
% If two interfering transmitters use frequencies from different bands,
% they cannot use the same frequency number.
:- interfere(T1, T2), assign(T1, F1), assign(T2, F2),
   freq_band(F1, B1), freq_band(F2, B2), B1 != B2,
   F1 = F2.

% --- Objective: Minimize total cost ---
% Compute cost of each assignment
assign_cost(T, F, C) :- assign(T, F), freq(F, _, C).

% Total cost
total_cost(C) :- C = #sum { Cst, T : assign_cost(T, _, Cst) }.

% Minimize total cost
#minimize { Cst, T, F : assign(T, F), freq(F, _, Cst) }.

% --- Show results ---
#show assign/2.
#show total_cost/1.