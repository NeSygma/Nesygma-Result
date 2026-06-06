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

%% Initial counts per company
init_c1(realprop, 1). init_c2(realprop, 0). init_c3(realprop, 2).
init_c1(southco, 1). init_c2(southco, 1). init_c3(southco, 0).
init_c1(trustcorp, 0). init_c2(trustcorp, 3). init_c3(trustcorp, 0).

%% Total counts
total_class1(2). total_class2(4). total_class3(2).

%% Each building is owned by exactly one company
{ owns(C, B) } :- company(C), building(B).
:- building(B), not { owns(C, B) : company(C) } 1.
:- building(B), { owns(C, B) : company(C) } > 1.

%% Count per company per class
c1_count(C, N) :- N = #count { B : owns(C, B), building_class(B, 1) }, company(C).
c2_count(C, N) :- N = #count { B : owns(C, B), building_class(B, 2) }, company(C).
c3_count(C, N) :- N = #count { B : owns(C, B), building_class(B, 3) }, company(C).

%% Total counts must match
:- total_class1(T1), S1 = #sum { N, C : c1_count(C, N) }, S1 != T1.
:- total_class2(T2), S2 = #sum { N, C : c2_count(C, N) }, S2 != T2.
:- total_class3(T3), S3 = #sum { N, C : c3_count(C, N) }, S3 != T3.

%% Invariant: Each company's total value is conserved.
%% Value: class 1 = 4, class 2 = 2, class 3 = 1
%% (Because 1 class 1 = 2 class 2 = 4 class 3)
value(C, V) :- V = 4*N1 + 2*N2 + 1*N3, c1_count(C, N1), c2_count(C, N2), c3_count(C, N3).

:- company(C), init_c1(C, I1), init_c2(C, I2), init_c3(C, I3),
   init_value = 4*I1 + 2*I2 + 1*I3,
   value(C, V), V != init_value.

%% Condition: RealProp owns only class 2 buildings
:- c1_count(realprop, N), N > 0.
:- c3_count(realprop, N), N > 0.

%% RealProp must own at least one building (otherwise "owns only class 2" is vacuously true but unlikely)
%% Let's not add this constraint.

%% Let's compute what the counts must be for RealProp.
%% RealProp value = 6. If RealProp has only class 2 buildings, then 2*N = 6, so N = 3.
%% RealProp must own exactly 3 class 2 buildings.
:- c2_count(realprop, N), N != 3.

%% Now, total class 2 buildings = 4. So Southco + Trustcorp have 1 class 2 building total.
%% Total class 1 buildings = 2. RealProp has 0. So Southco + Trustcorp have 2 class 1 buildings.
%% Total class 3 buildings = 2. RealProp has 0. So Southco + Trustcorp have 2 class 3 buildings.

%% Let's enumerate all possible models and see what's common.

%% (A) Trustcorp owns a class 1 building.
trustcorp_has_c1 :- c1_count(trustcorp, N), N > 0.

%% (B) Trustcorp owns the Meyer Building.
trustcorp_owns_meyer :- owns(trustcorp, meyer_building).

%% (C) Southco owns a class 2 building.
southco_has_c2 :- c2_count(southco, N), N > 0.

%% (D) Southco owns both of the class 3 buildings.
southco_has_both_c3 :- owns(southco, yates_house), owns(southco, zimmer_house).

%% (E) Southco owns the Flores Tower.
southco_owns_flores :- owns(southco, flores_tower).

#show owns/2.
#show c1_count/2.
#show c2_count/2.
#show c3_count/2.
#show trustcorp_has_c1/0.
#show trustcorp_owns_meyer/0.
#show southco_has_c2/0.
#show southco_has_both_c3/0.
#show southco_owns_flores/0.