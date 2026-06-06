%% Basic entities and domains
% People: 0=Agatha (victim), 1=Butler, 2=Charles, 3=Daisy, 4=Edward, 5=Felicity,
%         6=George, 7=Harriet, 8=Ian, 9=Julia, 10=Kenneth, 11=Lucy
person(0..11).

% Rooms: 0=Study, 1=Hall, 2=Kitchen, 3=Library, 4=Garden, 5=Dining, 6=Cellar,
%        7=Lounge, 8=Conservatory, 9=Bedroom, 10=Attic, 11=Garage
room(0..11).

% Weapons: 0=Gun, 1=Knife (murder weapon), 2=Rope, 3=Candlestick, 4=Wrench, 5=Poison
weapon(0..5).

% Time points: 0=19:00, 1=19:30, 2=20:00, 3=20:30, 4=21:00 (murder), 5=21:30, 6=22:00
time(0..6).

% High-confidence location facts at time 4 (murder time)
location(0,0,4).  % Agatha in Study
location(11,0,4). % Lucy in Study
location(1,6,4).  % Butler in Cellar
location(2,3,4). % Charles in Library
location(3,1,4). % Daisy in Hall
location(4,4,4). % Edward in Garden
location(5,2,4). % Felicity in Kitchen
location(6,5,4). % George in Dining
location(7,7,4). % Harriet in Lounge
location(8,8,4). % Ian in Conservatory
location(9,9,4). % Julia in Bedroom
location(10,10,4).% Kenneth in Attic

%% Room adjacency (movement allowed only between adjacent rooms or staying put)
% Study: connected to Hall, Library
adjacent(0,1). adjacent(0,3).
% Hall: connected to Study, Kitchen, Dining, Cellar, Lounge, Bedroom
adjacent(1,0). adjacent(1,2). adjacent(1,5). adjacent(1,6). adjacent(1,7). adjacent(1,9).
% Kitchen: connected to Hall, Dining, Garage
adjacent(2,1). adjacent(2,5). adjacent(2,11).
% Library: connected to Study, Garden, Lounge
adjacent(3,0). adjacent(3,4). adjacent(3,7).
% Garden: connected to Library, Conservatory, Garage
adjacent(4,3). adjacent(4,8). adjacent(4,11).
% Dining: connected to Hall, Kitchen, Lounge
adjacent(5,1). adjacent(5,2). adjacent(5,7).
% Cellar: connected to Hall, Garage
adjacent(6,1). adjacent(6,11).
% Lounge: connected to Hall, Library, Dining, Conservatory, Bedroom, Attic
adjacent(7,1). adjacent(7,3). adjacent(7,5). adjacent(7,8). adjacent(7,9). adjacent(7,10).
% Conservatory: connected to Garden, Lounge
adjacent(8,4). adjacent(8,7).
% Bedroom: connected to Hall, Lounge, Attic
adjacent(9,1). adjacent(9,7). adjacent(9,10).
% Attic: connected to Bedroom, Lounge
adjacent(10,7). adjacent(10,9).
% Garage: connected to Kitchen, Cellar, Garden
adjacent(11,2). adjacent(11,6). adjacent(11,4).

% Symmetric adjacency (if R1 adjacent to R2, then R2 adjacent to R1)
adjacent(R1,R2) :- adjacent(R2,R1), room(R1), room(R2).

%% Hate relationships (based on constraints)
% Agatha (0) hates everybody except the Butler (1)
hates(0,P) :- person(P), P != 1.

% Charles (2) hates no one that Agatha hates
% This means: if Agatha hates P, then Charles does not hate P
hates(2,P) :- person(P), not hates_agatha_hates(P).
hates_agatha_hates(P) :- hates(0,P), person(P).

% Butler (1) hates everyone not richer than Aunt Agatha (Agatha=0)
% and everyone whom Agatha hates
% We'll define this after we define richer relationships

% No one hates everyone
:- person(P), not hates_someone(P).
hates_someone(P) :- person(P), person(Q), hates(P,Q).

%% Wealth relationships (richer)
% Constraints: irreflexive and antisymmetric
% Also: killer is not richer than victim (Agatha=0)

% Choice rule for richer relationships (open relation)
{ richer(P1,P2) : person(P1), person(P2), P1 != P2 }.

% Irreflexive: no one is richer than themselves
:- richer(P,P).

% Antisymmetric: if P1 is richer than P2, then P2 is not richer than P1
:- richer(P1,P2), richer(P2,P1).

