% Define items
item(1..27).

% Item properties: size, category, fragility, priority
size(1,9).   cat(1,electronics). frag(1,fragile).  pri(1,high).
size(2,8).   cat(2,electronics). frag(2,sturdy).   pri(2,high).
size(3,3).   cat(3,electronics). frag(3,sturdy).   pri(3,high).
size(4,9).   cat(4,liquid).      frag(4,fragile).  pri(4,high).
size(5,7).   cat(5,liquid).      frag(5,sturdy).   pri(5,high).
size(6,4).   cat(6,liquid).      frag(6,sturdy).   pri(6,high).
size(7,10).  cat(7,electronics). frag(7,fragile).  pri(7,high).
size(8,10).  cat(8,standard).    frag(8,sturdy).   pri(8,high).
size(9,10).  cat(9,liquid).      frag(9,fragile).  pri(9,high).
size(10,10). cat(10,standard).   frag(10,sturdy).  pri(10,high).
size(11,8).  cat(11,standard).   frag(11,sturdy).  pri(11,high).
size(12,7).  cat(12,standard).   frag(12,sturdy).  pri(12,high).
size(13,5).  cat(13,standard).   frag(13,sturdy).  pri(13,low).
size(14,8).  cat(14,standard).   frag(14,fragile). pri(14,low).
size(15,6).  cat(15,standard).   frag(15,fragile). pri(15,low).
size(16,6).  cat(16,standard).   frag(16,sturdy).  pri(16,low).
size(17,8).  cat(17,standard).   frag(17,fragile). pri(17,low).
size(18,6).  cat(18,standard).   frag(18,fragile). pri(18,low).
size(19,6).  cat(19,standard).   frag(19,sturdy).  pri(19,low).
size(20,7).  cat(20,standard).   frag(20,sturdy).  pri(20,low).
size(21,7).  cat(21,standard).   frag(21,sturdy).  pri(21,low).
size(22,6).  cat(22,standard).   frag(22,sturdy).  pri(22,low).
size(23,7).  cat(23,standard).   frag(23,sturdy).  pri(23,low).
size(24,5).  cat(24,standard).   frag(24,fragile). pri(24,low).
size(25,5).  cat(25,standard).   frag(25,fragile). pri(25,low).
size(26,3).  cat(26,standard).   frag(26,sturdy).  pri(26,low).
size(27,5).  cat(27,standard).   frag(27,sturdy).  pri(27,low).

% Define bins (enough to accommodate all items - total size ~185, capacity 20 each)
bin(1..11).

% Priority bins: bins 1-6
priority_bin(1..6).

% Constraint 2: Each item assigned to exactly one bin
1 { assigned(I, B) : bin(B) } 1 :- item(I).

% Constraint 1: Capacity - total size in each bin <= 20
:- bin(B), #sum { S, I : assigned(I, B), size(I, S) } > 20.

% Constraint 3: Incompatibility - electronics and liquids cannot be in same bin
:- bin(B), assigned(I1, B), cat(I1, electronics), assigned(I2, B), cat(I2, liquid).

% Constraint 4: Fragility limit - at most 2 fragile items per bin
:- bin(B), #count { I : assigned(I, B), frag(I, fragile) } > 2.

% Constraint 5: Priority placement - high-priority items only in bins 1-6
:- assigned(I, B), pri(I, high), not priority_bin(B).

% Compute derived facts for output
used_bin(B) :- assigned(_, B).
num_bins(N) :- N = #count { B : used_bin(B) }.

bin_size(B, S) :- bin(B), S = #sum { Sz, I : assigned(I, B), size(I, Sz) }.
bin_fragile(B, C) :- bin(B), C = #count { I : assigned(I, B), frag(I, fragile) }.
bin_has_high(B) :- assigned(I, B), pri(I, high).
total_priority_utilization(U) :- U = #sum { Sz, B : bin_has_high(B), bin_size(B, Sz) }.

feasible :- num_bins(N), N >= 1.

#show assigned/2.
#show num_bins/1.
#show bin_size/2.
#show bin_fragile/2.
#show bin_has_high/1.
#show total_priority_utilization/1.
#show feasible/0.