%% Problem: Trading buildings among RealProp, Southco, Trustcorp
%% Each trade: (1) 1-for-1 same class, (2) 1 class1 for 2 class2, (3) 1 class2 for 2 class3
%% Initial ownership:
%% RealProp: Garza (class1), Yates (class3), Zimmer (class3)
%% Southco: Flores (class1), Lynch (class2)
%% Trustcorp: King (class2), Meyer (class2), Ortiz (class2)

%% We need to determine which of the given ownership scenarios is IMPOSSIBLE
%% no matter how many trades are made.

%% Approach: Model the state space of possible ownership configurations reachable
%% via valid trades. Since trades are reversible (1-for-1 same class is symmetric,
%% and the other trades have inverses), we can think in terms of invariants.

%% Key insight: The total "value" in each class can change via trades.
%% Let's track the number of buildings of each class owned by each company.
%% Trades:
%% Type 1: (c1,c1) -> (c1,c1)  [swap same class, no net change]
%% Type 2: 1 c1 -> 2 c2  [c1: -1, c2: +2]
%% Type 3: 1 c2 -> 2 c3  [c2: -1, c3: +2]
%% Inverse of type 2: 2 c2 -> 1 c1  [c1: +1, c2: -2]
%% Inverse of type 3: 2 c3 -> 1 c2  [c2: +1, c3: -2]

%% So the reachable states are those where certain invariants hold.
%% Let's compute the initial counts per company.

%% Initial counts:
%% RealProp: c1=1 (Garza), c2=0, c3=2 (Yates, Zimmer)
%% Southco: c1=1 (Flores), c2=1 (Lynch), c3=0
%% Trustcorp: c1=0, c2=3 (King, Meyer, Ortiz), c3=0

%% Total: c1=2, c2=4, c3=2

%% Let's model the problem directly by exploring reachable states.
%% We'll use a state-space search with bounded trades.

%% Domain
company(realprop; southco; trustcorp).
class(1;2;3).

%% Initial state
init_owns(realprop, 1, 1).  % Garza
init_owns(realprop, 3, 2).  % Yates, Zimmer
init_owns(southco, 1, 1).   % Flores
init_owns(southco, 2, 1).   % Lynch
init_owns(trustcorp, 2, 3). % King, Meyer, Ortiz

%% Total buildings per class (invariant: total count of buildings is fixed)
total_class(1, 2).
total_class(2, 4).
total_class(3, 2).

%% Total buildings = 2+4+2 = 8

%% We'll model reachable states via constraints on what's possible.
%% Key invariants:
%% Let c1_r, c2_r, c3_r be counts for RealProp, etc.
%% Total per class is fixed.
%% Trades change counts but preserve certain linear combinations.

%% Let's think about what linear combinations are invariant.
%% Trade type 2: (c1: -1, c2: +2)  -> vector v2 = (-1, 2, 0)
%% Trade type 3: (c2: -1, c3: +2)  -> vector v3 = (0, -1, 2)
%% Inverse type 2: (c1: +1, c2: -2) -> -v2
%% Inverse type 3: (c2: +1, c3: -2) -> -v3

%% Invariants: find vectors w such that w·v2 = 0 and w·v3 = 0
%% w = (w1, w2, w3)
%% w·v2 = -w1 + 2*w2 = 0  => w1 = 2*w2
%% w·v3 = -w2 + 2*w3 = 0  => w2 = 2*w3
%% So w1 = 4*w3, w2 = 2*w3. Let w3=1: w = (4, 2, 1)
%% So 4*c1 + 2*c2 + c3 is invariant for each company!

%% Check: initial values
%% RealProp: 4*1 + 2*0 + 2 = 6
%% Southco: 4*1 + 2*1 + 0 = 6
%% Trustcorp: 4*0 + 2*3 + 0 = 6

%% So each company always has invariant = 6.
%% Also total buildings per company can vary.

%% Let's verify: each company's invariant = 4*c1 + 2*c2 + c3 = 6

%% Now let's check each option.

%% Option A: RealProp owns Flores (c1) and Garza (c1)
%% RealProp: c1=2, c2=0, c3=0. Invariant = 4*2 + 2*0 + 0 = 8. Not 6. IMPOSSIBLE.

%% Option B: Southco owns Flores (c1) and Meyer (c2)
%% Southco: c1=1, c2=1, c3=0. Invariant = 4*1 + 2*1 + 0 = 6. OK.
%% But wait - Southco has 2 buildings. Total buildings for Southco = 2.
%% Initially Southco had 2 buildings. Can Southco have exactly 2 buildings?
%% Let's check: total buildings = 8. If Southco has 2, the other two have 6.
%% RealProp initially has 3, Trustcorp has 3. Total 8.
%% Possible? Let's check if there's a reachable state.

%% Option C: Southco owns Garza (c1) and Lynch (c2)
%% Southco: c1=1, c2=1, c3=0. Invariant = 6. OK. 2 buildings.

