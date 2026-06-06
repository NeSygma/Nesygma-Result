% --- Declare items and their properties ---
item(1..27).

size(1,9). size(2,8). size(3,3). size(4,9). size(5,7). size(6,4).
size(7,10). size(8,10). size(9,10). size(10,10). size(11,8). size(12,7).
size(13,5). size(14,8). size(15,6). size(16,6). size(17,8). size(18,6).
size(19,6). size(20,7). size(21,7). size(22,6). size(23,7). size(24,5).
size(25,5). size(26,3). size(27,5).

category(1,electronics). category(2,electronics). category(3,electronics).
category(4,liquid). category(5,liquid). category(6,liquid).
category(7,electronics). category(8,standard). category(9,liquid).
category(10,standard). category(11,standard). category(12,standard).
category(13,standard). category(14,standard). category(15,standard).
category(16,standard). category(17,standard). category(18,standard).
category(19,standard). category(20,standard). category(21,standard).
category(22,standard). category(23,standard). category(24,standard).
category(25,standard). category(26,standard). category(27,standard).

fragility(1,fragile). fragility(2,sturdy). fragility(3,sturdy).
fragility(4,fragile). fragility(5,sturdy). fragility(6,sturdy).
fragility(7,fragile). fragility(8,sturdy). fragility(9,fragile).
fragility(10,sturdy). fragility(11,sturdy). fragility(12,sturdy).
fragility(13,sturdy). fragility(14,fragile). fragility(15,fragile).
fragility(16,sturdy). fragility(17,fragile). fragility(18,fragile).
fragility(19,sturdy). fragility(20,sturdy). fragility(21,sturdy).
fragility(22,sturdy). fragility(23,sturdy). fragility(24,fragile).
fragility(25,fragile). fragility(26,sturdy). fragility(27,sturdy).

priority(1,high). priority(2,high). priority(3,high).
priority(4,high). priority(5,high). priority(6,high).
priority(7,high). priority(8,high). priority(9,high).
priority(10,high). priority(11,high). priority(12,high).
priority(13,low). priority(14,low). priority(15,low).
priority(16,low). priority(17,low). priority(18,low).
priority(19,low). priority(20,low). priority(21,low).
priority(22,low). priority(23,low). priority(24,low).
priority(25,low). priority(26,low). priority(27,low).

% --- Declare bins ---
% Assume a maximum of 27 bins (one per item)
bin(1..27).

% Bin capacity
capacity(20).

% Priority bins: bins 1-6
is_priority_bin(B) :- bin(B), B <= 6.

% Incompatibility between categories
incompatible(electronics, liquid).
incompatible(liquid, electronics).

% --- Assignment ---
% Each item assigned to exactly one bin
1 { assigned(I, B) : bin(B) } 1 :- item(I).

% --- Constraints ---

% Capacity: total size per bin <= 20
total_size(B, S) :- bin(B), S = #sum { Sz : assigned(I, B), size(I, Sz) }.
:- bin(B), total_size(B, S), S > 20.

% Incompatibility: electronics and liquids cannot be in the same bin
:- assigned(I1, B), assigned(I2, B), I1 < I2,
   category(I1, C1), category(I2, C2),
   incompatible(C1, C2).

% Fragility limit: <= 2 fragile items per bin
fragile_count(B, C) :- bin(B), C = #count { I : assigned(I, B), fragility(I, fragile) }.
:- bin(B), fragile_count(B, C), C > 2.

% Priority placement: high-priority items only in bins 1-6
:- assigned(I, B), priority(I, high), bin(B), B > 6.

% --- Helper predicates for output ---
has_priority_item(B) :- assigned(I, B), priority(I, high).

% --- Output ---
#show feasible/0.
#show optimal/0.
#show num_bins/1.
#show total_priority_utilization/1.
#show bin_items/3.
#show bin_total_size/2.
#show bin_fragile_count/2.
#show bin_has_priority/1.

% Define feasibility and other output atoms
feasible :- not unsatisfiable.
unsatisfiable :- bin(B), total_size(B, S), S > 20.
unsatisfiable :- assigned(I1, B), assigned(I2, B), I1 < I2,
                 category(I1, C1), category(I2, C2),
                 incompatible(C1, C2).
unsatisfiable :- bin(B), fragile_count(B, C), C > 2.
unsatisfiable :- assigned(I, B), priority(I, high), bin(B), B > 6.

optimal :- not feasible.

num_bins(N) :- N = #count { B : bin(B), total_size(B, _) }.

total_priority_utilization(S) :-
    S = #sum { Sz : bin(B), has_priority_item(B), total_size(B, Sz) }.

bin_items(B, I, Sz) :- assigned(I, B), size(I, Sz).
bin_total_size(B, S) :- bin(B), total_size(B, S).
bin_fragile_count(B, C) :- bin(B), fragile_count(B, C).
bin_has_priority(B) :- bin(B), has_priority_item(B).