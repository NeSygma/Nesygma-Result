%%% Model: Building trades between RealProp, Southco, Trustcorp
%%% Check if Trustcorp must own a class 1 building

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

%%% Final ownership: exactly one owner per building
1 { final_own(B, C) : company(C) } 1 :- bldg(B, _).

%%% Value per building (class1=4, class2=2, class3=1)
val(B, 4) :- bldg(B, 1).
val(B, 2) :- bldg(B, 2).
val(B, 1) :- bldg(B, 3).

%%% Total value per company must be preserved
init_val(C, V) :- V = #sum{Val, B : init_own(B, C), val(B, Val)}, company(C).
final_val(C, V) :- V = #sum{Val, B : final_own(B, C), val(B, Val)}, company(C).
:- init_val(C, V1), final_val(C, V2), V1 != V2.

%%% RealProp owns only class 2 buildings in final state
:- final_own(B, realprop), bldg(B, C), C != 2.

%%% At least one trade occurred
:- #count{B : final_own(B, C1), init_own(B, C2), C1 != C2} = 0.

%%% Check if option (A) can be false: Trustcorp owns NO class 1 building
:- not final_own(_, trustcorp), bldg(_, 1).  % This is wrong syntax
%%% Actually: constraint that Trustcorp does NOT own a class 1 building
no_c1_trustcorp :- #count{B : final_own(B, trustcorp), bldg(B, 1)} = 0.
:- no_c1_trustcorp.

#show final_own/2.