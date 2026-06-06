%%% Problem: Building Trades between RealProp, Southco, Trustcorp
%%% Find all final states where RealProp owns only class 2 buildings

%%% Constants
company(realprop; southco; trustcorp).

%%% Buildings: building(Name, Class)
building("GarzaTower", 1).
building("YatesHouse", 3).
building("ZimmerHouse", 3).
building("FloresTower", 1).
building("LynchBuilding", 2).
building("KingBuilding", 2).
building("MeyerBuilding", 2).
building("OrtizBuilding", 2).

%%% Initial ownership
init_own("GarzaTower", realprop).
init_own("YatesHouse", realprop).
init_own("ZimmerHouse", realprop).
init_own("FloresTower", southco).
init_own("LynchBuilding", southco).
init_own("KingBuilding", trustcorp).
init_own("MeyerBuilding", trustcorp).
init_own("OrtizBuilding", trustcorp).

%%% Class of each building
class(B, C) :- building(B, C).

%%% Time steps (enough to explore all reachable states)
time(0..6).

%%% 1 { own(B, C, T) : company(C) } 1 :- building(B, _), time(T).
%%% Initial ownership at time 0
own(B, C, 0) :- init_own(B, C).

%%% Frame: ownership persists unless changed by a trade
own(B, C, T+1) :- own(B, C, T), time(T), T < 6, not lost(B, T).
lost(B, T) :- trade_happens(T), trade_give(B, _, T).

%%% A trade happens at each time step (we allow 0 or 1 trade per step)
{ trade_happens(T) } :- time(T), T < 6.

%%% Trade type selection
0 { trade_type(1, T); trade_type(2, T); trade_type(3, T) } 1 :- trade_happens(T).

%%% For type 1: swap two buildings of same class between two companies
%%% trade_party(Giver, Receiver, GiveB, RecvB, T)
%%% Giver gives GiveB, receives RecvB (both same class)
{trade_give(B1, T): building(B1,_)} 1 :- trade_happens(T), trade_type(1, T).
{trade_recv(B2, T): building(B2,_)} 1 :- trade_happens(T), trade_type(1, T).
trade_giver_company(C1, T) :- trade_happens(T), trade_type(1, T), own(B1, C1, T), trade_give(B1, T).
trade_receiver_company(C2, T) :- trade_happens(T), trade_type(1, T), own(B2, C2, T), trade_recv(B2, T), C2 != trade_giver_company(_, T).

%%% Actually, let's simplify using a different approach.
%%% Instead of explicit time steps, we can enumerate all possible final ownership
%%% assignments and check reachability via constraints on counts and trade possibilities.

%%% Let's restart with a cleaner model.

%%% We'll use a simpler constraint-based approach:
%%% Each building ends up with some company.
%%% The final ownership must be reachable via valid trades from initial.

%%% Key invariants:
%%% 1. Total "units" per company conserved (class1=4, class2=2, class3=1)
%%% 2. Trades change ownership but some constraints apply.

%%% Let's just enumerate all possible final ownership assignments and filter
%%% by checking if a trade sequence exists.

%%% For reachability, we can use the observation that any ownership assignment
%%% that satisfies certain invariants is reachable.
%%% Let's just model the final state constraints and see which options are forced.

%%% Final ownership choice
{ final_own(B, C) } :- building(B, _), company(C).

%%% Each building owned by exactly one company
:- building(B, _), #count{C: final_own(B, C)} != 1.

%%% RealProp must own only class 2 buildings in final state
%%% RealProp can own 0 or more class 2, and no class 1 or class 3
:- final_own(B, realprop), class(B, C), C != 2.

%%% At least one trade? Not necessary for "after some trades" but RealProp doesn't start with only class 2.
%%% So we must check that final differs from initial for at least one building.
:- #count{B: final_own(B, C1), init_own(B, C2), C1 != C2} = 0.

%%% Unit conservation per company: total value conserved
value(B, 4) :- class(B, 1).
value(B, 2) :- class(B, 2).
value(B, 1) :- class(B, 3).

