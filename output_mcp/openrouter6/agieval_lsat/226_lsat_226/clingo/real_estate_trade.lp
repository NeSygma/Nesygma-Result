% Real Estate Trade Problem

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
owned(realprop, garza_tower).
owned(realprop, yates_house).
owned(realprop, zimmer_house).
owned(southco, flores_tower).
owned(southco, lynch_building).
owned(trustcorp, king_building).
owned(trustcorp, meyer_building).
owned(trustcorp, ortiz_building).

% Answer choices as facts
choice_a. choice_b. choice_c. choice_d. choice_e.

% Owned final for choice A
owned_final(realprop, garza_tower) :- choice_a.
owned_final(realprop, flores_tower) :- choice_a.
owned_final(southco, lynch_building) :- choice_a.
owned_final(southco, yates_house) :- choice_a.
owned_final(southco, zimmer_house) :- choice_a.
owned_final(trustcorp, king_building) :- choice_a.
owned_final(trustcorp, meyer_building) :- choice_a.
owned_final(trustcorp, ortiz_building) :- choice_a.

% Owned final for choice B
owned_final(realprop, garza_tower) :- choice_b.
owned_final(realprop, king_building) :- choice_b.
owned_final(realprop, ortiz_building) :- choice_b.
owned_final(southco, flores_tower) :- choice_b.
owned_final(southco, lynch_building) :- choice_b.
owned_final(trustcorp, meyer_building) :- choice_b.
owned_final(trustcorp, yates_house) :- choice_b.
owned_final(trustcorp, zimmer_house) :- choice_b.

% Owned final for choice C
owned_final(realprop, garza_tower) :- choice_c.
owned_final(realprop, lynch_building) :- choice_c.
owned_final(southco, flores_tower) :- choice_c.
owned_final(southco, yates_house) :- choice_c.
owned_final(southco, zimmer_house) :- choice_c.
owned_final(trustcorp, king_building) :- choice_c.
owned_final(trustcorp, meyer_building) :- choice_c.
owned_final(trustcorp, ortiz_building) :- choice_c.

% Owned final for choice D
owned_final(realprop, garza_tower) :- choice_d.
owned_final(realprop, meyer_building) :- choice_d.
owned_final(realprop, yates_house) :- choice_d.
owned_final(southco, flores_tower) :- choice_d.
owned_final(southco, lynch_building) :- choice_d.
owned_final(trustcorp, king_building) :- choice_d.
owned_final(trustcorp, ortiz_building) :- choice_d.
owned_final(trustcorp, zimmer_house) :- choice_d.

% Owned final for choice E
owned_final(realprop, garza_tower) :- choice_e.
owned_final(realprop, yates_house) :- choice_e.
owned_final(realprop, zimmer_house) :- choice_e.
owned_final(southco, lynch_building) :- choice_e.
owned_final(southco, ortiz_building) :- choice_e.
owned_final(trustcorp, flores_tower) :- choice_e.
owned_final(trustcorp, king_building) :- choice_e.
owned_final(trustcorp, meyer_building) :- choice_e.

% Ensure each building is owned by exactly one company in owned_final for each choice
1 { owned_final(C, B) : company(C) } 1 :- building(B), choice_a.
1 { owned_final(C, B) : company(C) } 1 :- building(B), choice_b.
1 { owned_final(C, B) : company(C) } 1 :- building(B), choice_c.
1 { owned_final(C, B) : company(C) } 1 :- building(B), choice_d.
1 { owned_final(C, B) : company(C) } 1 :- building(B), choice_e.

% Trade types
trade_type(1). trade_type(2). trade_type(3).

% Select two companies for the trade
{ selected_company(C) } 2 :- company(C).
:- #count { C : selected_company(C) } != 2.

% Order the selected companies
selected_company_ordered(C1, C2) :- selected_company(C1), selected_company(C2), C1 < C2.

% Transfer choice rules: for each building owned by a selected company, it can be transferred to the other selected company
{ transfer(C1, C2, B) } :- selected_company_ordered(C1, C2), building(B), owned(C1, B).
{ transfer(C2, C1, B) } :- selected_company_ordered(C1, C2), building(B), owned(C2, B).

% Ensure each building is transferred at most once
:- transfer(_, _, B1), transfer(_, _, B2), B1 = B2.

% Count transfers per direction
count_c1_to_c2(N) :- N = #count { B : transfer(C1, C2, B) }.
count_c2_to_c1(N) :- N = #count { B : transfer(C2, C1, B) }.

% Trade type constraints
% Type 1: one transfer each direction, same class
:- trade_type(1), count_c1_to_c2(N), N != 1.
:- trade_type(1), count_c2_to_c1(N), N != 1.
:- trade_type(1), transfer(C1, C2, B1), transfer(C2, C1, B2), class(B1, CL1), class(B2, CL2), CL1 != CL2.

% Type 2: one transfer from C1 to C2 (class 1), two transfers from C2 to C1 (class 2)
:- trade_type(2), transfer(C1, C2, B), class(B, CL), CL != 1.
:- trade_type(2), transfer(C2, C1, B), class(B, CL), CL != 2.
:- trade_type(2), count_c2_to_c1(N), N != 2.

% Type 3: one transfer from C1 to C2 (class 2), two transfers from C2 to C1 (class 3)
:- trade_type(3), transfer(C1, C2, B), class(B, CL), CL != 2.
:- trade_type(3), transfer(C2, C1, B), class(B, CL), CL != 3.
:- trade_type(3), count_c2_to_c1(N), N != 2.

% Derived final ownership from transfers
transferred_from(C, B) :- transfer(C, _, B).
transferred_to(C, B) :- transfer(_, C, B).

derived_final(C, B) :- owned(C, B), not transferred_from(C, B).
derived_final(C, B) :- transferred_to(C, B).

% Ensure each building has exactly one owner in derived_final
1 { derived_final(C, B) : company(C) } 1 :- building(B).

% Match derived_final with owned_final for the choice
:- choice_a, building(B), company(C), derived_final(C, B) != owned_final(C, B).
:- choice_b, building(B), company(C), derived_final(C, B) != owned_final(C, B).
:- choice_c, building(B), company(C), derived_final(C, B) != owned_final(C, B).
:- choice_d, building(B), company(C), derived_final(C, B) != owned_final(C, B).
:- choice_e, building(B), company(C), derived_final(C, B) != owned_final(C, B).

% Feasibility for each choice
feasible(choice_a) :- choice_a, trade_type(_), selected_company(_), transfer(_, _, _).
feasible(choice_b) :- choice_b, trade_type(_), selected_company(_), transfer(_, _, _).
feasible(choice_c) :- choice_c, trade_type(_), selected_company(_), transfer(_, _, _).
feasible(choice_d) :- choice_d, trade_type(_), selected_company(_), transfer(_, _, _).
feasible(choice_e) :- choice_e, trade_type(_), selected_company(_), transfer(_, _, _).

% Map the correct answer to option/1
option(a) :- feasible(choice_a).
option(b) :- feasible(choice_b).
option(c) :- feasible(choice_c).
option(d) :- feasible(choice_d).
option(e) :- feasible(choice_e).

#show option/1.