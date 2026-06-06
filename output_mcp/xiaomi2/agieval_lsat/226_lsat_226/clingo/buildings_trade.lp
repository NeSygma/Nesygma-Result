% Define companies
company(realprop).
company(southco).
company(trustcorp).

% Define buildings and their classes
building(garza_tower, 1).
building(yates_house, 3).
building(zimmer_house, 3).
building(flores_tower, 1).
building(lynch_building, 2).
building(king_building, 2).
building(meyer_building, 2).
building(ortiz_building, 2).

% Initial ownership
initial_owner(garza_tower, realprop).
initial_owner(yates_house, realprop).
initial_owner(zimmer_house, realprop).
initial_owner(flores_tower, southco).
initial_owner(lynch_building, southco).
initial_owner(king_building, trustcorp).
initial_owner(meyer_building, trustcorp).
initial_owner(ortiz_building, trustcorp).

% Define the five answer options as final ownership states
% Option A
final_owner_a(garza_tower, realprop).
final_owner_a(flores_tower, realprop).
final_owner_a(lynch_building, southco).
final_owner_a(yates_house, southco).
final_owner_a(zimmer_house, southco).
final_owner_a(king_building, trustcorp).
final_owner_a(meyer_building, trustcorp).
final_owner_a(ortiz_building, trustcorp).

% Option B
final_owner_b(garza_tower, realprop).
final_owner_b(king_building, realprop).
final_owner_b(ortiz_building, realprop).
final_owner_b(flores_tower, southco).
final_owner_b(lynch_building, southco).
final_owner_b(meyer_building, trustcorp).
final_owner_b(yates_house, trustcorp).
final_owner_b(zimmer_house, trustcorp).

% Option C
final_owner_c(garza_tower, realprop).
final_owner_c(lynch_building, realprop).
final_owner_c(flores_tower, southco).
final_owner_c(yates_house, southco).
final_owner_c(zimmer_house, southco).
final_owner_c(king_building, trustcorp).
final_owner_c(meyer_building, trustcorp).
final_owner_c(ortiz_building, trustcorp).

% Option D
final_owner_d(garza_tower, realprop).
final_owner_d(meyer_building, realprop).
final_owner_d(yates_house, realprop).
final_owner_d(flores_tower, southco).
final_owner_d(lynch_building, southco).
final_owner_d(king_building, trustcorp).
final_owner_d(ortiz_building, trustcorp).
final_owner_d(zimmer_house, trustcorp).

% Option E
final_owner_e(garza_tower, realprop).
final_owner_e(yates_house, realprop).
final_owner_e(zimmer_house, realprop).
final_owner_e(lynch_building, southco).
final_owner_e(ortiz_building, southco).
final_owner_e(flores_tower, trustcorp).
final_owner_e(king_building, trustcorp).
final_owner_e(meyer_building, trustcorp).

% For each option, determine which buildings changed ownership
changed_a(B) :- building(B, _), initial_owner(B, C1), final_owner_a(B, C2), C1 != C2.
changed_b(B) :- building(B, _), initial_owner(B, C1), final_owner_b(B, C2), C1 != C2.
changed_c(B) :- building(B, _), initial_owner(B, C1), final_owner_c(B, C2), C1 != C2.
changed_d(B) :- building(B, _), initial_owner(B, C1), final_owner_d(B, C2), C1 != C2.
changed_e(B) :- building(B, _), initial_owner(B, C1), final_owner_e(B, C2), C1 != C2.

% Count changed buildings for each option
count_changed_a(N) :- N = #count{B : changed_a(B)}.
count_changed_b(N) :- N = #count{B : changed_b(B)}.
count_changed_c(N) :- N = #count{B : changed_c(B)}.
count_changed_d(N) :- N = #count{B : changed_d(B)}.
count_changed_e(N) :- N = #count{B : changed_e(B)}.

% Trade type 1: 1-for-1 same class (2 buildings change)
% Trade type 2: 1 class1 for 2 class2 (3 buildings change)
% Trade type 3: 1 class2 for 2 class3 (3 buildings change)

% For option A: check if changed buildings form a valid trade
% Trade type 1: exactly 2 buildings swap, same class
valid_trade_a :- count_changed_a(2),
                 changed_a(B1), changed_a(B2), B1 < B2,
                 building(B1, Cl), building(B2, Cl),
                 initial_owner(B1, C1), initial_owner(B2, C2),
                 final_owner_a(B1, C2), final_owner_a(B2, C1),
                 C1 != C2.

% Trade type 2: 1 class1 for 2 class2 (3 buildings change)
valid_trade_a :- count_changed_a(3),
                 changed_a(B1), building(B1, 1),
                 changed_a(B2), building(B2, 2), B1 != B2,
                 changed_a(B3), building(B3, 2), B3 != B1, B3 != B2,
                 initial_owner(B1, C1), initial_owner(B2, C2), initial_owner(B3, C2),
                 final_owner_a(B1, C2), final_owner_a(B2, C1), final_owner_a(B3, C1),
                 C1 != C2.

% Trade type 3: 1 class2 for 2 class3 (3 buildings change)
valid_trade_a :- count_changed_a(3),
                 changed_a(B1), building(B1, 2),
                 changed_a(B2), building(B2, 3), B1 != B2,
                 changed_a(B3), building(B3, 3), B3 != B1, B3 != B2,
                 initial_owner(B1, C1), initial_owner(B2, C2), initial_owner(B3, C2),
                 final_owner_a(B1, C2), final_owner_a(B2, C1), final_owner_a(B3, C1),
                 C1 != C2.