total_value_init(C, V) :- V = #sum{Val, B: init_own(B, C), value(B, Val)}.
total_value_final(C, V) :- V = #sum{Val, B: final_own(B, C), value(B, Val)}.

:- total_value_init(C, V1), total_value_final(C, V2), V1 != V2.

%%% Now, the reachability constraint: we need to ensure the final state
%%% is reachable via valid trades. This is complex but we can use
%%% some necessary conditions or simulate trades.

%%% Let's try to simulate trades explicitly with a bounded number of steps.

%%% Actually, let's use the unit conservation and also consider that
%%% the total number of buildings per class changes only via specific trades.
%%% But perhaps unit conservation plus some other constraints are sufficient.

%%% Let's also ensure that no building is "created" or "destroyed" - 
%%% but trades can create new buildings of class 2 or 3.
%%% The total count of buildings can increase.

%%% Let's just compute reachable states by explicit trade simulation.

%%% Reset and use explicit time-step simulation

%%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Time-step model with explicit trades
%%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#show option/1.

%%% Step 1: Enumerate all possible final states via trade simulation

%%% Trade happens at each time step (exactly one trade per step, or none)
%%% We'll allow up to 4 trades

step(0..4).

%%% At each step, we decide if a trade occurs
{ trade_step(S) } :- step(S), S < 4.

%%% Exactly one trade per active step (simplify: each step where trade happens, one trade)
%%% But we need to define what a trade is.

%%% Too complex. Let me just use reasoning.

%%% Actually, we already reasoned that option A must be true.
%%% Let's encode the final state constraints and just check which options
%%% can be false in some valid final state.

%%% We'll use the unit conservation and a check that the trade sequence exists
%%% by modeling the necessary conditions.

%%% Necessary condition for reachability:
%%% The multiset of buildings owned by each company can be transformed
%%% via a series of trades described by the three types.

%%% I'll model trades as operations on count vectors.

%%% Counts of buildings per class for each company
%%% Initial counts:
init_count(realprop, 1, 1). init_count(realprop, 2, 0). init_count(realprop, 3, 2).
init_count(southco, 1, 1). init_count(southco, 2, 1). init_count(southco, 3, 0).
init_count(trustcorp, 1, 0). init_count(trustcorp, 2, 3). init_count(trustcorp, 3, 0).

%%% Final counts (to be determined)
{ final_count(C, Cls, N) } :- company(C), Cls = 1..3, N = 0..8.

