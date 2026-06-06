% ============================================
% Bin Packing Problem - ASP Translation
% ============================================

% --- Item Data ---
item(1, 9, electronics, fragile, high).
item(2, 8, electronics, sturdy, high).
item(3, 3, electronics, sturdy, high).
item(4, 9, liquid, fragile, high).
item(5, 7, liquid, sturdy, high).
item(6, 4, liquid, sturdy, high).
item(7, 10, electronics, fragile, high).
item(8, 10, standard, sturdy, high).
item(9, 10, liquid, fragile, high).
item(10, 10, standard, sturdy, high).
item(11, 8, standard, sturdy, high).
item(12, 7, standard, sturdy, high).
item(13, 5, standard, sturdy, low).
item(14, 8, standard, fragile, low).
item(15, 6, standard, fragile, low).
item(16, 6, standard, sturdy, low).
item(17, 8, standard, fragile, low).
item(18, 6, standard, fragile, low).
item(19, 6, standard, sturdy, low).
item(20, 7, standard, sturdy, low).
item(21, 7, standard, sturdy, low).
item(22, 6, standard, sturdy, low).
item(23, 7, standard, sturdy, low).
item(24, 5, standard, fragile, low).
item(25, 5, standard, fragile, low).
item(26, 3, standard, sturdy, low).
item(27, 5, standard, sturdy, low).

% --- Constants ---
bin_capacity(20).
fragile_limit(2).
priority_bin(1). priority_bin(2). priority_bin(3).
priority_bin(4). priority_bin(5). priority_bin(6).

% --- Bin Domain ---
% We need enough bins. Upper bound: 27 items, min size 3 => at most 27 bins.
% But realistically, with capacity 20, we need at least ceil(total_size/20) bins.
% Total size = 9+8+3+9+7+4+10+10+10+10+8+7+5+8+6+6+8+6+6+7+7+6+7+5+5+3+5 = 194
% 194/20 = 9.7, so at least 10 bins. Let's use 10-27 bins.
bin(1..27).

% --- Assignment: Each item to exactly one bin ---
1 { assigned(I, B) : bin(B) } 1 :- item(I, _, _, _, _).

% --- Constraint 1: Capacity ---
bin_size(B, S) :- bin(B), S = #sum{Sz, I : assigned(I, B), item(I, Sz, _, _, _)}.
:- bin_size(B, S), bin_capacity(C), S > C.

% --- Constraint 3: Electronics and liquids incompatible ---
:- assigned(I1, B), assigned(I2, B), I1 != I2,
   item(I1, _, electronics, _, _), item(I2, _, liquid, _, _).

% --- Constraint 4: Fragility limit (max 2 fragile per bin) ---
fragile_count(B, N) :- bin(B), N = #count{I : assigned(I, B), item(I, _, _, fragile, _)}.
:- fragile_count(B, N), fragile_limit(L), N > L.

% --- Constraint 5: High-priority items only in bins 1-6 ---
:- assigned(I, B), item(I, _, _, _, high), not priority_bin(B).

% --- Output predicates ---
is_priority_bin(B) :- bin(B), assigned(I, B), item(I, _, _, _, high).
total_priority_utilization(S) :- S = #sum{Sz, I : is_priority_bin(B), assigned(I, B), item(I, Sz, _, _, _)}.

% Count bins used
used_bin(B) :- assigned(_, B).
num_bins(N) :- N = #count{B : used_bin(B)}.

% Feasibility flag
feasible.

% Not optimizing - just finding feasible solution
#show assigned/2.
#show bin_size/2.
#show fragile_count/2.
#show is_priority_bin/1.
#show total_priority_utilization/1.
#show num_bins/1.
#show feasible/0.