% Positions
position(1..5).

% Venues: G = gladwyn, H = howard
venue(1,g). % first lecture Gladwyn Hall
venue(4,h). % fourth lecture Howard Auditorium

% Exactly one of positions 2,3,5 is Howard Auditorium (since total H =2)
1 { venue(2,h); venue(3,h); venue(5,h) } 1.
% The others among 2,3,5 are Gladwyn Hall
venue(P,g) :- position(P), P != 1, P != 4, not venue(P,h).

% Birds
bird(o). % oystercatchers
bird(p). % petrels
bird(r). % rails
bird(s). % sandpipers
bird(t). % terns

% Assign each position exactly one bird
1 { bird_at(P,B) : bird(B) } 1 :- position(P).
% Each bird appears exactly once
:- bird_at(P1,B), bird_at(P2,B), P1 != P2.

% Constraints from problem
% Sandpipers in Howard Auditorium
:- bird_at(P,s), not venue(P,h).
% Sandpipers earlier than Oystercatchers
:- bird_at(Ps,s), bird_at(Po,o), Ps >= Po.
% Petrels in Gladwyn Hall
:- bird_at(P,p), not venue(P,g).
% Terns earlier than Petrels
:- bird_at(Pt,t), bird_at(Pp,p), Pt >= Pp.
% Exactly three lectures in Gladwyn Hall
:- #count { P : venue(P,g) } != 3.

% Option B condition: second and third lectures both Howard Auditorium
conditionB :- venue(2,h), venue(3,h).
violationB :- not conditionB.
#minimize { 1@1, violationB }.

option(b) :- violationB.

#show option/1.