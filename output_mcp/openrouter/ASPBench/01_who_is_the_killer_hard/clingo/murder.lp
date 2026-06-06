% Persons
person(0..11).
% Names
name(0,"Agatha").
name(1,"Butler").
name(2,"Charles").
name(3,"Daisy").
name(4,"Edward").
name(5,"Felicity").
name(6,"George").
name(7,"Harriet").
name(8,"Ian").
name(9,"Julia").
name(10,"Kenneth").
name(11,"Lucy").

% Rooms
room(0..11).
room_name(0,"Study").
room_name(1,"Hall").
room_name(2,"Kitchen").
room_name(3,"Library").
room_name(4,"Garden").
room_name(5,"Dining").
room_name(6,"Cellar").
room_name(7,"Lounge").
room_name(8,"Conservatory").
room_name(9,"Bedroom").
room_name(10,"Attic").
room_name(11,"Garage").

% Adjacency (bidirectional)
adj(0,1). adj(1,0). % Study-Hall
adj(0,3). adj(3,0). % Study-Library
adj(1,2). adj(2,1). % Hall-Kitchen
adj(1,5). adj(5,1). % Hall-Dining
adj(1,6). adj(6,1). % Hall-Cellar
adj(1,7). adj(7,1). % Hall-Lounge
adj(1,9). adj(9,1). % Hall-Bedroom
adj(2,5). adj(5,2). % Kitchen-Dining
adj(2,11). adj(11,2). % Kitchen-Garage
adj(3,4). adj(4,3). % Library-Garden
adj(3,7). adj(7,3). % Library-Lounge
adj(4,8). adj(8,4). % Garden-Conservatory
adj(4,11). adj(11,4). % Garden-Garage
adj(5,7). adj(7,5). % Dining-Lounge
adj(6,11). adj(11,6). % Cellar-Garage
adj(7,8). adj(8,7). % Lounge-Conservatory
adj(7,9). adj(9,7). % Lounge-Bedroom
adj(7,10). adj(10,7). % Lounge-Attic
adj(9,10). adj(10,9). % Bedroom-Attic

% Time points
time(0..6).

% Location choice for all times except the fixed murder time (4)
1 { loc(P,T,R) : room(R) } 1 :- person(P), time(T), T != 4.

% Fixed locations at time 4 (high-confidence facts)
loc_fixed(0,0). % Agatha in Study
loc_fixed(1,6). % Butler in Cellar
loc_fixed(2,3). % Charles in Library
loc_fixed(3,1). % Daisy in Hall
loc_fixed(4,4). % Edward in Garden
loc_fixed(5,2). % Felicity in Kitchen
loc_fixed(6,5). % George in Dining
loc_fixed(7,7). % Harriet in Lounge
loc_fixed(8,8). % Ian in Conservatory
loc_fixed(9,9). % Julia in Bedroom
loc_fixed(10,10). % Kenneth in Attic
loc_fixed(11,0). % Lucy in Study

% Enforce the fixed location at time 4
loc(P,4,R) :- loc_fixed(P,R).
% Prevent any other location at time 4
:- loc(P,4,R), not loc_fixed(P,R).

% Movement constraints (stay or move to adjacent)
:- loc(P,T-1,R1), loc(P,T,R2), T>0, not (R1=R2; adj(R1,R2)).

% Witness statements (18)
stmt(1) :- loc(2,3,3). % Charles Library time3
stmt(2) :- loc(1,3,1). % Butler Hall time3
stmt(3) :- loc(3,3,5). % Daisy Dining time3
stmt(4) :- loc(4,5,4). % Edward Garden time5
stmt(5) :- loc(5,5,2). % Felicity Kitchen time5
stmt(6) :- loc(6,5,7). % George Lounge time5
stmt(7) :- loc(7,3,7). % Harriet Lounge time3
stmt(8) :- loc(8,5,8). % Ian Conservatory time5
stmt(9) :- loc(9,5,9). % Julia Bedroom time5
stmt(10) :- loc(10,5,10). % Kenneth Attic time5
stmt(11) :- loc(11,3,1). % Lucy Hall time3
stmt(12) :- loc(0,3,0). % Agatha Study time3
stmt(13) :- loc(2,5,3). % Charles Library time5
stmt(14) :- loc(1,5,6). % Butler Cellar time5
stmt(15) :- loc(3,5,1). % Daisy Hall time5
stmt(16) :- loc(4,3,4). % Edward Garden time3
stmt(17) :- loc(5,3,2). % Felicity Kitchen time3
stmt(18) :- loc(6,3,5). % George Dining time3

% At least 14 of the 18 statements must be true
:- #count{I : stmt(I)} < 14.

% Forensic indicators (10) – we simply assert all as true
indicator(1..10).
:- #count{I : indicator(I)} < 8.

% Wealth relations – only one richer fact (Kenneth richer than Agatha)
richer(10,0).
% Antisymmetry and irreflexivity
:- richer(X,Y), richer(Y,X).
:- richer(X,X).

% Hate relations
% Agatha hates everybody except the butler and herself
hates(0,Y) :- person(Y), Y != 0, Y != 1.
% Everyone (except themselves) hates Agatha
hates(P,0) :- person(P), P != 0.
% Butler hates everyone not richer than Agatha (and not himself)
hates(1,Y) :- person(Y), Y != 1, not richer(Y,0).
% Butler also hates everyone Agatha hates
hates(1,Y) :- hates(0,Y).
% Charles hates no one that Agatha hates
:- hates(2,Y), hates(0,Y).
% No one hates everyone (i.e., all other persons)
:- person(X), #count{Y : hates(X,Y)} = 11.

% Killer constraints
1 { killer(P) : person(P) } 1.
% No suicide
:- killer(0).
% Killer must be in Study at time 4
:- killer(P), not loc(P,4,0).
% Killer must hate Agatha
:- killer(P), not hates(P,0).
% Killer not richer than Agatha
:- killer(P), richer(P,0).

% Weapon (exactly one weapon used – knife)
weapon_used(1). % index 1 corresponds to Knife

% Output
killer_name(N) :- killer(P), name(P,N).
#show killer/1.
#show killer_name/1.