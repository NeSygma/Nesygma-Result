% --- Data ---
transmitter(t1; t2; t3; t4; t5; t6; t7; t8; t9; t10).

frequency(101, low, 10).
frequency(102, low, 12).
frequency(103, low, 15).
frequency(201, mid, 20).
frequency(202, mid, 22).
frequency(203, mid, 25).
frequency(204, mid, 28).
frequency(301, high, 40).
frequency(302, high, 45).

allowed(t1, low).
allowed(t2, low).
allowed(t3, mid).
allowed(t4, mid).
allowed(t5, mid).
allowed(t6, high).
allowed(t7, low). allowed(t7, mid).
allowed(t8, low). allowed(t8, mid).
allowed(t9, mid). allowed(t9, high).
allowed(t10, mid). allowed(t10, high).

interference(t1, t2).
interference(t1, t7).
interference(t2, t8).
interference(t3, t4).
interference(t3, t9).
interference(t4, t5).
interference(t4, t7).
interference(t5, t8).
interference(t5, t10).
interference(t6, t9).
interference(t6, t10).

% --- Logic ---
% Symmetric interference
interference_sym(T1, T2) :- interference(T1, T2).
interference_sym(T2, T1) :- interference(T1, T2).

% Assignment
{ assign(T, F) : frequency(F, B, C), allowed(T, B) } = 1 :- transmitter(T).

% Same-band interference: |F1 - F2| > 1
:- interference_sym(T1, T2), assign(T1, F1), assign(T2, F2), 
   frequency(F1, B, _), frequency(F2, B, _), 
   F1 != F2, |F1 - F2| <= 1.

% Cross-band interference: F1 != F2 (Trivially satisfied as all F are distinct)
:- interference_sym(T1, T2), assign(T1, F1), assign(T2, F2), 
   frequency(F1, B1, _), frequency(F2, B2, _), B1 != B2, F1 == F2.

% Objective: Minimize total cost
total_cost(S) :- S = #sum { C, T : assign(T, F), frequency(F, _, C) }.
#minimize { S : total_cost(S) }.

#show assign/2.
#show total_cost/1.