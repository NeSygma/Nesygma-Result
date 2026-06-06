% Radio Frequency Assignment Problem

% --- Domain Declarations ---
transmitter(t1). transmitter(t2). transmitter(t3). transmitter(t4). transmitter(t5).
transmitter(t6). transmitter(t7). transmitter(t8). transmitter(t9). transmitter(t10).

% Frequencies: frequency(band, number, cost)
frequency("low", 101, 10). frequency("low", 102, 12). frequency("low", 103, 15).
frequency("mid", 201, 20). frequency("mid", 202, 22). frequency("mid", 203, 25). frequency("mid", 204, 28).
frequency("high", 301, 40). frequency("high", 302, 45).

% Band restrictions for transmitters
allowed_band(t1, "low"). allowed_band(t2, "low").
allowed_band(t3, "mid"). allowed_band(t4, "mid"). allowed_band(t5, "mid").
allowed_band(t6, "high").
allowed_band(t7, "low"). allowed_band(t7, "mid").
allowed_band(t8, "low"). allowed_band(t8, "mid").
allowed_band(t9, "mid"). allowed_band(t9, "high").
allowed_band(t10, "mid"). allowed_band(t10, "high").

% Interference pairs (undirected - store both directions for convenience)
interference(t1, t2). interference(t2, t1).
interference(t1, t7). interference(t7, t1).
interference(t2, t8). interference(t8, t2).
interference(t3, t4). interference(t4, t3).
interference(t3, t9). interference(t9, t3).
interference(t4, t5). interference(t5, t4).
interference(t4, t7). interference(t7, t4).
interference(t5, t8). interference(t8, t5).
interference(t5, t10). interference(t10, t5).
interference(t6, t9). interference(t9, t6).
interference(t6, t10). interference(t10, t6).

% --- Assignment Choice Rule ---
% Each transmitter gets exactly one frequency from its allowed bands
1 { assignment(t, f) : frequency(B, f, _), allowed_band(t, B) } 1 :- transmitter(t).

% --- Constraints ---

% 1. Band restriction is already enforced by choice rule above

% 2. Same-band interference: if interfering transmitters use same band, frequencies must differ by > 1
:- interference(t1, t2),
   assignment(t1, f1), assignment(t2, f2),
   frequency(B1, f1, _), frequency(B2, f2, _),
   B1 == B2,  % same band
   |f1 - f2| <= 1.  % difference <= 1

% 3. Cross-band interference: if interfering transmitters use different bands, they cannot use same frequency number
:- interference(t1, t2),
   assignment(t1, f1), assignment(t2, f2),
   frequency(B1, f1, _), frequency(B2, f2, _),
   B1 != B2,  % different bands
   f1 == f2.  % same frequency number (should never happen with given frequencies, but include for completeness)

% 4. Complete assignment is already enforced by choice rule (exactly 1 per transmitter)

% --- Objective: Minimize total cost ---
total_cost(C) :- C = #sum { Cost, t : assignment(t, f), frequency(_, f, Cost) }.

% --- Show assignments and total cost ---
#show assignment/2.
#show total_cost/1.