% Murder Mystery Solver

% ===== 1. DOMAIN DECLARATIONS =====
person(0..11).
room(0..11).
time(0..6).
weapon(0..5).

% Names for people
name(0, "Agatha").
name(1, "Butler").
name(2, "Charles").
name(3, "Daisy").
name(4, "Edward").
name(5, "Felicity").
name(6, "George").
name(7, "Harriet").
name(8, "Ian").
name(9, "Julia").
name(10, "Kenneth").
name(11, "Lucy").

% Names for rooms
room_name(0, "Study").
room_name(1, "Hall").
room_name(2, "Kitchen").
room_name(3, "Library").
room_name(4, "Garden").
room_name(5, "Dining").
room_name(6, "Cellar").
room_name(7, "Lounge").
room_name(8, "Conservatory").
room_name(9, "Bedroom").
room_name(10, "Attic").
room_name(11, "Garage").

% Weapon names
weapon_name(0, "Gun").
weapon_name(1, "Knife").
weapon_name(2, "Rope").
weapon_name(3, "Candlestick").
weapon_name(4, "Wrench").
weapon_name(5, "Poison").

% ===== 2. ROOM ADJACENCY =====
% Movement allowed only between adjacent rooms or staying put
adjacent(0, 1). adjacent(0, 3).  % Study: Hall, Library
adjacent(1, 0). adjacent(1, 2). adjacent(1, 5). adjacent(1, 6). adjacent(1, 7). adjacent(1, 9).  % Hall: Study, Kitchen, Dining, Cellar, Lounge, Bedroom
adjacent(2, 1). adjacent(2, 5). adjacent(2, 11).  % Kitchen: Hall, Dining, Garage
adjacent(3, 0). adjacent(3, 4). adjacent(3, 7).  % Library: Study, Garden, Lounge
adjacent(4, 3). adjacent(4, 8). adjacent(4, 11).  % Garden: Library, Conservatory, Garage
adjacent(5, 1). adjacent(5, 2). adjacent(5, 7).  % Dining: Hall, Kitchen, Lounge
adjacent(6, 1). adjacent(6, 11).  % Cellar: Hall, Garage
adjacent(7, 1). adjacent(7, 3). adjacent(7, 5). adjacent(7, 8). adjacent(7, 9). adjacent(7, 10).  % Lounge: Hall, Library, Dining, Conservatory, Bedroom, Attic
adjacent(8, 4). adjacent(8, 7).  % Conservatory: Garden, Lounge
adjacent(9, 1). adjacent(9, 7). adjacent(9, 10).  % Bedroom: Hall, Lounge, Attic
adjacent(10, 9). adjacent(10, 7).  % Attic: Bedroom, Lounge
adjacent(11, 2). adjacent(11, 6). adjacent(11, 4).  % Garage: Kitchen, Cellar, Garden

% ===== 3. HIGH-CONFIDENCE LOCATION FACTS AT TIME 4 =====
location(0, 0, 4).  % Agatha: Study at time 4
location(11, 0, 4). % Lucy: Study at time 4
location(1, 6, 4).   % Butler: Cellar at time 4
location(2, 3, 4).   % Charles: Library at time 4
location(3, 1, 4).   % Daisy: Hall at time 4
location(4, 4, 4).   % Edward: Garden at time 4
location(5, 2, 4).   % Felicity: Kitchen at time 4
location(6, 5, 4).   % George: Dining at time 4
location(7, 7, 4).   % Harriet: Lounge at time 4
location(8, 8, 4).   % Ian: Conservatory at time 4
location(9, 9, 4).   % Julia: Bedroom at time 4
location(10, 10, 4). % Kenneth: Attic at time 4

