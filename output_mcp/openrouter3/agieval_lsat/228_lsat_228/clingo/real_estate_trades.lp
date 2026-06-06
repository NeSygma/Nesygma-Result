% Companies
company(realprop). company(southco). company(trustcorp).

% Buildings with classes
building(garza_tower, 1).
building(yates_house, 3).
building(zimmer_house, 3).
building(flores_tower, 1).
building(lynch_building, 2).
building(king_building, 2).
building(meyer_building, 2).
building(ortiz_building, 2).

% All buildings
building(B) :- building(B, _).

% Classes
class(1). class(2). class(3).

% Initial ownership
initial_owner(garza_tower, realprop).
initial_owner(yates_house, realprop).
initial_owner(zimmer_house, realprop).
initial_owner(flores_tower, southco).
initial_owner(lynch_building, southco).
initial_owner(king_building, trustcorp).
initial_owner(meyer_building, trustcorp).
initial_owner(ortiz_building, trustcorp).

% Final ownership - each building owned by exactly one company
{ final_owner(B, C) } :- building(B), company(C).
1 { final_owner(B, C) : company(C) } 1 :- building(B).

% Count buildings per class for each company in final state
class_count(C, Class, N) :- company(C), class(Class),
    N = #count{ B : final_owner(B, C), building(B, Class) }.

% Initial class counts
init_class_count(realprop, 1, 1).  % Garza Tower
init_class_count(realprop, 3, 2).  % Yates House, Zimmer House
init_class_count(southco, 1, 1).   % Flores Tower
init_class_count(southco, 2, 1).   % Lynch Building
init_class_count(trustcorp, 2, 3). % King, Meyer, Ortiz

% Total class counts across all companies (should be preserved)
total_class(Class, N) :- class(Class),
    N = #sum{ Count, C : init_class_count(C, Class, Count) }.

% Final total class counts must equal initial
:- class(Class),
    Final = #sum{ Count, C : class_count(C, Class, Count) },
    Init = #sum{ Count, C : init_class_count(C, Class, Count) },
    Final != Init.

% The key constraint: RealProp owns only class 2 buildings after trades
% This means: RealProp has zero class 1 and zero class 3 buildings
:- class_count(realprop, 1, N), N > 0.
:- class_count(realprop, 3, N), N > 0.

% RealProp must have at least one building (it has 3 buildings initially)
:- class_count(realprop, 2, N), N < 3.

% Now, let's derive the answer choices

% A: Trustcorp owns a class 1 building
trustcorp_has_class1 :- class_count(trustcorp, 1, N), N > 0.

% B: Trustcorp owns the Meyer Building
trustcorp_has_meyer :- final_owner(meyer_building, trustcorp).

% C: Southco owns a class 2 building
southco_has_class2 :- class_count(southco, 2, N), N > 0.

% D: Southco owns both of the class 3 buildings
southco_has_both_class3 :-
    final_owner(yates_house, southco),
    final_owner(zimmer_house, southco).

% E: Southco owns the Flores Tower
southco_has_flores :- final_owner(flores_tower, southco).

% Now, we need to find which one MUST be true
% We'll check each condition and see if it's forced by the constraints

% Let's add reasoning about the trades

% RealProp must trade its class 1 building for two class 2 buildings
% This requires a trading partner with at least two class 2 buildings
% Initially, only Trustcorp has at least two class 2 buildings (3 total)
% So RealProp must trade with Trustcorp for the class 1 for two class 2 trade

% Therefore, Trustcorp receives Garza Tower (class 1)
% So Trustcorp must own a class 1 building

% This makes answer A true

% Map the correct answer to option/1
option(a) :- trustcorp_has_class1.
option(b) :- trustcorp_has_meyer.
option(c) :- southco_has_class2.
option(d) :- southco_has_both_class3.
option(e) :- southco_has_flores.

#show option/1.
#show trustcorp_has_class1/0.
#show trustcorp_has_meyer/0.
#show southco_has_class2/0.
#show southco_has_both_class3/0.
#show southco_has_flores/0.
#show class_count/3.
#show final_owner/2.