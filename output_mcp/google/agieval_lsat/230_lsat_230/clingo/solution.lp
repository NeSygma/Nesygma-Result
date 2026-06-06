% Define buildings and their classes
building(gt, 1). building(ft, 1).
building(lb, 2). building(kb, 2). building(mb, 2). building(ob, 2).
building(yh, 3). building(zh, 3).

% Define values for classes
value(1, 4).
value(2, 2).
value(3, 1).

% Define initial ownership
initial_owns(realprop, gt). initial_owns(realprop, yh). initial_owns(realprop, zh).
initial_owns(southco, ft). initial_owns(southco, lb).
initial_owns(trustcorp, kb). initial_owns(trustcorp, mb). initial_owns(trustcorp, ob).

% Calculate initial value for each company
company_value(C, V) :- company(C), V = #sum { Val, B : initial_owns(C, B), building(B, Class), value(Class, Val) }.
company(realprop). company(southco). company(trustcorp).

% Define options
% (A) RP: {LB, MB, OB}
option_value(a, 2+2+2).
% (B) SC: {GT, MB}
option_value(b, 4+2).
% (C) SC: {KB, MB, OB}
option_value(c, 2+2+2).
% (D) TC: {FT, YH}
option_value(d, 4+1).
% (E) TC: {GT, LB}
option_value(e, 4+2).

% The invariant is that the total value of each company's holdings is 6.
% Check which option violates this invariant.
option(X) :- option_value(X, V), V != 6.

#show option/1.