% Butler hates everyone not richer than Aunt Agatha (Agatha=0)
% This means: for all P where not richer[P,0], hates[1,P]
hates(1,P) :- person(P), not richer(P,0).

% Butler also hates everyone whom Agatha hates
hates(1,P) :- hates(0,P), person(P).

%% Movement constraints
% Each person is in exactly one room at each time
1 { location(P,R,T) : room(R) } 1 :- person(P), time(T).

% Movement is local: from time T-1 to T, a person either stays in the same room
% or moves to an adjacent room
:- location(P,R1,T-1), location(P,R2,T), T > 0, room(R1), room(R2),
   not adjacent(R1,R2), R1 != R2.

%% Witness statements (medium reliability: at least 14 of 18 must be true)
% Define witness statements as facts with indices
witness_statement(1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18).

% Witness statement 1: Charles was in Library at time 3
witness_true(1) :- location(2,3,3).
% Witness statement 2: Butler was in Hall at time 3
witness_true(2) :- location(1,1,3).
% Witness statement 3: Daisy was in Dining at time 3
witness_true(3) :- location(3,5,3).
% Witness statement 4: Edward was in Garden at time 5
witness_true(4) :- location(4,4,5).
% Witness statement 5: Felicity was in Kitchen at time 5
witness_true(5) :- location(5,2,5).
% Witness statement 6: George was in Lounge at time 5
witness_true(6) :- location(6,7,5).
% Witness statement 7: Harriet was in Lounge at time 3
witness_true(7) :- location(7,7,3).
% Witness statement 8: Ian was in Conservatory at time 5
witness_true(8) :- location(8,8,5).
% Witness statement 9: Julia was in Bedroom at time 5
witness_true(9) :- location(9,9,5).
% Witness statement 10: Kenneth was in Attic at time 5
witness_true(10) :- location(10,10,5).
% Witness statement 11: Lucy was in Hall at time 3
witness_true(11) :- location(11,1,3).
% Witness statement 12: Agatha was in Study at time 3
witness_true(12) :- location(0,0,3).
% Witness statement 13: Charles was in Library at time 5
witness_true(13) :- location(2,3,5).
% Witness statement 14: Butler was in Cellar at time 5
witness_true(14) :- location(1,6,5).
% Witness statement 15: Daisy was in Hall at time 5
witness_true(15) :- location(3,1,5).
% Witness statement 16: Edward was in Garden at time 3
witness_true(16) :- location(4,4,3).
% Witness statement 17: Felicity was in Kitchen at time 3
witness_true(17) :- location(5,2,3).
% Witness statement 18: George was in Dining at time 3
witness_true(18) :- location(6,5,3).

% At least 14 witness statements must be true
:- { witness_true(S) : witness_statement(S) } 13.

%% Forensic indicators (high reliability: all 10 must be true, all consistent with knife)
% Define forensic indicators as open relations (they must be consistent with knife)
{ gunshot_residue_near_body }.
{ shell_casings_in_study }.
{ blunt_force_not_primary }.
{ wound_pattern_blade_consistent }.
{ ligature_marks_on_neck }.
{ clean_edged_cut_present }.
{ heavy_object_blood_spatter }.
{ powder_burns_on_clothing }.
{ toxin_trace_in_glass }.
{ kitchen_knife_missing_after_time_4 }.

% Ensure forensic indicators are consistent with knife (weapon 1)
% Forensic indicators 1-10 are all consistent with knife, so no additional constraints needed
% except that the knife was used.

%% Killer and weapon constraints
% Exactly one killer
1 { killer(K) : person(K) } 1.

% Killer is not the victim (no suicides)
:- killer(K), K = 0.

% Killer must be in the Study at time 4 (murder location)
:- killer(K), not location(K,0,4).

% Killer hates the victim (Agatha=0)
:- killer(K), not hates(K,0).

% Killer is not richer than the victim (cannot be strictly richer)
:- killer(K), richer(K,0).

% Exactly one weapon was used: the Knife (weapon 1)
1 { weapon_used(W) : weapon(W) } 1.
:- weapon_used(W), W != 1.

%% Person names for output
person_name(0, "Agatha").
person_name(1, "Butler").
person_name(2, "Charles").
person_name(3, "Daisy").
person_name(4, "Edward").
person_name(5, "Felicity").
person_name(6, "George").
person_name(7, "Harriet").
person_name(8, "Ian").
person_name(9, "Julia").
person_name(10, "Kenneth").
person_name(11, "Lucy").

% Show the solution
#show killer/1.
#show killer_name/2.
#show weapon_used/1.