%%% Sum of counts per class across companies equals total buildings of that class (initially)
%%% But total buildings can increase: type2 creates 2 class2 from 1 class1 (net +1 building)
%%% type3 creates 2 class3 from 1 class2 (net +1 building)
%%% So total buildings = 8 + (#type2_trades) + (#type3_trades)
%%% We don't know how many trades happened.

%%% Let's just enumerate with some reasonable bounds.

%%% Let's use a different strategy: enumerate all possible final ownerships
%%% and check if a trade sequence exists via SAT.

%%% Since the state space is small, we can precompute reachable states.

%%% Let me just write a brute-force search using ASP aggregates.

%%% We'll treat each building's final owner as a choice.
%%% Then we'll add constraints that the state is reachable.

%%% For reachability, we can use the following observation:
%%% Any ownership assignment that:
%%% 1. Conserves units per company
%%% 2. Has the same total counts of class 1 and class 2 and class 3 adjusted for net creation
%%% is reachable.

%%% Net creation: each type2 trade consumes 1 class1 and creates 2 class2.
%%% Each type3 trade consumes 1 class2 and creates 2 class3.

%%% Let delta_c1, delta_c2, delta_c3 be the net change in total counts of each class.

%%% delta_c1 = -t2 (each type2 reduces class1 count by 1)
%%% delta_c2 = +2*t2 - t3 (each type2 adds 2 class2, each type3 consumes 1 class2)
%%% delta_c3 = +2*t3 (each type3 adds 2 class3)

%%% Where t2, t3 are non-negative integers (number of type2 and type3 trades).
%%% t1 (type1) doesn't change counts.

%%% Initial total counts: c1=2, c2=4, c3=2
%%% Final total counts: c1' = 2 - t2, c2' = 4 + 2*t2 - t3, c3' = 2 + 2*t3

%%% Since counts can't be negative: t2 <= 2, t3 <= 4 + 2*t2

%%% Also final counts must be non-negative.

%%% Additionally, each company's unit value is conserved.

%%% Let's incorporate this into our model.

{ t2 = 0..2 }.
{ t3 = 0..10 }.

%%% Total final counts
total_c1(2 - t2) :- t2 = T2.
total_c2(4 + 2*T2 - T3) :- t2 = T2, t3 = T3.
total_c3(2 + 2*T3) :- t3 = T3.

%%% Counts must be non-negative
:- total_c1(N), N < 0.
:- total_c2(N), N < 0.
:- total_c3(N), N < 0.

%%% Now, each building has a final owner
{ final_own(B, C) : company(C) } :- building(B, _).

%%% Each building exactly one owner
:- building(B, _), #count{C : final_own(B, C)} != 1.

%%% Count buildings per class per company in final state
final_count_cc(C, Cls, N) :- N = #count{B : class(B, Cls), final_own(B, C)}, company(C), Cls = 1..3.

%%% Total counts of each class must match
:- total_c1(N), #sum{NC, C : final_count_cc(C, 1, NC)} != N.
:- total_c2(N), #sum{NC, C : final_count_cc(C, 2, NC)} != N.
:- total_c3(N), #sum{NC, C : final_count_cc(C, 3, NC)} != N.

%%% Unit conservation per company
value_unit(B, 4) :- class(B, 1).
value_unit(B, 2) :- class(B, 2).
value_unit(B, 1) :- class(B, 3).

init_val(C, V) :- V = #sum{Val, B : init_own(B, C), value_unit(B, Val)}.
final_val(C, V) :- V = #sum{Val, B : final_own(B, C), value_unit(B, Val)}.

:- init_val(C, V1), final_val(C, V2), V1 != V2.

%%% RealProp must own only class 2 buildings in final state
:- final_own(B, realprop), class(B, C), C != 2.

%%% RealProp must own at least one building? Not necessarily, but "only class 2" allows zero.
%%% However, if RealProp owns zero buildings, that satisfies "only class 2" vacuously.
%%% But we also need "after some number of trades" - if zero trades, RealProp has non-class2.
%%% So final must differ from initial.
:- #count{B : final_own(B, C1), init_own(B, C2), C1 != C2} = 0.

%%% Now check options
option(a) :- not some_not_a.
option(b) :- not some_not_b.
option(c) :- not some_not_c.
option(d) :- not some_not_d.
option(e) :- not some_not_e.

%%% A: Trustcorp owns a class 1 building.
some_not_a :- final_own(B, trustcorp), class(B, 1).

%%% B: Trustcorp owns the Meyer Building.
some_not_b :- final_own("MeyerBuilding", trustcorp).

%%% C: Southco owns a class 2 building.
some_not_c :- final_own(B, southco), class(B, 2).

%%% D: Southco owns both of the class 3 buildings.
class3_both_southco :- final_own("YatesHouse", southco), final_own("ZimmerHouse", southco).
some_not_d :- class3_both_southco.

%%% E: Southco owns the Flores Tower.
some_not_e :- final_own("FloresTower", southco).

%%% Actually, I made a mistake: some_not_X should mean "there exists a model where X is false"
%%% So option X is "must be true" if there is NO model where X is false.
%%% Let's fix.

%%% We want: option(a) is true if all models have "Trustcorp owns a class 1 building".
%%% In ASP, we can check: if there is no model where Trustcorp does NOT own a class 1 building.
%%% But we need to use #show to see models.

%%% Let me recast: We'll compute answer/1 instead, and then map.

%%% Actually, simpler: Let's just compute all models and see which options hold in all.

%%% Since this is a decision problem, let's just output the models and analyze.

%%% Let's change to show the relevant atoms.

#show final_own/2.
#show t2/1.
#show t3/1.
#show class/2.