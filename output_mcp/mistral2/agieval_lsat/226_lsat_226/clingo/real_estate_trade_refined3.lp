% --- Base facts ---
company(realprop).
company(southco).
company(trustcorp).

building(garza_tower, class1).
building(yates_house, class3).
building(zimmer_house, class3).
building(flores_tower, class1).
building(lynch_building, class2).
building(king_building, class2).
building(meyer_building, class2).
building(ortiz_building, class2).

% Initial ownership
owns(realprop, garza_tower).
owns(realprop, yates_house).
owns(realprop, zimmer_house).
owns(southco, flores_tower).
owns(southco, lynch_building).
owns(trustcorp, king_building).
owns(trustcorp, meyer_building).
owns(trustcorp, ortiz_building).

% Trade types
type(1). % Trade one building for one other building of the same class
type(2). % Trade one class1 building for two class2 buildings
type(3). % Trade one class2 building for two class3 buildings

% --- Trade rules ---
% Trade type 1: Trade one building for one other building of the same class
% traded(C1, B1, C2, B2) means C1 gives B1 to C2 and C2 gives B2 to C1
1 { traded(C1, B1, C2, B2) : 
        owns(C1, B1), 
        owns(C2, B2), 
        building(B1, Class), 
        building(B2, Class), 
        C1 != C2 
    } 1 :- type(1).

% Trade type 2: Trade one class1 building for two class2 buildings
% traded(C1, B1, C2, B21, B22) means C1 gives B1 to C2 and C2 gives B21 and B22 to C1
1 { traded(C1, B1, C2, B21, B22) : 
        owns(C1, B1), 
        building(B1, class1), 
        owns(C2, B21), owns(C2, B22), 
        building(B21, class2), building(B22, class2), 
        B21 != B22, 
        C1 != C2 
    } 1 :- type(2).

% Trade type 3: Trade one class2 building for two class3 buildings
% traded(C1, B1, C2, B21, B22) means C1 gives B1 to C2 and C2 gives B21 and B22 to C1
1 { traded(C1, B1, C2, B21, B22) : 
        owns(C1, B1), 
        building(B1, class2), 
        owns(C2, B21), owns(C2, B22), 
        building(B21, class3), building(B22, class3), 
        B21 != B22, 
        C1 != C2 
    } 1 :- type(3).

% --- Final ownership ---
% If a building is not traded away, it remains owned by the original company
final_owns(C, B) :- owns(C, B), not traded_away(C, B).

% If a company receives a building, it is owned by that company
final_owns(C2, B1) :- traded(C1, B1, C2, _).
final_owns(C1, B21) :- traded(C1, _, C2, B21, _).
final_owns(C1, B22) :- traded(C1, _, C2, _, B22).

% If a company gives away a building, it no longer owns it
traded_away(C1, B1) :- traded(C1, B1, _, _).
traded_away(C2, B21) :- traded(_, _, C2, B21, _).
traded_away(C2, B22) :- traded(_, _, C2, _, B22).

% --- Constraints ---
% Only one trade is allowed
:- { traded(_, _, _, _) } > 1.
:- { traded(_, _, _, _, _) } > 1.

% --- Options ---
% Option A: RealProp: Flores Tower, Garza Tower; Southco: Lynch Building, Yates House, Zimmer House; Trustcorp: King Building, Meyer Building, Ortiz Building
option(a) :-
    final_owns(realprop, flores_tower),
    final_owns(realprop, garza_tower),
    not final_owns(realprop, yates_house),
    not final_owns(realprop, zimmer_house),
    final_owns(southco, lynch_building),
    final_owns(southco, yates_house),
    final_owns(southco, zimmer_house),
    final_owns(trustcorp, king_building),
    final_owns(trustcorp, meyer_building),
    final_owns(trustcorp, ortiz_building).

% Option B: RealProp: Garza Tower, King Building, Ortiz Building; Southco: Flores Tower, Lynch Building; Trustcorp: Meyer Building, Yates House, Zimmer House
option(b) :-
    final_owns(realprop, garza_tower),
    final_owns(realprop, king_building),
    final_owns(realprop, ortiz_building),
    final_owns(southco, flores_tower),
    final_owns(southco, lynch_building),
    not final_owns(southco, yates_house),
    not final_owns(southco, zimmer_house),
    final_owns(trustcorp, meyer_building),
    final_owns(trustcorp, yates_house),
    final_owns(trustcorp, zimmer_house).

% Option C: RealProp: Garza Tower, Lynch Building; Southco: Flores Tower, Yates House, Zimmer House; Trustcorp: King Building, Meyer Building, Ortiz Building
option(c) :-
    final_owns(realprop, garza_tower),
    final_owns(realprop, lynch_building),
    not final_owns(realprop, yates_house),
    not final_owns(realprop, zimmer_house),
    final_owns(southco, flores_tower),
    final_owns(southco, yates_house),
    final_owns(southco, zimmer_house),
    final_owns(trustcorp, king_building),
    final_owns(trustcorp, meyer_building),
    final_owns(trustcorp, ortiz_building).

% Option D: RealProp: Garza Tower, Meyer Building, Yates House; Southco: Flores Tower, Lynch Building; Trustcorp: King Building, Ortiz Building, Zimmer House
option(d) :-
    final_owns(realprop, garza_tower),
    final_owns(realprop, meyer_building),
    final_owns(realprop, yates_house),
    not final_owns(realprop, zimmer_house),
    final_owns(southco, flores_tower),
    final_owns(southco, lynch_building),
    not final_owns(southco, yates_house),
    not final_owns(southco, zimmer_house),
    final_owns(trustcorp, king_building),
    final_owns(trustcorp, ortiz_building),
    final_owns(trustcorp, zimmer_house).

% Option E: RealProp: Garza Tower, Yates House, Zimmer House; Southco: Lynch Building, Ortiz Building; Trustcorp: Flores Tower, King Building, Meyer Building
option(e) :-
    final_owns(realprop, garza_tower),
    final_owns(realprop, yates_house),
    final_owns(realprop, zimmer_house),
    final_owns(southco, lynch_building),
    final_owns(southco, ortiz_building),
    final_owns(trustcorp, flores_tower),
    final_owns(trustcorp, king_building),
    final_owns(trustcorp, meyer_building),
    not final_owns(trustcorp, ortiz_building).

% --- Show the correct option ---
#show option/1.