%% Option D: Trustcorp owns Flores (c1) and Ortiz (c2)
%% Trustcorp: c1=1, c2=1, c3=0. Invariant = 6. OK. 2 buildings.

%% Option E: Trustcorp owns Garza (c1) and Meyer (c2)
%% Trustcorp: c1=1, c2=1, c3=0. Invariant = 6. OK. 2 buildings.

%% So only option A violates the invariant. But let's double-check by
%% actually modeling the reachable states to be sure.

%% Let's model the state space more carefully.
%% Each company has counts (c1, c2, c3) summing to some total.
%% Total buildings = 8.
%% Each company's invariant = 4*c1 + 2*c2 + c3 = 6.

%% Let's enumerate all possible (c1,c2,c3) for a company satisfying:
%% 4*c1 + 2*c2 + c3 = 6, c1,c2,c3 >= 0 integers.

%% c1=0: 2*c2 + c3 = 6. Solutions: (0,0,6), (0,1,4), (0,2,2), (0,3,0)
%% c1=1: 4 + 2*c2 + c3 = 6 => 2*c2 + c3 = 2. Solutions: (1,0,2), (1,1,0)
%% c1=2: 8 + 2*c2 + c3 = 6 => 2*c2 + c3 = -2. No solutions.
%% So possible (c1,c2,c3) per company: 
%% (0,0,6), (0,1,4), (0,2,2), (0,3,0), (1,0,2), (1,1,0)

%% Now, total across all 3 companies: sum c1 = 2, sum c2 = 4, sum c3 = 2.

%% Let's enumerate all possible assignments to verify option A is impossible.

%% We'll use ASP to enumerate reachable states.

%% Domain of possible count vectors for a company
count_vec(0,0,6). count_vec(0,1,4). count_vec(0,2,2). count_vec(0,3,0).
count_vec(1,0,2). count_vec(1,1,0).

%% Each company gets exactly one count vector
1 { state(C, C1, C2, C3) : count_vec(C1, C2, C3) } 1 :- company(C).

%% Total counts must match
:- state(_, C1, C2, C3), #sum { C1, C : state(C, C1, _, _) } != 2.
:- state(_, C1, C2, C3), #sum { C2, C : state(C, _, C2, _) } != 4.
:- state(_, C1, C2, C3), #sum { C3, C : state(C, _, _, C3) } != 2.

%% Now check each option

%% Option A: RealProp owns Flores (c1) and Garza (c1)
%% RealProp has c1=2, c2=0, c3=0. But (2,0,0) is not a valid count vector.
%% So option A is impossible. Let's verify by checking if state(realprop,2,0,0) is possible.
impossible_a :- state(realprop, 2, 0, 0).

%% Option B: Southco owns Flores (c1) and Meyer (c2)
%% Southco has c1=1, c2=1, c3=0. That's (1,1,0) which is valid.
%% But we also need to check that the specific buildings match.
%% Flores is class 1, Meyer is class 2. So Southco has 1 class1 and 1 class2.
%% That's consistent with (1,1,0).

%% Option C: Southco owns Garza (c1) and Lynch (c2)
%% Southco has c1=1, c2=1, c3=0. Same as B.

%% Option D: Trustcorp owns Flores (c1) and Ortiz (c2)
%% Trustcorp has c1=1, c2=1, c3=0. Same.

%% Option E: Trustcorp owns Garza (c1) and Meyer (c2)
%% Trustcorp has c1=1, c2=1, c3=0. Same.

%% So option A is the only one that's impossible based on the invariant.
%% But let's also verify that options B-E are actually reachable.

%% Let's check if there exists a state satisfying each option.

%% For option B: Southco has (1,1,0)
possible_b :- state(southco, 1, 1, 0).

%% For option C: Southco has (1,1,0) - same count
possible_c :- state(southco, 1, 1, 0).

%% For option D: Trustcorp has (1,1,0)
possible_d :- state(trustcorp, 1, 1, 0).

%% For option E: Trustcorp has (1,1,0)
possible_e :- state(trustcorp, 1, 1, 0).

%% Now, we need to determine which option CANNOT be true.
%% Option A is impossible because (2,0,0) is not a valid count vector.
%% But let's also check if options B-E are all possible.

%% Let's find all valid states and see which options are satisfiable.

%% We'll derive which options are possible
option_possible(a) :- not impossible_a.
option_possible(b) :- possible_b.
option_possible(c) :- possible_c.
option_possible(d) :- possible_d.
option_possible(e) :- possible_e.

%% The answer is the option that is NOT possible
impossible_option(X) :- option(X), not option_possible(X).

%% Map to answer
option(a) :- impossible_option(a).
option(b) :- impossible_option(b).
option(c) :- impossible_option(c).
option(d) :- impossible_option(d).
option(e) :- impossible_option(e).

#show option/1.
#show state/4.
#show impossible_option/1.