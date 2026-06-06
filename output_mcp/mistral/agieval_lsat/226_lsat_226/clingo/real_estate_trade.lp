% Companies
company(realprop).
company(southco).
company(trustcorp).

% Buildings and their classes
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

% Helper: get class of a building
class(Building, Class) :- building(Building, Class).

% Define trade types as facts
type(type1).
type(type2).
type(type3).

% Choice rule: which trade happens (if any)
% We allow any possible trade to be chosen
{trade_happens(Company, Type, Building1, Building2, Building3) : 
    company(Company),
    type(Type),
    building(Building1, _),
    building(Building2, _),
    building(Building3, _)}.

% Exactly one trade happens
:- {trade_happens(Company, Type, Building1, Building2, Building3)} != 1.

% Type 1: trade one building for one other building of the same class
% The company gives Building1 and receives Building2
% Both must be of the same class
:- trade_happens(Company, type1, Building1, Building2, _),
   class(Building1, Class1),
   class(Building2, Class2),
   Class1 \= Class2.

% Type 2: trade one class 1 building for two class 2 buildings
% The company gives Building1 (class1) and receives Building2 and Building3 (both class2)
:- trade_happens(Company, type2, Building1, Building2, Building3),
   class(Building1, class1),
   (class(Building2, Class2), Class2 \= class2 ; class(Building3, Class3), Class3 \= class2).

% Type 3: trade one class 2 building for two class 3 buildings
% The company gives Building1 (class2) and receives Building2 and Building3 (both class3)
:- trade_happens(Company, type3, Building1, Building2, Building3),
   class(Building1, class2),
   (class(Building2, Class2), Class2 \= class3 ; class(Building3, Class3), Class3 \= class3).

% Preconditions for trades:
% For Type 1: Company must own Building1 initially
:- trade_happens(Company, type1, Building1, Building2, _),
   not owns(Company, Building1).

% For Type 2: Company must own Building1 (class1) initially
:- trade_happens(Company, type2, Building1, Building2, Building3),
   not owns(Company, Building1).

% For Type 3: Company must own Building1 (class2) initially
:- trade_happens(Company, type3, Building1, Building2, Building3),
   not owns(Company, Building1).

% Helper: a company gives up a building in a trade
trades_away(Company, Building) :-
    trade_happens(Company, _, Building, _, _).

trades_away(Company, Building) :-
    trade_happens(Company, _, _, Building, _).

trades_away(Company, Building) :-
    trade_happens(Company, _, _, _, Building).

% A company owns a building after the trade
owns_after_trade(Company, Building) :-
    owns(Company, Building),
    not trades_away(Company, Building).

owns_after_trade(Company, Building) :-
    trade_happens(OtherCompany, _, _, Building, _),
    Company \= OtherCompany.

owns_after_trade(Company, Building) :-
    trade_happens(OtherCompany, _, _, _, Building),
    Company \= OtherCompany.

% Check against answer choices
% Option A: RealProp: Flores Tower, Garza Tower; Southco: Lynch Building, Yates House, Zimmer House; Trustcorp: King Building, Meyer Building, Ortiz Building
option(a) :-
    owns_after_trade(realprop, garza_tower),
    owns_after_trade(realprop, flores_tower),
    owns_after_trade(southco, lynch_building),
    owns_after_trade(southco, yates_house),
    owns_after_trade(southco, zimmer_house),
    owns_after_trade(trustcorp, king_building),
    owns_after_trade(trustcorp, meyer_building),
    owns_after_trade(trustcorp, ortiz_building),
    not owns_after_trade(realprop, yates_house),
    not owns_after_trade(realprop, zimmer_house).

% Option B: RealProp: Garza Tower, King Building, Ortiz Building; Southco: Flores Tower, Lynch Building; Trustcorp: Meyer Building, Yates House, Zimmer House
option(b) :-
    owns_after_trade(realprop, garza_tower),
    owns_after_trade(realprop, king_building),
    owns_after_trade(realprop, ortiz_building),
    owns_after_trade(southco, flores_tower),
    owns_after_trade(southco, lynch_building),
    owns_after_trade(trustcorp, meyer_building),
    owns_after_trade(trustcorp, yates_house),
    owns_after_trade(trustcorp, zimmer_house),
    not owns_after_trade(realprop, yates_house),
    not owns_after_trade(realprop, zimmer_house),
    not owns_after_trade(trustcorp, king_building),
    not owns_after_trade(trustcorp, ortiz_building).

% Option C: RealProp: Garza Tower, Lynch Building; Southco: Flores Tower, Yates House, Zimmer House; Trustcorp: King Building, Meyer Building, Ortiz Building
option(c) :-
    owns_after_trade(realprop, garza_tower),
    owns_after_trade(realprop, lynch_building),
    owns_after_trade(southco, flores_tower),
    owns_after_trade(southco, yates_house),
    owns_after_trade(southco, zimmer_house),
    owns_after_trade(trustcorp, king_building),
    owns_after_trade(trustcorp, meyer_building),
    owns_after_trade(trustcorp, ortiz_building),
    not owns_after_trade(realprop, yates_house),
    not owns_after_trade(realprop, zimmer_house),
    not owns_after_trade(southco, lynch_building).

% Option D: RealProp: Garza Tower, Meyer Building, Yates House; Southco: Flores Tower, Lynch Building; Trustcorp: King Building, Ortiz Building, Zimmer House
option(d) :-
    owns_after_trade(realprop, garza_tower),
    owns_after_trade(realprop, meyer_building),
    owns_after_trade(realprop, yates_house),
    owns_after_trade(southco, flores_tower),
    owns_after_trade(southco, lynch_building),
    owns_after_trade(trustcorp, king_building),
    owns_after_trade(trustcorp, ortiz_building),
    owns_after_trade(trustcorp, zimmer_house),
    not owns_after_trade(realprop, zimmer_house),
    not owns_after_trade(trustcorp, meyer_building).

% Option E: RealProp: Garza Tower, Yates House, Zimmer House; Southco: Lynch Building, Ortiz Building; Trustcorp: Flores Tower, King Building, Meyer Building
option(e) :-
    owns_after_trade(realprop, garza_tower),
    owns_after_trade(realprop, yates_house),
    owns_after_trade(realprop, zimmer_house),
    owns_after_trade(southco, lynch_building),
    owns_after_trade(southco, ortiz_building),
    owns_after_trade(trustcorp, flores_tower),
    owns_after_trade(trustcorp, king_building),
    owns_after_trade(trustcorp, meyer_building),
    not owns_after_trade(southco, flores_tower),
    not owns_after_trade(trustcorp, ortiz_building).

% Map the correct answer to option/1
option(a) :- option(a).
option(b) :- option(b).
option(c) :- option(c).
option(d) :- option(d).
option(e) :- option(e).

#show option/1.