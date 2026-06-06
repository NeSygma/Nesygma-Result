%%% BUILDING TRADES PROBLEM %%%

% --- OBJECTS ---
% Buildings
building(f).  % Flores Tower (class 1)
building(g).  % Garza Tower (class 1)
building(y).  % Yates House (class 3)
building(z).  % Zimmer House (class 3)
building(l).  % Lynch Building (class 2)
building(k).  % King Building (class 2)
building(m).  % Meyer Building (class 2)
building(o).  % Ortiz Building (class 2)

% Companies
company(r).  % RealProp
company(s).  % Southco
company(t).  % Trustcorp

% Classes
class(1). class(2). class(3).

% Building class
cls(f,1). cls(g,1).
cls(l,2). cls(k,2). cls(m,2). cls(o,2).
cls(y,3). cls(z,3).

% Class value (approximate value for counting)
% class 1 = 4, class 2 = 2, class 3 = 1
val(1,4). val(2,2). val(3,1).

% Initial ownership
init(r,g). init(r,y). init(r,z).  % RealProp: Garza, Yates, Zimmer
init(s,f). init(s,l).              % Southco: Flores, Lynch
init(t,k). init(t,m). init(t,o).   % Trustcorp: King, Meyer, Ortiz

% --- TRADE HORIZON ---
time(0..10).

% --- STATE: own(Building, Company, Time) ---

% Initial state: own(B,C,0) iff init(C,B)
own(B,C,0) :- building(B), company(C), init(C,B).

% Choice: at each time, a trade can happen
% A trade involves a company giving away some buildings and receiving others
% Trade types:
% Type 1: 1 building <-> 1 building of same class
% Type 2: 1 class-1 building <-> 2 class-2 buildings
% Type 3: 1 class-2 building <-> 2 class-3 buildings

% We model trades as: trade_from(C1, B1, C2, B2, T) means C1 gives B1 to C2 and receives B2 at time T
% But this is complex. Better: use exchange of buildings.

% Simplify: use trade(A_gives, B_gives, B_receives, T) where A gives B_gives and receives B_receives
% But we need multiple buildings on one side.

% Better approach: model each trade as a set of transfers.
% Trade type 1: one building changes owner with another (swap)
% Trade type 2: one class-1 goes from A to B, and two class-2s go from B to A
% Trade type 3: one class-2 goes from A to B, and two class-3s go from B to A

% Let's use: trade(T, Giver, Receiver, B_given, B_received) for simple 1-1 trades
% and use multiple predicates for multi-building trades.

% Actually, let's use a different modeling approach.
% A trade is an ordered action where at time T:
% - Company C1 gives building(s) X to company C2
% - Company C2 gives building(s) Y to company C1

% Represent as: exchange(C1, X, C2, Y, T) where X and Y can be lists/tuples.
% In ASP, use: exchange(C1, C2, T, B1, B2) for 1-1 trades.
% For 1-2 trades, use: exchange2(C1, B1, C2, B21, B22, T) etc.

% This is getting complicated. Let me use a different approach.

% --- SIMPLER APPROACH: Reachability via ownership sets ---
% Instead of modeling trades step by step, check if a target ownership configuration
% is reachable through valid trades.

% A trade is valid if:
% Type 1: Swap buildings of same class between two companies
% Type 2: Company A gives a class-1 to Company B, receives two class-2 from B
% Type 3: Company A gives a class-2 to Company B, receives two class-3 from B

% Ownership is a partition of buildings among companies.
% A configuration change (C1 -> C2) is valid if there's a trade.

% Instead of explicit time steps, model the final ownership and check
% if there's a sequence of trades. But this is hard in ASP.

% Let's use the "trading network" approach:
% Since trades are reversible (type 1 is symmetric, types 2/3 have inverses),
% we can think of which buildings end up with which companies,
% constrained by trade possibilities.

