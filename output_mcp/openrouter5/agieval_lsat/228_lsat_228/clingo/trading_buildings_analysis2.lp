%% Problem: Three real estate companies trading buildings
%% We need to determine what MUST be true if RealProp ends up owning only class 2 buildings.

%% --- Domain Definitions ---

%% Companies
company(realprop; southco; trustcorp).

%% Buildings with their classes
building(garza_tower; yates_house; zimmer_house; flores_tower; lynch_building; king_building; meyer_building; ortiz_building).

%% Building classes
building_class(garza_tower, 1).
building_class(yates_house, 3).
building_class(zimmer_house, 3).
building_class(flores_tower, 1).
building_class(lynch_building, 2).
building_class(king_building, 2).
building_class(meyer_building, 2).
building_class(ortiz_building, 2).

%% Initial ownership
init_owner(garza_tower, realprop).
init_owner(yates_house, realprop).
init_owner(zimmer_house, realprop).
init_owner(flores_tower, southco).
init_owner(lynch_building, southco).
init_owner(king_building, trustcorp).
init_owner(meyer_building, trustcorp).
init_owner(ortiz_building, trustcorp).

%% Each building is owned by exactly one company
{ owns(C, B) } :- company(C), building(B).
:- building(B), not { owns(C, B) : company(C) } 1.
:- building(B), { owns(C, B) : company(C) } > 1.

%% Count per company per class
c1_count(C, N) :- N = #count { B : owns(C, B), building_class(B, 1) }, company(C).
c2_count(C, N) :- N = #count { B : owns(C, B), building_class(B, 2) }, company(C).
c3_count(C, N) :- N = #count { B : owns(C, B), building_class(B, 3) }, company(C).

%% Total counts must match
total_class1(2). total_class2(4). total_class3(2).
:- total_class1(T1), S1 = #sum { N, C : c1_count(C, N) }, S1 != T1.
:- total_class2(T2), S2 = #sum { N, C : c2_count(C, N) }, S2 != T2.
:- total_class3(T3), S3 = #sum { N, C : c3_count(C, N) }, S3 != T3.

%% Value conservation: class 1 = 4, class 2 = 2, class 3 = 1
value(C, V) :- V = 4*N1 + 2*N2 + 1*N3, c1_count(C, N1), c2_count(C, N2), c3_count(C, N3).

init_value(realprop, 6).  % 1*4 + 0*2 + 2*1 = 6
init_value(southco, 6).   % 1*4 + 1*2 + 0*1 = 6
init_value(trustcorp, 6). % 0*4 + 3*2 + 0*1 = 6

:- company(C), init_value(C, IV), value(C, V), V != IV.

%% Condition: RealProp owns only class 2 buildings
:- c1_count(realprop, N), N > 0.
:- c3_count(realprop, N), N > 0.

%% RealProp value = 6. If only class 2, then 2*N = 6, so N = 3.
:- c2_count(realprop, N), N != 3.

%% Now let's check each option for MUST BE TRUE.
%% We'll use a trick: for each option, check if there exists a model where it's false.
%% If no model exists where it's false, then it MUST be true.

%% (A) Trustcorp owns a class 1 building.
%% Check if there's a model where trustcorp has no class 1.
:- not trustcorp_has_c1.
trustcorp_has_c1 :- c1_count(trustcorp, N), N > 0.

%% (B) Trustcorp owns the Meyer Building.
:- not trustcorp_owns_meyer.
trustcorp_owns_meyer :- owns(trustcorp, meyer_building).

%% (C) Southco owns a class 2 building.
:- not southco_has_c2.
southco_has_c2 :- c2_count(southco, N), N > 0.

%% (D) Southco owns both of the class 3 buildings.
:- not southco_has_both_c3.
southco_has_both_c3 :- owns(southco, yates_house), owns(southco, zimmer_house).

%% (E) Southco owns the Flores Tower.
:- not southco_owns_flores.
southco_owns_flores :- owns(southco, flores_tower).

#show owns/2.
#show c1_count/2.
#show c2_count/2.
#show c3_count/2.