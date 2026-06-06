% Domains
person(j). person(k). person(l). person(n). person(o).
country(vene). country(yemen). country(zambia).

% Fixed assignment: Ong to Venezuela
assign(vene,o).
% Prevent other assignments to Venezuela
:- assign(vene,P), P != o.

% Exactly one ambassador per country (for remaining countries)
1 { assign(C,P) : person(P), P != o } 1 :- country(C), C != vene.

% No person assigned to more than one country
:- assign(C1,P), assign(C2,P), C1 != C2.

% Exclusive assignment of Kayne or Novetzke (exactly one)
assigned_k :- assign(_,k).
assigned_n :- assign(_,n).
:- assigned_k, assigned_n.
:- not assigned_k, not assigned_n.

% If Jaramillo assigned then Kayne assigned
:- assign(_,j), not assigned_k.

% If Landon assigned then must be Zambia
:- assign(C,l), C != zambia.

% If Ong assigned to Venezuela then Kayne not Yemen
:- assign(vene,o), assign(yemen,k).

% Define other assigned persons (excluding Ong)
other_assigned(P) :- assign(_,P), P != o.

% Options mapping (feasibility)
option(a) :- other_assigned(j), other_assigned(l), not other_assigned(k), not other_assigned(n).
option(b) :- other_assigned(j), other_assigned(n), not other_assigned(k), not other_assigned(l).
option(c) :- other_assigned(k), other_assigned(l), not other_assigned(j), not other_assigned(n).
option(d) :- other_assigned(k), other_assigned(n), not other_assigned(j), not other_assigned(l).
option(e) :- other_assigned(l), other_assigned(n), not other_assigned(j), not other_assigned(k).

#show option/1.