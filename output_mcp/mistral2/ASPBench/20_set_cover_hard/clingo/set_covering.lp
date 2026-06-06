% --- Domains ---
element(1..20).
set(0..13).

% --- Set Properties ---
set_cost(0,1). set_cost(1,1). set_cost(2,1). set_cost(3,1). set_cost(4,1). set_cost(5,1).
set_cost(6,1). set_cost(7,1). set_cost(8,1). set_cost(9,4). set_cost(10,4). set_cost(11,4).
set_cost(12,4). set_cost(13,4).

set_category(0,"A"). set_category(1,"A"). set_category(2,"A").
set_category(3,"B"). set_category(4,"B"). set_category(5,"B").
set_category(6,"C"). set_category(7,"C"). set_category(8,"C").
set_category(9,"specialized"). set_category(10,"specialized"). set_category(11,"specialized").
set_category(12,"specialized"). set_category(13,"specialized").

% Set elements as facts
set_element(0,1). set_element(0,2). set_element(0,3). set_element(0,4). set_element(0,5).
set_element(1,1). set_element(1,6). set_element(1,11). set_element(1,16).
set_element(2,2). set_element(2,7). set_element(2,12). set_element(2,17).
set_element(3,3). set_element(3,8). set_element(3,13). set_element(3,18).
set_element(4,4). set_element(4,9). set_element(4,14). set_element(4,19).
set_element(5,5). set_element(5,10). set_element(5,15). set_element(5,20).
set_element(6,6). set_element(6,7). set_element(6,8). set_element(6,9). set_element(6,10).
set_element(7,1). set_element(7,3). set_element(7,5). set_element(7,7). set_element(7,9).
set_element(8,2). set_element(8,4). set_element(8,6). set_element(8,8). set_element(8,10).
set_element(9,1). set_element(9,2). set_element(9,3). set_element(9,4). set_element(9,5). set_element(9,6). set_element(9,7).
set_element(10,11). set_element(10,12). set_element(10,13). set_element(10,14). set_element(10,15).
set_element(11,8). set_element(11,9). set_element(11,10).
set_element(12,1). set_element(12,5). set_element(12,10). set_element(12,15).
set_element(13,16). set_element(13,17). set_element(13,18). set_element(13,19). set_element(13,20).

% Prerequisites
requires(9,0).
requires(11,6).

% Mutual exclusion
mutex(12,13).

% Standard categories
standard_category("A").
standard_category("B").
standard_category("C").

% --- Choice Rule ---
{ selected(S) : set(S) }.

% --- Coverage ---
covered(E) :- element(E), selected(S), set_element(S,E).

% --- Ensure all elements are covered ---
:- element(E), not covered(E).

% --- Cover count for redundancy penalty ---
1 { cover_count(E,1) ; cover_count(E,2) ; cover_count(E,3) ; cover_count(E,4..20) } 1 :- element(E), selected(S), set_element(S,E).

% --- Prerequisites ---
:- selected(S1), requires(S1, S2), not selected(S2).

% --- Mutual Exclusion ---
:- selected(S1), selected(S2), mutex(S1, S2).

% --- Category Balancing ---
has_category(C) :- set_category(S, C), standard_category(C), selected(S).
:- selected(S), set_category(S, "specialized"), not has_category("A").
:- selected(S), set_category(S, "specialized"), not has_category("B").
:- selected(S), set_category(S, "specialized"), not has_category("C").

% --- Redundancy Penalty ---
redundancy_penalty(R) :- R = 2 * (#count{ E : element(E), cover_count(E,N), N > 3 }).

% --- Base Cost ---
base_cost(B) :- B = #sum{ Cost, S : selected(S), set_cost(S, Cost) }.

% --- Total Cost ---
total_cost(T) :- base_cost(B), redundancy_penalty(R), T = B + R.

% --- Objective ---
#minimize{ T : total_cost(T) }.

% --- Show ---
#show selected/1.
#show total_cost/1.
#show base_cost/1.
#show redundancy_penalty/1.