% Actually, a simpler insight: 
% The total "value" of buildings each company owns can change only via trades.
% Type 1: values unchanged for both.
% Type 2: A loses 4, gains 2+2=4. B loses 2+2=4, gains 4. (net zero)
% Type 3: A loses 2, gains 1+1=2. B loses 1+1=2, gains 2. (net zero)
% So total value per company is INVARIANT under trades!

% RealProp initial value: g(4) + y(1) + z(1) = 6
% Southco initial value: f(4) + l(2) = 6
% Trustcorp initial value: k(2) + m(2) + o(2) = 6

% Each company has total value 6, and this cannot change via trades!

% Now check each option:

% Option A: RealProp owns Flores Tower (4) and Garza Tower (4) = 8 ≠ 6. IMPOSSIBLE!

% Option B: Southco owns Flores Tower (4) and Meyer Building (2) = 6. Possible?
% Option C: Southco owns Garza Tower (4) and Lynch Building (2) = 6. Possible?
% Option D: Trustcorp owns Flores Tower (4) and Ortiz Building (2) = 6. Possible?
% Option E: Trustcorp owns Garza Tower (4) and Meyer Building (2) = 6. Possible?

% So option A is impossible due to value invariance!

% Let me verify this logic is correct.

% --- VALUE INVARIANCE CHECK ---

% Each building has a "value weight":
bval(f,4). bval(g,4).  % class 1
bval(l,2). bval(k,2). bval(m,2). bval(o,2).  % class 2
bval(y,1). bval(z,1).  % class 3

% Total value for a company in a given ownership configuration
tot_val(C, V) :- company(C), V = #sum{W, B : own(B,C), bval(B,W)}.

% Initial ownership values
init_val(C, V) :- company(C), V = #sum{W, B : init(C,B), bval(B,W)}.

% Check: init_val(r)=6, init_val(s)=6, init_val(t)=6
% test_init :- init_val(r,6), init_val(s,6), init_val(t,6).

% A trade must preserve each company's total value
% Types 1, 2, 3 all preserve value

% Therefore the value of each company is invariant

% Define target ownership for each option
% Option A: RealProp owns Flores Tower and Garza Tower
option_owns(a, f, r). option_owns(a, g, r).
% The remaining buildings must go to Southco or Trustcorp, but we need to check
% if RealProp's value is 6.

% Let's define target value for RealProp for each option

% Option A: RealProp has f(4)+g(4)=8
target_val(a, r, 8).

% Option B: Southco has f(4)+m(2)=6
target_val(b, s, 6).

% Option C: Southco has g(4)+l(2)=6
target_val(c, s, 6).

% Option D: Trustcorp has f(4)+o(2)=6
target_val(d, t, 6).

% Option E: Trustcorp has g(4)+m(2)=6
target_val(e, t, 6).

% An option is impossible if target value ≠ initial value
impossible(O) :- target_val(O, C, V), init_val(C, V0), V != V0.

% Map to answer
option(a) :- impossible(a).
option(b) :- not impossible(b).
option(c) :- not impossible(c).
option(d) :- not impossible(d).
option(e) :- not impossible(e).

% But wait - the question asks "which CANNOT be true"
% So we need the option that cannot be true.
% If option A is impossible, it's the answer.

% Let me double-check: is value truly invariant?
% Type 1: swap same class - obviously same value
% Type 2: one class-1 (value 4) for two class-2 (value 2+2=4) - same value
% Type 3: one class-2 (value 2) for two class-3 (value 1+1=2) - same value
% Yes, value is invariant.

% Also verify initial values:
% RealProp: Garza(4) + Yates(1) + Zimmer(1) = 6
% Southco: Flores(4) + Lynch(2) = 6
% Trustcorp: King(2) + Meyer(2) + Ortiz(2) = 6
% Yes, all 6.

% Option A gives RealProp: Flores(4) + Garza(4) = 8. Not 6. IMPOSSIBLE.
% Therefore A cannot be true.

#show impossible/1.
#show option/1.