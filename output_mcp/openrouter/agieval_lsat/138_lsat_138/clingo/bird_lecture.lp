% Domains
pos(1..5).
bird(oystercatcher). bird(petrel). bird(rail). bird(sandpiper). bird(tern).
location(g). location(h).

% Assign each position a unique bird
1 { bird_at(P,B) : bird(B) } 1 :- pos(P).
:- bird_at(P1,B), bird_at(P2,B), P1 != P2.

% Assign each position a location (G or H)
1 { location_at(P,g); location_at(P,h) } 1 :- pos(P).
% Exactly three lectures in Gladwyn Hall (g)
:- #count{P : location_at(P,g)} != 3.

% Given constraints
location_at(1,g).
location_at(4,h).

% Sandpipers lecture is at position 3 and in Howard Auditorium
bird_at(3,sandpiper).
location_at(3,h).

% Sandpipers earlier than Oystercatchers (position >3)
:- bird_at(Po,oystercatcher), Po <= 3.

% Terns earlier than Petrels
:- bird_at(Pp,petrel), bird_at(Pt,tern), Pt >= Pp.

% Petrels in Gladwyn Hall
:- bird_at(Pp,petrel), not location_at(Pp,g).

% Options definitions
option(a) :- bird_at(2,oystercatcher), location_at(2,g).
option(b) :- bird_at(5,oystercatcher), location_at(5,h).
option(c) :- bird_at(2,rail), location_at(2,h).
option(d) :- bird_at(2,tern), location_at(2,g).
option(e) :- bird_at(4,tern), location_at(4,h).

% At least one option must hold
:- not option(a), not option(b), not option(c), not option(d), not option(e).

#show option/1.