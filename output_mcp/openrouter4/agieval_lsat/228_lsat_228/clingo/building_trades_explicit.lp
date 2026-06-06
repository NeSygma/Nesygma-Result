%%% Model building trades with explicit trade sequence constraints.
%%% We need any number of trades (0 to max_trades) to reach the final state.

company(realprop; southco; trustcorp).

bldg(garza,1). bldg(yates,3). bldg(zimmer,3).
bldg(flores,1). bldg(lynch,2).
bldg(king,2). bldg(meyer,2). bldg(ortiz,2).

%%% Initial ownership
init_own(garza,realprop). init_own(yates,realprop). init_own(zimmer,realprop).
init_own(flores,southco). init_own(lynch,southco).
init_own(king,trustcorp). init_own(meyer,trustcorp). init_own(ortiz,trustcorp).

%%% Time horizon for trades
time(0..6).  %% allow up to 6 trades

%%% Ownership at each time point
1 { own(B, C, 0) : company(C) } 1 :- bldg(B, _), init_own(B, C).
%%% At time 0, ownership equals initial
:- own(B, C, 0), not init_own(B, C).

%%% Value per building
val(B, 4) :- bldg(B, 1).
val(B, 2) :- bldg(B, 2).
val(B, 1) :- bldg(B, 3).

%%% Trade happens between two companies at each time step
%%% Trade types:
%%% Type 1: 1-for-1 same class
%%% Type 2: 1 class 1 for 2 class 2
%%% Type 3: 1 class 2 for 2 class 3

%%% trade_type1(A, B, C1, C2, T): company C1 gives building A, company C2 gives building B, same class
%%% trade_type2(A, B1, B2, C1, C2, T): company C1 gives class1 A, company C2 gives class2 B1,B2
%%% trade_type3(A, B1, B2, C1, C2, T): company C1 gives class2 A, company C2 gives class3 B1,B2

%%% At most one trade per time step, between two different companies
{ trade_type1(B1, B2, C1, C2, T) : bldg(B1,Cl), bldg(B2,Cl), company(C1), company(C2), C1 != C2, own(B1,C1,T), own(B2,C2,T) } 1.
{ trade_type2(B1, B21, B22, C1, C2, T) : bldg(B1,1), bldg(B21,2), bldg(B22,2), B21 != B22, company(C1), company(C2), C1 != C2, own(B1,C1,T), own(B21,C2,T), own(B22,C2,T) } 1.
{ trade_type3(B1, B21, B22, C1, C2, T) : bldg(B1,2), bldg(B21,3), bldg(B22,3), B21 != B22, company(C1), company(C2), C1 != C2, own(B1,C1,T), own(B21,C2,T), own(B22,C2,T) } 1.

%%% At most one trade per time step
:- time(T), #count{T1,B21,B22,C1,C2 : trade_type1(_,B21,B22,C1,C2,T); T2,B1,B22,C1,C2 : trade_type2(B1,_,B22,C1,C2,T); T3,B1,B21,C1,C2 : trade_type3(B1,B21,_,C1,C2,T)} > 1.

%%% Effects: ownership at T+1
%%% If no trade, ownership persists (frame axiom)
own(B, C, T+1) :- own(B, C, T), time(T), time(T+1), not affected(B, T).

%%% Buildings affected by a trade at time T
affected(B, T) :- trade_type1(B, _, _, _, _, T).
affected(B, T) :- trade_type1(_, B, _, _, _, T).
affected(B, T) :- trade_type2(B, _, _, _, _, _, T).
affected(B, T) :- trade_type2(_, B, _, _, _, _, T).
affected(B, T) :- trade_type2(_, _, B, _, _, _, T).
affected(B, T) :- trade_type3(B, _, _, _, _, _, T).
affected(B, T) :- trade_type3(_, B, _, _, _, _, T).
affected(B, T) :- trade_type3(_, _, B, _, _, _, T).

%%% Type 1: C1 gives B1, C2 gives B2, same class
own(B2, C1, T+1) :- trade_type1(B1, B2, C1, C2, T).
own(B1, C2, T+1) :- trade_type1(B1, B2, C1, C2, T).

%%% Type 2: C1 gives class 1 B1 to C2, C2 gives class 2 B21,B22 to C1
own(B21, C1, T+1) :- trade_type2(B1, B21, B22, C1, C2, T).
own(B22, C1, T+1) :- trade_type2(B1, B21, B22, C1, C2, T).
own(B1, C2, T+1) :- trade_type2(B1, B21, B22, C1, C2, T).

%%% Type 3: C1 gives class 2 B1 to C2, C2 gives class 3 B21,B22 to C1
own(B21, C1, T+1) :- trade_type3(B1, B21, B22, C1, C2, T).
own(B22, C1, T+1) :- trade_type3(B1, B21, B22, C1, C2, T).
own(B1, C2, T+1) :- trade_type3(B1, B21, B22, C1, C2, T).

%%% Each building has exactly one owner at each time
:- own(B, C1, T), own(B, C2, T), C1 != C2.

%%% RealProp owns only class 2 at final time (max_time)
max_time = #max{T : time(T)}.
:- own(B, realprop, max_time), bldg(B, C), C != 2.

%%% At least one trade occurred
:- #count{T : trade_type1(_,_,_,_,_,T); trade_type2(_,_,_,_,_,_,T); trade_type3(_,_,_,_,_,_,T)} = 0.

%%% Check option (A): Trustcorp owns a class 1 building
trustcorp_has_c1 :- own(B, trustcorp, max_time), bldg(B, 1).

%%% Force option (A) to be false to see if it's possible
:- trustcorp_has_c1.

#show own/3.
#show trade_type1/6.
#show trade_type2/7.
#show trade_type3/7.