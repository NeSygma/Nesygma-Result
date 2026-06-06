% ==================== DOMAIN DEFINITIONS ====================

% Transmitters
transmitter(t1). transmitter(t2). transmitter(t3). transmitter(t4). transmitter(t5).
transmitter(t6). transmitter(t7). transmitter(t8). transmitter(t9). transmitter(t10).

% Frequencies
frequency(101). frequency(102). frequency(103).
frequency(201). frequency(202). frequency(203). frequency(204).
frequency(301). frequency(302).

% Bands
band(low). band(mid). band(high).

% Frequency to band mapping
band(101, low). band(102, low). band(103, low).
band(201, mid). band(202, mid). band(203, mid). band(204, mid).
band(301, high). band(302, high).

% Frequency costs
cost(101, 10). cost(102, 12). cost(103, 15).
cost(201, 20). cost(202, 22). cost(203, 25). cost(204, 28).
cost(301, 40). cost(302, 45).

% ==================== BAND RESTRICTIONS ====================

% Low band only: t1, t2
allowed_band(t1, low). allowed_band(t2, low).

% Mid band only: t3, t4, t5
allowed_band(t3, mid). allowed_band(t4, mid). allowed_band(t5, mid).

% High band only: t6
allowed_band(t6, high).

% Low or mid bands: t7, t8
allowed_band(t7, low). allowed_band(t7, mid).
allowed_band(t8, low). allowed_band(t8, mid).

% Mid or high bands: t9, t10
allowed_band(t9, mid). allowed_band(t9, high).
allowed_band(t10, mid). allowed_band(t10, high).

% ==================== INTERFERENCE PAIRS ====================

interferes(t1, t2). interferes(t1, t7). interferes(t2, t8).
interferes(t3, t4). interferes(t3, t9). interferes(t4, t5).
interferes(t4, t7). interferes(t5, t8). interferes(t5, t10).
interferes(t6, t9). interferes(t6, t10).

% Make interferes symmetric
interferes(T2, T1) :- interferes(T1, T2).

% ==================== ASSIGNMENT (CHOICE) ====================

% Each transmitter gets exactly one frequency from its allowed bands
1 { assigned(T, F) : frequency(F), band(F, B), allowed_band(T, B) } 1 :- transmitter(T).

% ==================== INTERFERENCE CONSTRAINTS ====================

% Same-band interference: if two interfering transmitters use same band,
% their frequencies must differ by more than 1
:- interferes(T1, T2), assigned(T1, F1), assigned(T2, F2),
   band(F1, B), band(F2, B),
   |F1 - F2| <= 1.

% Cross-band interference: if two interfering transmitters use different bands,
% they cannot use the same frequency number
:- interferes(T1, T2), assigned(T1, F1), assigned(T2, F2),
   band(F1, B1), band(F2, B2), B1 != B2,
   F1 = F2.

% ==================== OBJECTIVE ====================

% Compute total cost
total_cost(S) :- S = #sum { C, T : assigned(T, F), cost(F, C) }.

% Minimize total cost
#minimize { C, T : assigned(T, F), cost(F, C) }.

% ==================== OUTPUT ====================

#show assigned/2.
#show total_cost/1.