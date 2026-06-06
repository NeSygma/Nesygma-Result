% Companies
company(realprop). company(southco). company(trustcorp).

% Buildings and classes
building(garza). class(garza,1).
building(yates). class(yates,3).
building(zimmer). class(zimmer,3).
building(flores). class(flores,1).
building(lynch). class(lynch,2).
building(king). class(king,2).
building(meyer). class(meyer,2).
building(ortiz). class(ortiz,2).

% Each building owned by exactly one company
1 { owns(C,B) : company(C) } 1 :- building(B).

% RealProp ends with only class 2 buildings
:- owns(realprop,B), class(B,Cls), Cls != 2.

% Options
option(a) :- owns(trustcorp,B), class(B,1).
option(b) :- owns(trustcorp,meyer).
option(c) :- owns(southco,B), class(B,2).
option(d) :- owns(southco,yates), owns(southco,zimmer).
option(e) :- owns(southco,flores).

#show option/1.