% --- Data ---
transmitter(t1;t2;t3;t4;t5;t6;t7;t8;t9;t10).

% Frequencies
freq(101;102;103;201;202;203;204;301;302).

% Cost of each frequency
cost(101,10). cost(102,12). cost(103,15).
cost(201,20). cost(202,22). cost(203,25). cost(204,28).
cost(301,40). cost(302,45).

% Band membership
band(101,low). band(102,low). band(103,low).
band(201,mid). band(202,mid). band(203,mid). band(204,mid).
band(301,high). band(302,high).

% Allowed bands per transmitter
allowed_band(t1,low). allowed_band(t2,low).
allowed_band(t3,mid). allowed_band(t4,mid). allowed_band(t5,mid).
allowed_band(t6,high).
allowed_band(t7,low). allowed_band(t7,mid).
allowed_band(t8,low). allowed_band(t8,mid).
allowed_band(t9,mid). allowed_band(t9,high).
allowed_band(t10,mid). allowed_band(t10,high).

% Interference pairs (undirected - symmetric)
interfere(t1,t2). interfere(t1,t7). interfere(t2,t8).
interfere(t3,t4). interfere(t3,t9). interfere(t4,t5).
interfere(t4,t7). interfere(t5,t8). interfere(t5,t10).
interfere(t6,t9). interfere(t6,t10).

% --- Derived predicates ---

% A frequency is allowed for a transmitter if it belongs to an allowed band
allowed_freq(T,F) :- allowed_band(T,B), band(F,B).

% --- Assignment: each transmitter gets exactly one allowed frequency ---
1 { assignment(T,F) : allowed_freq(T,F) } 1 :- transmitter(T).

% --- Constraint 2: Same-band interference: frequencies must differ by more than 1 ---
% i.e., |F1 - F2| > 1 for interfering transmitters in the same band
:- interfere(T1,T2), assignment(T1,F1), assignment(T2,F2), 
   band(F1,B), band(F2,B),
   F1 = F2+1.
:- interfere(T1,T2), assignment(T1,F1), assignment(T2,F2), 
   band(F1,B), band(F2,B),
   F2 = F1+1.
:- interfere(T1,T2), assignment(T1,F), assignment(T2,F),
   band(F,B1), band(F,B2).

% --- Constraint 3: Cross-band interference: cannot use the same frequency ---
% (Since all frequencies are unique values across bands, this is automatically
%  satisfied for cross-band pairs, but we encode it for completeness.)
:- interfere(T1,T2), assignment(T1,F), assignment(T2,F).

% --- Objective: Minimize total licensing cost ---
#minimize { C : assignment(T,F), cost(F,C) }.

% --- Output ---
#show assignment/2.
total_cost(C) :- C = #sum { Cost,F,T : assignment(T,F), cost(F,Cost) }.
#show total_cost/1.