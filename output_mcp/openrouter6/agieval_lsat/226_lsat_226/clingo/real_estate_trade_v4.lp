% Real Estate Trade Problem - Version 4

% Companies
company(realprop). company(southco). company(trustcorp).

% Buildings
building(garza_tower). building(yates_house). building(zimmer_house).
building(flores_tower). building(lynch_building).
building(king_building). building(meyer_building). building(ortiz_building).

% Classes
class(garza_tower, 1). class(yates_house, 3). class(zimmer_house, 3).
class(flores_tower, 1). class(lynch_building, 2).
class(king_building, 2). class(meyer_building, 2). class(ortiz_building, 2).

% Initial ownership
owned_initial(realprop, garza_tower).
owned_initial(realprop, yates_house).
owned_initial(realprop, zimmer_house).
owned_initial(southco, flores_tower).
owned_initial(southco, lynch_building).
owned_initial(trustcorp, king_building).
owned_initial(trustcorp, meyer_building).
owned_initial(trustcorp, ortiz_building).

% Answer choices as facts
choice(a). choice(b). choice(c). choice(d). choice(e).

% Define final ownership for each choice
% Choice A
final(realprop, garza_tower) :- choice(a).
final(realprop, flores_tower) :- choice(a).
final(southco, lynch_building) :- choice(a).
final(southco, yates_house) :- choice(a).
final(southco, zimmer_house) :- choice(a).
final(trustcorp, king_building) :- choice(a).
final(trustcorp, meyer_building) :- choice(a).
final(trustcorp, ortiz_building) :- choice(a).

% Choice B
final(realprop, garza_tower) :- choice(b).
final(realprop, king_building) :- choice(b).
final(realprop, ortiz_building) :- choice(b).
final(southco, flores_tower) :- choice(b).
final(southco, lynch_building) :- choice(b).
final(trustcorp, meyer_building) :- choice(b).
final(trustcorp, yates_house) :- choice(b).
final(trustcorp, zimmer_house) :- choice(b).

% Choice C
final(realprop, garza_tower) :- choice(c).
final(realprop, lynch_building) :- choice(c).
final(southco, flores_tower) :- choice(c).
final(southco, yates_house) :- choice(c).
final(southco, zimmer_house) :- choice(c).
final(trustcorp, king_building) :- choice(c).
final(trustcorp, meyer_building) :- choice(c).
final(trustcorp, ortiz_building) :- choice(c).

% Choice D
final(realprop, garza_tower) :- choice(d).
final(realprop, meyer_building) :- choice(d).
final(realprop, yates_house) :- choice(d).
final(southco, flores_tower) :- choice(d).
final(southco, lynch_building) :- choice(d).
final(trustcorp, king_building) :- choice(d).
final(trustcorp, ortiz_building) :- choice(d).
final(trustcorp, zimmer_house) :- choice(d).

% Choice E
final(realprop, garza_tower) :- choice(e).
final(realprop, yates_house) :- choice(e).
final(realprop, zimmer_house) :- choice(e).
final(southco, lynch_building) :- choice(e).
final(southco, ortiz_building) :- choice(e).
final(trustcorp, flores_tower) :- choice(e).
final(trustcorp, king_building) :- choice(e).
final(trustcorp, meyer_building) :- choice(e).

% Ensure each building is owned by exactly one company in final for each choice
1 { final(C, B) : company(C) } 1 :- building(B), choice(a).
1 { final(C, B) : company(C) } 1 :- building(B), choice(b).
1 { final(C, B) : company(C) } 1 :- building(B), choice(c).
1 { final(C, B) : company(C) } 1 :- building(B), choice(d).
1 { final(C, B) : company(C) } 1 :- building(B), choice(e).

% For each choice, determine which buildings changed hands
% A building changed hands if its owner in final differs from initial
changed(B, C1, C2) :- building(B), company(C1), company(C2), C1 != C2,
                       owned_initial(C1, B), final(C2, B).

% Count changed buildings per company for each choice
changed_from(C, N) :- N = #count { B : changed(B, C, _) }, company(C).
changed_to(C, N) :- N = #count { B : changed(B, _, C) }, company(C).

% For a valid trade, exactly two companies should be involved in changes
% And the pattern of changes should match one of the three trade types

% Trade type 1: One building from C1 to C2, one building from C2 to C1, same class
valid_trade_type1(C1, C2) :- changed_from(C1, 1), changed_to(C1, 1),
                              changed_from(C2, 1), changed_to(C2, 1),
                              changed(B1, C1, C2), changed(B2, C2, C1),
                              class(B1, CL), class(B2, CL).

% Trade type 2: One class 1 from C1 to C2, two class 2 from C2 to C1
valid_trade_type2(C1, C2) :- changed_from(C1, 1), changed_to(C1, 2),
                              changed_from(C2, 2), changed_to(C2, 1),
                              changed(B1, C1, C2), class(B1, 1),
                              changed(B2, C2, C1), class(B2, 2),
                              changed(B3, C2, C1), class(B3, 2), B2 != B3.

% Trade type 3: One class 2 from C1 to C2, two class 3 from C2 to C1
valid_trade_type3(C1, C2) :- changed_from(C1, 1), changed_to(C1, 2),
                              changed_from(C2, 2), changed_to(C2, 1),
                              changed(B1, C1, C2), class(B1, 2),
                              changed(B2, C2, C1), class(B2, 3),
                              changed(B3, C2, C1), class(B3, 3), B2 != B3.

% A choice is feasible if there exists a valid trade
feasible(choice_a) :- choice(a), valid_trade_type1(_, _).
feasible(choice_a) :- choice(a), valid_trade_type2(_, _).
feasible(choice_a) :- choice(a), valid_trade_type3(_, _).

feasible(choice_b) :- choice(b), valid_trade_type1(_, _).
feasible(choice_b) :- choice(b), valid_trade_type2(_, _).
feasible(choice_b) :- choice(b), valid_trade_type3(_, _).

feasible(choice_c) :- choice(c), valid_trade_type1(_, _).
feasible(choice_c) :- choice(c), valid_trade_type2(_, _).
feasible(choice_c) :- choice(c), valid_trade_type3(_, _).

feasible(choice_d) :- choice(d), valid_trade_type1(_, _).
feasible(choice_d) :- choice(d), valid_trade_type2(_, _).
feasible(choice_d) :- choice(d), valid_trade_type3(_, _).

feasible(choice_e) :- choice(e), valid_trade_type1(_, _).
feasible(choice_e) :- choice(e), valid_trade_type2(_, _).
feasible(choice_e) :- choice(e), valid_trade_type3(_, _).

% Map the correct answer to option/1
option(a) :- feasible(choice_a).
option(b) :- feasible(choice_b).
option(c) :- feasible(choice_c).
option(d) :- feasible(choice_d).
option(e) :- feasible(choice_e).

#show option/1.