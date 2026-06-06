%%% DATA %%%

% Companies
company(realprop; southco; trustcorp).

% Buildings
building(garza_tower; yates_house; zimmer_house; flores_tower; lynch_building; king_building; meyer_building; ortiz_building).

% Classes
class(1;2;3).

% Building classes
building_class(garza_tower, 1).
building_class(yates_house, 3).
building_class(zimmer_house, 3).
building_class(flores_tower, 1).
building_class(lynch_building, 2).
building_class(king_building, 2).
building_class(meyer_building, 2).
building_class(ortiz_building, 2).

% Initial ownership
initial_owner(garza_tower, realprop).
initial_owner(yates_house, realprop).
initial_owner(zimmer_house, realprop).
initial_owner(flores_tower, southco).
initial_owner(lynch_building, southco).
initial_owner(king_building, trustcorp).
initial_owner(meyer_building, trustcorp).
initial_owner(ortiz_building, trustcorp).

%%% TRADE MODEL %%%

% Choose exactly one kind of trade
1 { trade_kind(1); trade_kind(2); trade_kind(3) } 1.

% Choose giver and receiver (distinct companies)
1 { giver(C) : company(C) } 1.
1 { receiver(C) : company(C) } 1.
:- giver(C), receiver(C).

% For Kind 1: trade one building for one other building of the same class
1 { trade_give(B) : building(B), initial_owner(B, C), giver(C) } 1 :- trade_kind(1).
1 { trade_receive(B) : building(B), initial_owner(B, C), receiver(C) } 1 :- trade_kind(1).

% Same class constraint for kind 1
:- trade_kind(1), trade_give(B1), trade_receive(B2), building_class(B1, C1), building_class(B2, C2), C1 != C2.

% For Kind 2: trade one class 1 building for two class 2 buildings
1 { trade_give(B) : building(B), initial_owner(B, C), giver(C), building_class(B, 1) } 1 :- trade_kind(2).
2 { trade_receive(B) : building(B), initial_owner(B, C), receiver(C), building_class(B, 2) } 2 :- trade_kind(2).

% For Kind 3: trade one class 2 building for two class 3 buildings
1 { trade_give(B) : building(B), initial_owner(B, C), giver(C), building_class(B, 2) } 1 :- trade_kind(3).
2 { trade_receive(B) : building(B), initial_owner(B, C), receiver(C), building_class(B, 3) } 2 :- trade_kind(3).

% Buildings given and received must be disjoint
:- trade_give(B), trade_receive(B).

%%% FINAL OWNERSHIP %%%

% Giver loses the buildings they gave, gains the buildings they received
final_owner(B, R) :- trade_give(B), receiver(R).
final_owner(B, G) :- trade_receive(B), giver(G).

% All other buildings keep their initial owner
final_owner(B, O) :- building(B), initial_owner(B, O), not trade_give(B), not trade_receive(B).

% Each building has exactly one final owner
:- building(B), #count { C : final_owner(B, C) } != 1.

%%% OPTIONS DATA %%%

option(a;b;c;d;e).

% Option A: RealProp: Flores Tower, Garza Tower; Southco: Lynch, Yates, Zimmer; Trustcorp: King, Meyer, Ortiz
option_bld_owner(a, realprop, flores_tower).
option_bld_owner(a, realprop, garza_tower).
option_bld_owner(a, southco, lynch_building).
option_bld_owner(a, southco, yates_house).
option_bld_owner(a, southco, zimmer_house).
option_bld_owner(a, trustcorp, king_building).
option_bld_owner(a, trustcorp, meyer_building).
option_bld_owner(a, trustcorp, ortiz_building).

% Option B: RealProp: Garza, King, Ortiz; Southco: Flores, Lynch; Trustcorp: Meyer, Yates, Zimmer
option_bld_owner(b, realprop, garza_tower).
option_bld_owner(b, realprop, king_building).
option_bld_owner(b, realprop, ortiz_building).
option_bld_owner(b, southco, flores_tower).
option_bld_owner(b, southco, lynch_building).
option_bld_owner(b, trustcorp, meyer_building).
option_bld_owner(b, trustcorp, yates_house).
option_bld_owner(b, trustcorp, zimmer_house).

% Option C: RealProp: Garza, Lynch; Southco: Flores, Yates, Zimmer; Trustcorp: King, Meyer, Ortiz
option_bld_owner(c, realprop, garza_tower).
option_bld_owner(c, realprop, lynch_building).
option_bld_owner(c, southco, flores_tower).
option_bld_owner(c, southco, yates_house).
option_bld_owner(c, southco, zimmer_house).
option_bld_owner(c, trustcorp, king_building).
option_bld_owner(c, trustcorp, meyer_building).
option_bld_owner(c, trustcorp, ortiz_building).

% Option D: RealProp: Garza, Meyer, Yates; Southco: Flores, Lynch; Trustcorp: King, Ortiz, Zimmer
option_bld_owner(d, realprop, garza_tower).
option_bld_owner(d, realprop, meyer_building).
option_bld_owner(d, realprop, yates_house).
option_bld_owner(d, southco, flores_tower).
option_bld_owner(d, southco, lynch_building).
option_bld_owner(d, trustcorp, king_building).
option_bld_owner(d, trustcorp, ortiz_building).
option_bld_owner(d, trustcorp, zimmer_house).

% Option E: RealProp: Garza, Yates, Zimmer; Southco: Lynch, Ortiz; Trustcorp: Flores, King, Meyer
option_bld_owner(e, realprop, garza_tower).
option_bld_owner(e, realprop, yates_house).
option_bld_owner(e, realprop, zimmer_house).
option_bld_owner(e, southco, lynch_building).
option_bld_owner(e, southco, ortiz_building).
option_bld_owner(e, trustcorp, flores_tower).
option_bld_owner(e, trustcorp, king_building).
option_bld_owner(e, trustcorp, meyer_building).

% Ensure each option assigns each building to exactly one company
:- building(B), option(Opt), not option_bld_owner(Opt, _, B).

%%% CHECK WHICH OPTIONS MATCH THE TRADE RESULT %%%

% An option matches if all its building assignments match the final ownership
matches(Opt) :- option(Opt), 
    #count { B : building(B), option_bld_owner(Opt, C, B), final_owner(B, C) } = 8.

#show matches/1.
#show final_owner/2.
#show trade_kind/1.
#show giver/1.
#show receiver/1.
#show trade_give/1.
#show trade_receive/1.