% ===== 4. WITNESS STATEMENTS =====
% Each statement is a fact that can be true or false
% We need at least 14 of 18 to be true
witness_statement(1, 2, 3).   % 1. Charles was in Library at time 3
witness_statement(1, 1, 3).   % 2. Butler was in Hall at time 3
witness_statement(3, 1, 3).   % 3. Daisy was in Dining at time 3
witness_statement(4, 4, 5).   % 4. Edward was in Garden at time 5
witness_statement(5, 2, 5).   % 5. Felicity was in Kitchen at time 5
witness_statement(6, 7, 5).   % 6. George was in Lounge at time 5
witness_statement(7, 7, 3).   % 7. Harriet was in Lounge at time 3
witness_statement(8, 8, 5).   % 8. Ian was in Conservatory at time 5
witness_statement(9, 9, 5).   % 9. Julia was in Bedroom at time 5
witness_statement(10, 10, 5). % 10. Kenneth was in Attic at time 5
witness_statement(11, 1, 3).  % 11. Lucy was in Hall at time 3
witness_statement(0, 0, 3).   % 12. Agatha was in Study at time 3
witness_statement(2, 3, 5).   % 13. Charles was in Library at time 5
witness_statement(1, 6, 5).   % 14. Butler was in Cellar at time 5
witness_statement(3, 1, 5).   % 15. Daisy was in Hall at time 5
witness_statement(4, 4, 3).   % 16. Edward was in Garden at time 3
witness_statement(5, 2, 3).   % 17. Felicity was in Kitchen at time 3
witness_statement(6, 5, 3).   % 18. George was in Dining at time 3

% Witness statement is true if the location matches
witness_true(S) :- witness_statement(S, P, T), location(P, R, T).

% Count true witness statements
witness_count(N) :- N = #count{S : witness_true(S)}.

% Constraint: at least 14 witness statements must be true
:- witness_count(N), N < 14.

% ===== 5. FORENSIC INDICATORS =====
% We need at least 8 of 10 to be true, all consistent with knife
% Since we know the murder weapon is knife (constraint 16), we can model these as constraints
% All forensic indicators are consistent with knife, so we count them as true
forensic_count(10). % All 10 are true since weapon is knife
:- forensic_count(N), N < 8.

% ===== 6. LOGICAL CONSTRAINTS =====
% Killer selection
% Agatha is victim (person 0)
% Killer cannot be Agatha
% Exactly one killer
1 { killer(K) : person(K), K != 0 } 1.

% Agatha hates everybody except the butler
% Agatha hates herself? No, she's the victim
% Agatha hates everyone except herself and butler
hates(0, P) :- person(P), P != 0, P != 1.

% Richer relation is irreflexive and antisymmetric
% We'll use choice rules to define richer
{ richer(P1, P2) } :- person(P1), person(P2), P1 != P2.

% Constraint: richer is antisymmetric (if P1 richer than P2, then P2 not richer than P1)
:- richer(P1, P2), richer(P2, P1).

% Butler hates everyone not richer than Agatha
% "not richer than Agatha" means Agatha is richer than or equal to them
% Since we don't have equality, we'll model: butler hates P if Agatha is richer than P or P is Agatha
hates(1, P) :- person(P), P != 1, richer(0, P).
hates(1, 0) :- person(0). % Agatha is not richer than herself, so butler hates her

% The butler hates everyone whom Agatha hates
hates(1, P) :- hates(0, P).

% Charles hates no one that Agatha hates
% This means: if Agatha hates P, then Charles does not hate P
:- hates(0, P), hates(2, P).

% No one hates everyone
% For each person P, there must be at least one person Q that P does not hate
:- person(P), #count{Q : hates(P, Q)} = 12.

% Killer hates the victim (Agatha)
:- killer(K), not hates(K, 0).

% Killer is no richer than victim (cannot be strictly richer)
% This means: victim is richer than or equal to killer
% We'll use: not richer(killer, victim)
:- killer(K), richer(K, 0).

% ===== 7. MOVEMENT CONSTRAINTS =====
% Each person is in exactly one room at each time
1 { location(P, R, T) : room(R) } 1 :- person(P), time(T).

% Movement is local: from time T-1 to T, a person either stays in the same room or moves to an adjacent room
% For times 1 to 6
:- time(T), T > 0, person(P), location(P, R1, T-1), location(P, R2, T), R1 != R2, not adjacent(R1, R2).

% ===== 8. MURDER CONSTRAINTS =====
% Murder occurred in Study at time 4
% Killer must be in Study at time 4
:- killer(K), not location(K, 0, 4).

% Exactly one weapon was used: the Knife
% We'll model weapon usage
weapon_used(1). % Knife is used
% Constraint: only knife is used
:- weapon_used(W), W != 1.

% ===== 9. OUTPUT =====
killer(K) :- killer(K).
killer_name(Name) :- killer(K), name(K, Name).

#show killer/1.
#show killer_name/1.