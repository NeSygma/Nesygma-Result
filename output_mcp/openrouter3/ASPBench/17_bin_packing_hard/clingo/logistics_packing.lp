% Logistics Packing Problem - Clingo ASP Model

% ===== ITEM DATA =====
% item(ID, Size, Category, Fragility, Priority)
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

% ===== BIN DOMAIN =====
% We need enough bins for all items. Let's use bins 1-10 (can be extended)
bin(1). bin(2). bin(3). bin(4). bin(5). bin(6). bin(7). bin(8). bin(9). bin(10).

% Priority bins are 1-6
priority_bin(Bin) :- bin(Bin), Bin >= 1, Bin <= 6.

% ===== ASSIGNMENT =====
% Each item must be assigned to exactly one bin
1 { assigned(Item, Bin) : bin(Bin) } 1 :- item(Item, _, _, _, _).

% ===== CAPACITY CONSTRAINT =====
% Calculate total size per bin
bin_size(Bin, TotalSize) :- bin(Bin), 
    TotalSize = #sum { Size, Item : assigned(Item, Bin), item(Item, Size, _, _, _) }.

% Capacity must not exceed 20
:- bin_size(Bin, Size), Size > 20.

% ===== INCOMPATIBILITY CONSTRAINT =====
% Electronics and liquids cannot be in the same bin
has_electronics(Bin) :- assigned(Item, Bin), item(Item, _, electronics, _, _).
has_liquid(Bin) :- assigned(Item, Bin), item(Item, _, liquid, _, _).
:- has_electronics(Bin), has_liquid(Bin).

% ===== FRAGILITY LIMIT =====
% Count fragile items per bin
fragile_count(Bin, Count) :- bin(Bin),
    Count = #count { Item : assigned(Item, Bin), item(Item, _, _, fragile, _) }.

% No more than 2 fragile items per bin
:- fragile_count(Bin, Count), Count > 2.

% ===== PRIORITY PLACEMENT =====
% High-priority items only in bins 1-6
:- assigned(Item, Bin), item(Item, _, _, _, high), not priority_bin(Bin).

% Mark bins that contain high-priority items
has_priority(Bin) :- assigned(Item, Bin), item(Item, _, _, _, high).

% ===== DERIVED METRICS =====
% Number of bins used (bins with at least one item)
num_bins(N) :- N = #count { Bin : assigned(_, Bin) }.

% Total priority utilization (sum of sizes in bins with high-priority items)
total_priority_utilization(S) :- S = #sum { Size, Bin : 
    assigned(Item, Bin), item(Item, Size, _, _, high), has_priority(Bin) }.

% ===== FEASIBILITY =====
% Solution is feasible if all constraints are satisfied
feasible :- not impossible.
impossible :- bin_size(Bin, Size), Size > 20.
impossible :- has_electronics(Bin), has_liquid(Bin).
impossible :- fragile_count(Bin, Count), Count > 2.
impossible :- assigned(Item, Bin), item(Item, _, _, _, high), not priority_bin(Bin).

% ===== OUTPUT =====
#show feasible/0.
#show num_bins/1.
#show total_priority_utilization/1.
#show assigned/2.
#show bin_size/2.
#show fragile_count/2.
#show has_priority/1.