% Same for option B
valid_trade_b :- count_changed_b(2),
                 changed_b(B1), changed_b(B2), B1 < B2,
                 building(B1, Cl), building(B2, Cl),
                 initial_owner(B1, C1), initial_owner(B2, C2),
                 final_owner_b(B1, C2), final_owner_b(B2, C1),
                 C1 != C2.

valid_trade_b :- count_changed_b(3),
                 changed_b(B1), building(B1, 1),
                 changed_b(B2), building(B2, 2), B1 != B2,
                 changed_b(B3), building(B3, 2), B3 != B1, B3 != B2,
                 initial_owner(B1, C1), initial_owner(B2, C2), initial_owner(B3, C2),
                 final_owner_b(B1, C2), final_owner_b(B2, C1), final_owner_b(B3, C1),
                 C1 != C2.

valid_trade_b :- count_changed_b(3),
                 changed_b(B1), building(B1, 2),
                 changed_b(B2), building(B2, 3), B1 != B2,
                 changed_b(B3), building(B3, 3), B3 != B1, B3 != B2,
                 initial_owner(B1, C1), initial_owner(B2, C2), initial_owner(B3, C2),
                 final_owner_b(B1, C2), final_owner_b(B2, C1), final_owner_b(B3, C1),
                 C1 != C2.

% Same for option C
valid_trade_c :- count_changed_c(2),
                 changed_c(B1), changed_c(B2), B1 < B2,
                 building(B1, Cl), building(B2, Cl),
                 initial_owner(B1, C1), initial_owner(B2, C2),
                 final_owner_c(B1, C2), final_owner_c(B2, C1),
                 C1 != C2.

valid_trade_c :- count_changed_c(3),
                 changed_c(B1), building(B1, 1),
                 changed_c(B2), building(B2, 2), B1 != B2,
                 changed_c(B3), building(B3, 2), B3 != B1, B3 != B2,
                 initial_owner(B1, C1), initial_owner(B2, C2), initial_owner(B3, C2),
                 final_owner_c(B1, C2), final_owner_c(B2, C1), final_owner_c(B3, C1),
                 C1 != C2.

valid_trade_c :- count_changed_c(3),
                 changed_c(B1), building(B1, 2),
                 changed_c(B2), building(B2, 3), B1 != B2,
                 changed_c(B3), building(B3, 3), B3 != B1, B3 != B2,
                 initial_owner(B1, C1), initial_owner(B2, C2), initial_owner(B3, C2),
                 final_owner_c(B1, C2), final_owner_c(B2, C1), final_owner_c(B3, C1),
                 C1 != C2.

% Same for option D
valid_trade_d :- count_changed_d(2),
                 changed_d(B1), changed_d(B2), B1 < B2,
                 building(B1, Cl), building(B2, Cl),
                 initial_owner(B1, C1), initial_owner(B2, C2),
                 final_owner_d(B1, C2), final_owner_d(B2, C1),
                 C1 != C2.

valid_trade_d :- count_changed_d(3),
                 changed_d(B1), building(B1, 1),
                 changed_d(B2), building(B2, 2), B1 != B2,
                 changed_d(B3), building(B3, 2), B3 != B1, B3 != B2,
                 initial_owner(B1, C1), initial_owner(B2, C2), initial_owner(B3, C2),
                 final_owner_d(B1, C2), final_owner_d(B2, C1), final_owner_d(B3, C1),
                 C1 != C2.

valid_trade_d :- count_changed_d(3),
                 changed_d(B1), building(B1, 2),
                 changed_d(B2), building(B2, 3), B1 != B2,
                 changed_d(B3), building(B3, 3), B3 != B1, B3 != B2,
                 initial_owner(B1, C1), initial_owner(B2, C2), initial_owner(B3, C2),
                 final_owner_d(B1, C2), final_owner_d(B2, C1), final_owner_d(B3, C1),
                 C1 != C2.

% Same for option E
valid_trade_e :- count_changed_e(2),
                 changed_e(B1), changed_e(B2), B1 < B2,
                 building(B1, Cl), building(B2, Cl),
                 initial_owner(B1, C1), initial_owner(B2, C2),
                 final_owner_e(B1, C2), final_owner_e(B2, C1),
                 C1 != C2.

valid_trade_e :- count_changed_e(3),
                 changed_e(B1), building(B1, 1),
                 changed_e(B2), building(B2, 2), B1 != B2,
                 changed_e(B3), building(B3, 2), B3 != B1, B3 != B2,
                 initial_owner(B1, C1), initial_owner(B2, C2), initial_owner(B3, C2),
                 final_owner_e(B1, C2), final_owner_e(B2, C1), final_owner_e(B3, C1),
                 C1 != C2.

valid_trade_e :- count_changed_e(3),
                 changed_e(B1), building(B1, 2),
                 changed_e(B2), building(B2, 3), B1 != B2,
                 changed_e(B3), building(B3, 3), B3 != B1, B3 != B2,
                 initial_owner(B1, C1), initial_owner(B2, C2), initial_owner(B3, C2),
                 final_owner_e(B1, C2), final_owner_e(B2, C1), final_owner_e(B3, C1),
                 C1 != C2.

% Map correct answer to option
option(a) :- valid_trade_a.
option(b) :- valid_trade_b.
option(c) :- valid_trade_c.
option(d) :- valid_trade_d.
option(e) :- valid_trade_e.

#show option/1.