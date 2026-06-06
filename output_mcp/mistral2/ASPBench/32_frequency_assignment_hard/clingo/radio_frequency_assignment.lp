% --- DOMAINS ---
transmitter(t1; t2; t3; t4; t5; t6; t7; t8; t9; t10).
frequency(101; 102; 103; 201; 202; 203; 204; 301; 302).

% Frequency properties: band and cost
band(101, low).  cost(101, 10).
band(102, low).  cost(102, 12).
band(103, low).  cost(103, 15).
band(201, mid).  cost(201, 20).
band(202, mid).  cost(202, 22).
band(203, mid).  cost(203, 25).
band(204, mid).  cost(204, 28).
band(301, high). cost(301, 40).
band(302, high). cost(302, 45).

% Transmitter band restrictions
allowed(t1, low). allowed(t2, low).
allowed(t3, mid). allowed(t4, mid). allowed(t5, mid).
allowed(t6, high).
allowed(t7, low). allowed(t7, mid).
allowed(t8, low). allowed(t8, mid).
allowed(t9, mid). allowed(t9, high).
allowed(t10, mid). allowed(t10, high).

% Interference pairs
interferes(t1, t2). interferes(t1, t7).
interferes(t2, t8). interferes(t3, t4).
interferes(t3, t9). interferes(t4, t5).
interferes(t4, t7). interferes(t5, t8).
interferes(t5, t10). interferes(t6, t9).
interferes(t6, t10).

% --- CHOICE RULE ---
% Assign exactly one frequency to each transmitter
1 { assigned(T, F) : frequency(F) } 1 :- transmitter(T).

% --- BAND RESTRICTION CONSTRAINT ---
% Ensure assigned frequency is allowed for the transmitter
:- assigned(T, F), not allowed(T, B), band(F, B).

% --- INTERFERENCE CONSTRAINTS ---
% Same-band interference: frequencies must differ by more than 1
:- assigned(T1, F1), assigned(T2, F2), interferes(T1, T2),
   band(F1, B), band(F2, B), F1 != F2, abs(F1 - F2) =< 1.

% Cross-band interference: cannot use the same frequency number
:- assigned(T1, F), assigned(T2, F), interferes(T1, T2).

% --- OBJECTIVE: MINIMIZE TOTAL COST ---
% Calculate total cost
total_cost(C) :- C = #sum { Cost : assigned(T, F), cost(F, Cost) }.

% Minimize the total cost
#minimize { C : total_cost(C) }.

% --- SHOW ---
#show assigned/2.
#show total_cost/1.