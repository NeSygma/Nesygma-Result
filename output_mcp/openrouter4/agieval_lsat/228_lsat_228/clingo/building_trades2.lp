%%% Model: Building trades between RealProp, Southco, Trustcorp
%%% Goal: Find what MUST be true when RealProp owns only class 2 buildings

%%% Companies
company(realprop; southco; trustcorp).

%%% Buildings with classes
bldg(garza,1). bldg(yates,3). bldg(zimmer,3).
bldg(flores,1). bldg(lynch,2).
bldg(king,2). bldg(meyer,2). bldg(ortiz,2).

%%% Initial ownership
init_own(garza,realprop). init_own(yates,realprop). init_own(zimmer,realprop).
init_own(flores,southco). init_own(lynch,southco).
init_own(king,trustcorp). init_own(meyer,trustcorp). init_own(ortiz,trustcorp).

%%% Each building has exactly one final owner (chosen freely)
{ final_own(B, C) : company(C) } :- bldg(B, _).

%%% Exactly one owner per building
:- bldg(B, _), #count{C : final_own(B, C)} != 1.

%%% Class of building
class(B, Cls) :- bldg(B, Cls).

%%% Value per building (class1=4, class2=2, class3=1)
val(B, 4) :- class(B, 1).
val(B, 2) :- class(B, 2).
val(B, 1) :- class(B, 3).

%%% Total value per company (initial and final)
init_val(C, V) :- V = #sum{Val, B : init_own(B, C), val(B, Val)}, company(C).
final_val(C, V) :- V = #sum{Val, B : final_own(B, C), val(B, Val)}, company(C).

%%% Value conservation per company
:- init_val(C, V1), final_val(C, V2), V1 != V2.

%%% Total counts of each class initially
total_init(1, 2). total_init(2, 4). total_init(3, 2).

%%% Number of type2 and type3 trades (non-negative integers)
{ t2 = 0..2 }.
{ t3 = 0..6 }.

%%% Final total counts
total_final(1, 2 - T2) :- t2 = T2.
total_final(2, 4 + 2*T2 - T3) :- t2 = T2, t3 = T3.
total_final(3, 2 + 2*T3) :- t3 = T3.

%%% Counts must be non-negative
:- total_final(_, N), N < 0.

%%% Count of buildings per class in final state
final_count(Cls, N) :- N = #count{B : class(B, Cls), final_own(B, _)}, Cls = 1..3.

%%% Must match expected totals
:- total_final(Cls, Expected), final_count(Cls, Actual), Actual != Expected.

%%% RealProp owns only class 2 buildings in final state
:- final_own(B, realprop), class(B, C), C != 2.

%%% At least one building changed ownership (otherwise trivial, not matching "after some trades")
:- #count{B : final_own(B, C1), init_own(B, C2), C1 != C2} = 0.

%%% Now we want to check each option.
%%% Since we can't enumerate all models, we use a trick:
%%% For each option X, we ask: is there a model where X is false?
%%% We'll compute answer sets for each query.

%%% Let's directly test each option by adding a constraint
%%% that the option is false, and see if SAT or UNSAT.

%%% We'll do this in separate runs.

%%% For now, let's just output all models and see.

#show final_own/2.
#show t2/1.
#show t3/1.