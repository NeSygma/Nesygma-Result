% Universe elements
element(1..20).

% Sets
set(0..13).

% Set elements
set_elements(0,1;2;3;4;5).
set_elements(1,1;6;11;16).
set_elements(2,2;7;12;17).
set_elements(3,3;8;13;18).
set_elements(4,4;9;14;19).
set_elements(5,5;10;15;20).
set_elements(6,6;7;8;9;10).
set_elements(7,1;3;5;7;9).
set_elements(8,2;4;6;8;10).
set_elements(9,1;2;3;4;5;6;7).
set_elements(10,11;12;13;14;15).
set_elements(11,8;9;10).
set_elements(12,1;5;10;15).
set_elements(13,16;17;18;19;20).

% Set costs
set_cost(0,1). set_cost(1,1). set_cost(2,1).
set_cost(3,1). set_cost(4,1). set_cost(5,1).
set_cost(6,1). set_cost(7,1). set_cost(8,1).
set_cost(9,4). set_cost(10,4). set_cost(11,4).
set_cost(12,4). set_cost(13,4).

% Set categories
set_category(0,"A"). set_category(1,"A"). set_category(2,"A").
set_category(3,"B"). set_category(4,"B"). set_category(5,"B").
set_category(6,"C"). set_category(7,"C"). set_category(8,"C").
set_category(9,"specialized"). set_category(10,"specialized").
set_category(11,"specialized"). set_category(12,"specialized").
set_category(13,"specialized").

% Choice rule for set selection
{selected(S)} :- set(S).

% Prerequisites
:- selected(9), not selected(0).
:- selected(11), not selected(6).

% Mutual exclusion
:- selected(12), selected(13).

% Category balancing: If any specialized set is selected, ensure at least one from each standard category
:- selected(S), set_cost(S, Cost), Cost > 1,  % S is a specialized set
   not has_category_A, not has_category_B, not has_category_C.

has_category_A :- selected(S), set_category(S,"A").
has_category_B :- selected(S), set_category(S,"B").
has_category_C :- selected(S), set_category(S,"C").

% Calculate coverage: an element is covered if at least one set containing it is selected
covered(E) :- element(E), selected(S), set_elements(S,E).

% Ensure all elements are covered
:- element(E), not covered(E).

% Calculate redundancy: elements covered by more than 3 sets
% Count how many sets cover each element
num_covering_sets(E, N) :- element(E), N = #count { S : selected(S), set_elements(S,E) }.

% Mark elements as redundant if covered by >3 sets
redundant(E) :- num_covering_sets(E, N), N > 3.

% Calculate base cost
base_cost(C) :- C = #sum { Cost,S : selected(S), set_cost(S,Cost) }.

% Calculate penalty: 2 per redundant element
penalty(P) :- P = 2 * #count { E : redundant(E) }.

% Calculate total cost
total_cost(C) :- base_cost(Base), penalty(Pen), C = Base + Pen.

% Minimize total cost
#minimize { C : total_cost(C) }.

% Show the selected sets and total cost
#show selected/1.
#show total_cost/1.