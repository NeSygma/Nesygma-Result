% --- DOMAIN DECLARATIONS ---
person(0..11).
room(0..11).
time(0..6).
weapon(0..5).

% Person names (for readable output)
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

% Room names (for reference)
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

% --- ROOM ADJACENCY (undirected) ---
adj(0,1). adj(1,0).   % Study - Hall
adj(0,3). adj(3,0).   % Study - Library
adj(1,2). adj(2,1).   % Hall - Kitchen
adj(1,5). adj(5,1).   % Hall - Dining
adj(1,6). adj(6,1).   % Hall - Cellar
adj(1,7). adj(7,1).   % Hall - Lounge
adj(1,9). adj(9,1).   % Hall - Bedroom
adj(2,5). adj(5,2).   % Kitchen - Dining
adj(2,11). adj(11,2). % Kitchen - Garage
adj(3,4). adj(4,3).   % Library - Garden
adj(3,7). adj(7,3).   % Library - Lounge
adj(4,8). adj(8,4).   % Garden - Conservatory
adj(4,11). adj(11,4). % Garden - Garage
adj(5,7). adj(7,5).   % Dining - Lounge
adj(6,11). adj(11,6). % Cellar - Garage
adj(7,8). adj(8,7).   % Lounge - Conservatory
adj(7,9). adj(9,7).   % Lounge - Bedroom
adj(7,10). adj(10,7). % Lounge - Attic
adj(9,10). adj(10,9). % Bedroom - Attic

% --- LOCATION MODELING ---

% Each person is in exactly one room at each time
1 { person_at_time(P, R, T) : room(R) } 1 :- person(P), time(T).

% High-Confidence Location Facts at Time 4 (hard facts)
person_at_time(0, 0, 4).   % Agatha in Study
person_at_time(1, 6, 4).   % Butler in Cellar
person_at_time(2, 3, 4).   % Charles in Library
person_at_time(3, 1, 4).   % Daisy in Hall
person_at_time(4, 4, 4).   % Edward in Garden
person_at_time(5, 2, 4).   % Felicity in Kitchen
person_at_time(6, 5, 4).   % George in Dining
person_at_time(7, 7, 4).   % Harriet in Lounge
person_at_time(8, 8, 4).   % Ian in Conservatory
person_at_time(9, 9, 4).   % Julia in Bedroom
person_at_time(10, 10, 4). % Kenneth in Attic
person_at_time(11, 0, 4).  % Lucy in Study

% Movement constraint: from T to T+1, person stays in same room or moves to adjacent room
:- person(P), time(T), T < 6, 
   person_at_time(P, R1, T), person_at_time(P, R2, T+1),
   R1 != R2, not adj(R1, R2).

% --- WITNESS STATEMENTS ---
% witness_stmt(ID, Person, Room, Time)
witness_stmt(1, 2, 3, 3).   % Charles in Library at time 3
witness_stmt(2, 1, 1, 3).   % Butler in Hall at time 3
witness_stmt(3, 3, 5, 3).   % Daisy in Dining at time 3
witness_stmt(4, 4, 4, 5).   % Edward in Garden at time 5
witness_stmt(5, 5, 2, 5).   % Felicity in Kitchen at time 5
witness_stmt(6, 6, 7, 5).   % George in Lounge at time 5
witness_stmt(7, 7, 7, 3).   % Harriet in Lounge at time 3
witness_stmt(8, 8, 8, 5).   % Ian in Conservatory at time 5
witness_stmt(9, 9, 9, 5).   % Julia in Bedroom at time 5
witness_stmt(10, 10, 10, 5). % Kenneth in Attic at time 5
witness_stmt(11, 11, 1, 3). % Lucy in Hall at time 3
witness_stmt(12, 0, 0, 3).  % Agatha in Study at time 3
witness_stmt(13, 2, 3, 5).  % Charles in Library at time 5
witness_stmt(14, 1, 6, 5).  % Butler in Cellar at time 5
witness_stmt(15, 3, 1, 5).  % Daisy in Hall at time 5
witness_stmt(16, 4, 4, 3).  % Edward in Garden at time 3
witness_stmt(17, 5, 2, 3).  % Felicity in Kitchen at time 3
witness_stmt(18, 6, 5, 3).  % George in Dining at time 3

% Each witness statement can be true or false
{ stmt_true(N) } :- witness_stmt(N, _, _, _).

% If a witness statement is true, the person must be at that room at that time
:- stmt_true(N), witness_stmt(N, P, R, T), not person_at_time(P, R, T).

% At least 14 of 18 witness statements must be true
:- #count { N : stmt_true(N) } < 14.

% --- FORENSIC INDICATORS ---
% All 10 indicators are consistent with knife usage (since knife is the murder weapon)
% At least 8 of 10 must be true
indicator(1..10).
{ indicator_true(I) } :- indicator(I).
:- #count { I : indicator_true(I) } < 8.

% --- MURDER FACTS ---
victim(0).            % Agatha is the victim
murder_room(0).       % Study
murder_time(4).       % Time 4
murder_weapon(1).     % Knife

% --- KILLER ---
% Exactly one killer, not the victim
1 { killer(P) : person(P), P != 0 } 1.

% Killer must be in the Study at time 4
:- killer(P), not person_at_time(P, 0, 4).

% Exactly one weapon used: the Knife
1 { weapon_used(W) : weapon(W) } 1.
:- weapon_used(W), W != 1.

% --- HATES RELATION (open relation) ---
{ hates(P1, P2) : person(P2), P1 != P2 } :- person(P1).

% Constraint 5: Agatha hates everybody except the butler
:- person(P), P != 0, P != 1, not hates(0, P).
:- hates(0, 1).  % Agatha does NOT hate the butler

% Constraint 4: Charles hates no one that Agatha hates
:- person(P), hates(0, P), hates(2, P).

% Constraint 7: Butler hates everyone whom Agatha hates
:- person(P), hates(0, P), not hates(1, P).

% Constraint 6: Butler hates everyone not richer than Aunt Agatha (Agatha = person 0)
:- person(P), P != 1, not richer(P, 0), not hates(1, P).

% Constraint 8: No one hates everyone (all 11 other people)
:- person(P), #count { Q : person(Q), P != Q, hates(P, Q) } = 11.

% Constraint 2: The killer hates the victim
:- killer(P), not hates(P, 0).

% Constraint 3: The killer is no richer than the victim (not strictly richer)
:- killer(P), richer(P, 0).

% --- RICHER RELATION (open relation) ---
{ richer(P1, P2) : person(P2), P1 != P2 } :- person(P1).

% Irreflexive: no one is richer than themselves (handled by choice rule body P1 != P2)

% Antisymmetric: if richer(X,Y) then not richer(Y,X)
:- richer(P1, P2), richer(P2, P1), P1 != P2.

% --- OUTPUT ---
killer_id(K) :- killer(K).
killer_name(N) :- killer_id(K), person_name(K, N).

#show killer_id/1.
#show killer_name/1.
#show stmt_true/1.
#show indicator_true/1.