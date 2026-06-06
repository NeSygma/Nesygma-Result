% Domains
pos(1..5).
bird(oystercatchers; petrels; rails; sandpipers; terns).
venue(g; h).

% Generate assignments: each position gets exactly one bird and one venue
1 { bird_at(Pos, B) : bird(B) } 1 :- pos(Pos).
1 { venue_at(Pos, V) : venue(V) } 1 :- pos(Pos).

% Each bird appears exactly once
1 { bird_at(Pos, B) : pos(Pos) } 1 :- bird(B).

% Constraints from problem
venue_at(1, g).
venue_at(4, h).
:- #count { Pos : venue_at(Pos, g) } != 3.

% Sandpipers in Howard and earlier than oystercatchers
venue_at(PosS, h) :- bird_at(PosS, sandpipers).
:- bird_at(PosS, sandpipers), bird_at(PosO, oystercatchers), PosS >= PosO.

% Terns earlier than petrels, petrels in Gladwyn
venue_at(PosP, g) :- bird_at(PosP, petrels).
:- bird_at(PosT, terns), bird_at(PosP, petrels), PosT >= PosP.

% Check which options could be true for position 5
option_a :- bird_at(5, oystercatchers), venue_at(5, g).
option_b :- bird_at(5, petrels), venue_at(5, h).
option_c :- bird_at(5, rails), venue_at(5, h).
option_d :- bird_at(5, sandpipers), venue_at(5, h).
option_e :- bird_at(5, terns), venue_at(5, g).

#show option_a/0.
#show option_b/0.
#show option_c/0.
#show option_d/0.
#show option_e/0.