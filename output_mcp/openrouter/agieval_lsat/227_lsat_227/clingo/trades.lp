% Buildings and classes
building(garza,1). building(yates,3). building(zimmer,3).
building(flores,1). building(lynch,2).
building(king,2). building(meyer,2). building(ortiz,2).

% Original owners
original_owner(garza,realprop). original_owner(yates,realprop). original_owner(zimmer,realprop).
original_owner(flores,southco). original_owner(lynch,southco).
original_owner(king,trustcorp). original_owner(meyer,trustcorp). original_owner(ortiz,trustcorp).

owner(realprop). owner(southco). owner(trustcorp).

% Final ownership: each building assigned to exactly one owner
1 { final_owner(B,O) : owner(O) } 1 :- building(B).

% Initial class counts per owner
init_cnt(O,C,N) :- owner(O), C=1..3, N = #count{ B : original_owner(B,O), building(B,C) }.

% Final class counts per owner
final_cnt(O,C,N) :- owner(O), C=1..3, N = #count{ B : final_owner(B,O), building(B,C) }.

% Numbers for trade counts (allow up to 5 trades per ordered pair)
num(0..5).

% Trade type2: one class1 for two class2 (direction A->B)
1 { trade2(A,B,N) : num(N) } 1 :- owner(A), owner(B), A != B.
% Trade type3: one class2 for two class3 (direction A->B)
1 { trade3(A,B,N) : num(N) } 1 :- owner(A), owner(B), A != B.

% Compute total out/in trades per owner for each type
out2(O,Sum) :- owner(O), Sum = #sum{ N : trade2(O,_,N) }.
in2(O,Sum)  :- owner(O), Sum = #sum{ N : trade2(_,O,N) }.
out3(O,Sum) :- owner(O), Sum = #sum{ N : trade3(O,_,N) }.
in3(O,Sum)  :- owner(O), Sum = #sum{ N : trade3(_,O,N) }.

% Balance constraints: final counts must equal initial plus net changes
% Class 1
:- init_cnt(O,1,Init), final_cnt(O,1,Final), out2(O,Out), in2(O,In), Final != Init - Out + In.
% Class 2
:- init_cnt(O,2,Init), final_cnt(O,2,Final), out2(O,Out2), in2(O,In2), out3(O,Out3), in3(O,In3), Final != Init + 2*Out2 - 2*In2 - Out3 + In3.
% Class 3
:- init_cnt(O,3,Init), final_cnt(O,3,Final), out3(O,Out3), in3(O,In3), Final != Init + 2*Out3 - 2*In3.

% Helper to detect extra buildings for an owner
extra(O) :- final_owner(B,O), not allowed_building(O,B).

% Allowed building sets per option
allowed_building(realprop,garza). allowed_building(realprop,flores). % A
allowed_building(southco,flores). allowed_building(southco,meyer). % B
allowed_building(southco,garza). allowed_building(southco,lynch). % C
allowed_building(trustcorp,flores). allowed_building(trustcorp,ortiz). % D
allowed_building(trustcorp,garza). allowed_building(trustcorp,meyer). % E

% Map each option to its owner
option_owner(a,realprop).
option_owner(b,southco).
option_owner(c,southco).
option_owner(d,trustcorp).
option_owner(e,trustcorp).

% Condition for each option
cond(O) :- option_owner(O,Owner), not extra(Owner),
          allowed_building(Owner,B1), final_owner(B1,Owner),
          allowed_building(Owner,B2), final_owner(B2,Owner), B1 != B2.

satisfied(O) :- cond(O).

% Maximize number of satisfied options (expect 4)
#maximize { 1,O : satisfied(O) }.

% The impossible option is the one not satisfied
option(O) :- option_owner(O,_), not satisfied(O).

% Ensure exactly one option is reported
:- #count{ O : option(O) } != 1.

#show option/1.