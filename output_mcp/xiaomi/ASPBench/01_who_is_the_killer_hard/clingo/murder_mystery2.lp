% ============================================
% MURDER MYSTERY - ASP MODEL (v2)
% ============================================

% ============ DOMAINS ============
person(0..11).
room(0..11).
time(0..6).
weapon(0..5).

% Person names
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

% Room names
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

% ============ ROOM ADJACENCY ============
adjacent(0, 1). adjacent(0, 3).
adjacent(1, 0). adjacent(1, 2). adjacent(1, 5). adjacent(1, 6). adjacent(1, 7). adjacent(1, 9).
adjacent(2, 1). adjacent(2, 5). adjacent(2, 11).
adjacent(3, 0). adjacent(3, 4). adjacent(3, 7).
adjacent(4, 3). adjacent(4, 8). adjacent(4, 11).
adjacent(5, 1). adjacent(5, 2). adjacent(5, 7).
adjacent(6, 1). adjacent(6, 11).
adjacent(7, 1). adjacent(7, 3). adjacent(7, 5). adjacent(7, 8). adjacent(7, 9). adjacent(7, 10).
adjacent(8, 4). adjacent(8, 7).
adjacent(9, 1). adjacent(9, 7). adjacent(9, 10).
adjacent(10, 9). adjacent(10, 7).
adjacent(11, 2). adjacent(11, 6). adjacent(11, 4).

% Allow staying in same room
adjacent(R, R) :- room(R).

% ============ HIGH-CONFIDENCE LOCATION FACTS AT TIME 4 ============
location(0, 0, 4).   % Agatha: Study
location(11, 0, 4).  % Lucy: Study
location(1, 6, 4).   % Butler: Cellar
location(2, 3, 4).   % Charles: Library
location(3, 1, 4).   % Daisy: Hall
location(4, 4, 4).   % Edward: Garden
location(5, 2, 4).   % Felicity: Kitchen
location(6, 5, 4).   % George: Dining
location(7, 7, 4).   % Harriet: Lounge
location(8, 8, 4).   % Ian: Conservatory
location(9, 9, 4).   % Julia: Bedroom
location(10, 10, 4). % Kenneth: Attic

% ============ WITNESS STATEMENTS ============
witness(2, 3, 3).   % Charles in Library at time 3
witness(1, 1, 3).   % Butler in Hall at time 3
witness(3, 5, 3).   % Daisy in Dining at time 3
witness(4, 4, 5).   % Edward in Garden at time 5
witness(5, 2, 5).   % Felicity in Kitchen at time 5
witness(6, 7, 5).   % George in Lounge at time 5
witness(7, 7, 3).   % Harriet in Lounge at time 3
witness(8, 8, 5).   % Ian in Conservatory at time 5
witness(9, 9, 5).   % Julia in Bedroom at time 5
witness(10, 10, 5). % Kenneth in Attic at time 5
witness(11, 1, 3).  % Lucy in Hall at time 3
witness(0, 0, 3).   % Agatha in Study at time 3
witness(2, 3, 5).   % Charles in Library at time 5
witness(1, 6, 5).   % Butler in Cellar at time 5
witness(3, 1, 5).   % Daisy in Hall at time 5
witness(4, 4, 3).   % Edward in Garden at time 3
witness(5, 2, 3).   % Felicity in Kitchen at time 3
witness(6, 5, 3).   % George in Dining at time 3

% ============ FORENSIC INDICATORS ============
forensic(1). forensic(2). forensic(3). forensic(4). forensic(5).
forensic(6). forensic(7). forensic(8). forensic(9). forensic(10).

% ============ CONSTRAINT 1: Exactly one killer ============
1 { killer(P) : person(P) } 1.

% ============ CONSTRAINT 9: Agatha is the victim ============
victim(0).

% ============ CONSTRAINT 10: No suicides ============
:- killer(0).

% ============ CONSTRAINT 16: Murder weapon is Knife ============
murder_weapon(1).

% ============ HATE RELATIONS (Open relation with constraints) ============
% Choice rule for hates - we need to find valid assignment
{ hates(P1, P2) } :- person(P1), person(P2), P1 != P2.

% ============ CONSTRAINT 5: Agatha hates everybody except the butler ============
hates(0, P) :- person(P), P != 1, P != 0.
:- hates(0, 1).  % Agatha does NOT hate butler

% ============ CONSTRAINT 4: Charles hates no one that Agatha hates ============
:- hates(2, X), hates(0, X), person(X).

% ============ CONSTRAINT 6: Butler hates everyone not richer than Agatha ============
hates(1, P) :- person(P), P != 1, not richer(P, 0).

% ============ CONSTRAINT 7: Butler hates everyone whom Agatha hates ============
hates(1, P) :- hates(0, P), P != 1.

% ============ CONSTRAINT 8: No one hates everyone ============
:- person(P), not has_non_hated(P).
has_non_hated(P) :- person(P), person(Q), P != Q, not hates(P, Q).

% ============ CONSTRAINT 2: Killer hates victim ============
:- killer(P), not hates(P, 0).

% ============ RICHER RELATIONS (Open relation with constraints) ============
{ richer(P1, P2) } :- person(P1), person(P2), P1 != P2.
:- richer(P, P).  % Irreflexive
:- richer(P1, P2), richer(P2, P1).  % Antisymmetric

% ============ CONSTRAINT 3: Killer is no richer than victim ============
:- killer(P), richer(P, 0).

% ============ CONSTRAINT 12: Each person in exactly one room at each time ============
1 { location(P, R, T) : room(R) } 1 :- person(P), time(T).

% ============ CONSTRAINT 13: Movement is local ============
:- location(P, R1, T-1), location(P, R2, T), not adjacent(R1, R2), time(T), T > 0.

% ============ CONSTRAINT 15: Killer must be in Study at time 4 ============
:- killer(P), not location(P, 0, 4).

% ============ WITNESS STATEMENT CONSISTENCY ============
witness_true(P, R, T) :- witness(P, R, T), location(P, R, T).
witness_count(N) :- N = #count { P, R, T : witness_true(P, R, T) }.
:- witness_count(N), N < 14.

% ============ FORENSIC CONSISTENCY ============
forensic_count(N) :- N = #count { F : forensic(F) }.
:- forensic_count(N), N < 8.

% ============ SHOW ============
#show killer/1.
#show killer_name/2.
killer_name(P, N) :- killer(P), person_name(P, N).