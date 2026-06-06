% Real Estate Trade Problem - Version 3

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

% Select two companies for the trade
{ selected(C) } 2 :- company(C).
:- #count { C : selected(C) } != 2.

% Order the selected companies
selected_ordered(C1, C2) :- selected(C1), selected(C2), C1 < C2.

% Buildings transferred from C1 to C2
{ transfer(C1, C2, B) : building(B) } :- selected_ordered(C1, C2).
% Buildings transferred from C2 to C1
{ transfer(C2, C1, B) : building(B) } :- selected_ordered(C1, C2).

% Ensure each building is transferred at most once
:- transfer(_, _, B1), transfer(_, _, B2), B1 = B2.

% Count transfers per direction
count_c1_to_c2(N) :- N = #count { B : transfer(C1, C2, B) }.
count_c2_to_c1(N) :- N = #count { B : transfer(C2, C1, B) }.

% Trade type 1: one transfer each direction, same class
trade_type(1) :- count_c1_to_c2(1), count_c2_to_c1(1), transfer(C1, C2, B1), transfer(C2, C1, B2), class(B1, CL), class(B2, CL).

% Trade type 2: one transfer from C1 to C2 (class 1), two transfers from C2 to C1 (class 2)
trade_type(2) :- count_c1_to_c2(1), count_c2_to_c1(2), transfer(C1, C2, B1), class(B1, 1), transfer(C2, C1, B2), class(B2, 2), transfer(C2, C1, B3), class(B3, 2), B2 != B3.

% Trade type 3: one transfer from C1 to C2 (class 2), two transfers from C2 to C1 (class 3)
trade_type(3) :- count_c1_to_c2(1), count_c2_to_c1(2), transfer(C1, C2, B1), class(B1, 2), transfer(C2, C1, B2), class(B2, 3), transfer(C2, C1, B3), class(B3, 3), B2 != B3.

% Derived final ownership from transfers
transferred_from(C, B) :- transfer(C, _, B).
transferred_to(C, B) :- transfer(_, C, B).

derived_final(C, B) :- owned_initial(C, B), not transferred_from(C, B).
derived_final(C, B) :- transferred_to(C, B).

% Ensure each building has exactly one owner in derived_final
1 { derived_final(C, B) : company(C) } 1 :- building(B).

% Match derived_final with final for the choice
:- choice(a), building(B), company(C), derived_final(C, B) != final(C, B).
:- choice(b), building(B), company(C), derived_final(C, B) != final(C, B).
:- choice(c), building(B), company(C), derived_final(C, B) != final(C, B).
:- choice(d), building(B), company(C), derived_final(C, B) != final(C, B).
:- choice(e), building(B), company(C), derived_final(C, B) != final(C, B).

% Feasibility for each choice
feasible(choice_a) :- choice(a), trade_type(_).
feasible(choice_b) :- choice(b), trade_type(_).
feasible(choice_c) :- choice(c), trade_type(_).
feasible(choice_d) :- choice(d), trade_type(_).
feasible(choice_e) :- choice(e), trade_type(_).

% Map the correct answer to option/1
option(a) :- feasible(choice_a).
option(b) :- feasible(choice_b).
option(c) :- feasible(choice_c).
option(d) :- feasible(choice_d).
option(e) :- feasible(choice_e).

#show option/1.