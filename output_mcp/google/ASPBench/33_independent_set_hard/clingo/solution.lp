% --- Domain Definitions ---
vertex(1..24).
zone(1, 1..8).
zone(2, 9..16).
zone(3, 17..24).

type(1, core). type(9, core). type(17, core).
type(2, support). type(3, support). type(10, support). type(11, support). type(18, support). type(19, support).
type(V, peripheral) :- vertex(V), not type(V, core), not type(V, support).

edge(1,2). edge(1,4). edge(1,10). edge(1,17). edge(2,5). edge(2,9). edge(3,6). edge(4,7). edge(5,8). edge(6,7). edge(8,16). edge(8,24). edge(9,10). edge(9,12). edge(9,17). edge(10,14). edge(11,15). edge(12,16). edge(13,14). edge(16,24). edge(17,18). edge(17,20). edge(18,19). edge(18,21). edge(19,22). edge(20,23). edge(21,24).
edge(Y, X) :- edge(X, Y).

% --- Decision Variables ---
{ in_set(V) } :- vertex(V).

% --- Constraints ---
% 1. Standard Independence
:- in_set(X), in_set(Y), edge(X, Y).

% 2. Core Count Limit
core_count(N) :- N = #count { V : in_set(V), type(V, core) }.
:- core_count(N), N > 2.

% 3. Core-Support Dependency
has_support_in_zone(Z) :- in_set(S), type(S, support), zone(Z, S).
:- in_set(C), type(C, core), zone(Z, C), not has_support_in_zone(Z).

% 4. Conditional Zone Exclusion
has_peripheral_z1 :- in_set(V), type(V, peripheral), zone(1, V).
:- has_peripheral_z1, in_set(V), zone(3, V).

% 5. Peripheral Headcount Rule
peripheral_count(N) :- N = #count { V : in_set(V), type(V, peripheral) }.
:- peripheral_count(P), core_count(C), P > C.

% --- Objective ---
support_count(N) :- N = #count { V : in_set(V), type(V, support) }.
size(N) :- N = #count { V : in_set(V) }.
#maximize { N : size(N) }.

% --- Output ---
#show in_set/1.
#show size/1.
#show core_count/1.
#show support_count/1.
#show peripheral_count/1.