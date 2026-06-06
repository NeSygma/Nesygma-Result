% Define buildings and their classes
building("GarzaTower"; "YatesHouse"; "ZimmerHouse"; "FloresTower"; "LynchBuilding"; "KingBuilding"; "MeyerBuilding"; "OrtizBuilding").

class("GarzaTower", 1).
class("YatesHouse", 3).
class("ZimmerHouse", 3).
class("FloresTower", 1).
class("LynchBuilding", 2).
class("KingBuilding", 2).
class("MeyerBuilding", 2).
class("OrtizBuilding", 2).

% Define companies
company("RealProp"; "Southco"; "Trustcorp").

% Initial ownership
init_owns("RealProp", "GarzaTower").
init_owns("RealProp", "YatesHouse").
init_owns("RealProp", "ZimmerHouse").
init_owns("Southco", "FloresTower").
init_owns("Southco", "LynchBuilding").
init_owns("Trustcorp", "KingBuilding").
init_owns("Trustcorp", "MeyerBuilding").
init_owns("Trustcorp", "OrtizBuilding").

% Value of each class (class1=4, class2=2, class3=1)
class_value(1, 4).
class_value(2, 2).
class_value(3, 1).

% Each company's total value must remain 6 (invariant from trades)
company_value(C, 6) :- company(C).

% Define the ownership for each option
% Option A: RealProp owns Lynch Building, Meyer Building, and Ortiz Building
owns_a("RealProp", "LynchBuilding").
owns_a("RealProp", "MeyerBuilding").
owns_a("RealProp", "OrtizBuilding").

% Option B: Southco owns Garza Tower and Meyer Building
owns_b("Southco", "GarzaTower").
owns_b("Southco", "MeyerBuilding").

% Option C: Southco owns King Building, Meyer Building, and Ortiz Building
owns_c("Southco", "KingBuilding").
owns_c("Southco", "MeyerBuilding").
owns_c("Southco", "OrtizBuilding").

% Option D: Trustcorp owns Flores Tower and Yates House
owns_d("Trustcorp", "FloresTower").
owns_d("Trustcorp", "YatesHouse").

% Option E: Trustcorp owns Garza Tower and Lynch Building
owns_e("Trustcorp", "GarzaTower").
owns_e("Trustcorp", "LynchBuilding").

% Compute total value for each option's company
value_a(V) :- V = #sum{Val, B : owns_a(C, B), class(B, Cls), class_value(Cls, Val)}.
value_b(V) :- V = #sum{Val, B : owns_b(C, B), class(B, Cls), class_value(Cls, Val)}.
value_c(V) :- V = #sum{Val, B : owns_c(C, B), class(B, Cls), class_value(Cls, Val)}.
value_d(V) :- V = #sum{Val, B : owns_d(C, B), class(B, Cls), class_value(Cls, Val)}.
value_e(V) :- V = #sum{Val, B : owns_e(C, B), class(B, Cls), class_value(Cls, Val)}.

% An option is impossible if its value != 6 (violates the invariant)
impossible(a) :- value_a(V), V != 6.
impossible(b) :- value_b(V), V != 6.
impossible(c) :- value_c(V), V != 6.
impossible(d) :- value_d(V), V != 6.
impossible(e) :- value_e(V), V != 6.

% The answer is the impossible option
answer(X) :- impossible(X).

% Map to option/1
option(a) :- answer(a).
option(b) :- answer(b).
option(c) :- answer(c).
option(d) :- answer(d).
option(e) :- answer(e).

#show option/1.