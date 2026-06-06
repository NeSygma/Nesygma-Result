% Companies
company(realprop). company(southco). company(trustcorp).

% Buildings and classes
building(garza).   class(garza, 1).
building(yates).   class(yates, 3).
building(zimmer).  class(zimmer, 3).
building(flores).  class(flores, 1).
building(lynch).   class(lynch, 2).
building(king).    class(king, 2).
building(meyer).   class(meyer, 2).
building(ortiz).   class(ortiz, 2).

% Value assignment that is invariant under all trades:
% Type 1 (same class swap): value preserved trivially
% Type 2 (1 class1 for 2 class2): 4 = 2+2, preserved
% Type 3 (1 class2 for 2 class3): 2 = 1+1, preserved
value(1, 4). value(2, 2). value(3, 1).

% Initial ownership
init_owner(realprop, garza).  init_owner(realprop, yates).  init_owner(realprop, zimmer).
init_owner(southco, flores).  init_owner(southco, lynch).
init_owner(trustcorp, king).  init_owner(trustcorp, meyer). init_owner(trustcorp, ortiz).

% Compute initial value of each company
init_value(C, V) :- company(C), V = #sum { Val, B : init_owner(C, B), class(B, CL), value(CL, Val) }.

% --- Option definitions: which buildings each option assigns to which company ---

% Option A: RealProp has Lynch, Meyer, Ortiz
opt_a_owner(realprop, lynch). opt_a_owner(realprop, meyer). opt_a_owner(realprop, ortiz).
% (Other buildings go to other companies - not relevant for value check)

% Option B: Southco has Garza, Meyer
opt_b_owner(southco, garza). opt_b_owner(southco, meyer).

% Option C: Southco has King, Meyer, Ortiz
opt_c_owner(southco, king). opt_c_owner(southco, meyer). opt_c_owner(southco, ortiz).

% Option D: Trustcorp has Flores, Yates
opt_d_owner(trustcorp, flores). opt_d_owner(trustcorp, yates).

% Option E: Trustcorp has Garza, Lynch
opt_e_owner(trustcorp, garza). opt_e_owner(trustcorp, lynch).

% Compute value of the specified company's buildings in each option
opt_a_val(V) :- V = #sum { Val, B : opt_a_owner(realprop, B), class(B, CL), value(CL, Val) }.
opt_b_val(V) :- V = #sum { Val, B : opt_b_owner(southco, B), class(B, CL), value(CL, Val) }.
opt_c_val(V) :- V = #sum { Val, B : opt_c_owner(southco, B), class(B, CL), value(CL, Val) }.
opt_d_val(V) :- V = #sum { Val, B : opt_d_owner(trustcorp, B), class(B, CL), value(CL, Val) }.
opt_e_val(V) :- V = #sum { Val, B : opt_e_owner(trustcorp, B), class(B, CL), value(CL, Val) }.

% An option is IMPOSSIBLE if the value of the specified company's buildings
% does not equal that company's initial value (invariant violation)
impossible_a :- opt_a_val(V1), init_value(realprop, V2), V1 != V2.
impossible_b :- opt_b_val(V1), init_value(southco, V2), V1 != V2.
impossible_c :- opt_c_val(V1), init_value(southco, V2), V1 != V2.
impossible_d :- opt_d_val(V1), init_value(trustcorp, V2), V1 != V2.
impossible_e :- opt_e_val(V1), init_value(trustcorp, V2), V1 != V2.

% Map the correct answer to option/1
option(a) :- impossible_a.
option(b) :- impossible_b.
option(c) :- impossible_c.
option(d) :- impossible_d.
option(e) :- impossible_e.

#show option/1.
#show init_value/2.
#show opt_a_val/1.
#show opt_b_val/1.
#show opt_c_val/1.
#show opt_d_val/1.
#show opt_e_val/1.