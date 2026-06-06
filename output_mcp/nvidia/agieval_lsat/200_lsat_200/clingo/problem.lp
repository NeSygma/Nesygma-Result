item(harmonica).
item(lamp).
item(mirror).
item(sundial).
item(table).
item(vase).

day(1). day(2). day(3). day(4). day(5). day(6).

% Each item assigned to exactly one day
{ assigned(I,D) : day(D) } 1 :- item(I).
% Each day gets exactly one item
{ assigned(I,D) : item(I) } 1 :- day(D).

% Define earlier relation
earlier(X,Y) :- assigned(X,Dx), assigned(Y,Dy), Dx < Dy.

% Constraints
% 1. Sundial not on June 1
:- assigned(sundial, 1).

% 2. Sundial earlier than mirror and vase
:- not earlier(sundial, mirror).
:- not earlier(sundial, vase).

% 3. Conditional: if harmonica earlier than lamp then mirror earlier than lamp
:- assigned(harmonica, H), assigned(lamp, L), H < L, not earlier(mirror, lamp).

% 4. Table earlier than harmonica or vase, but not both
% At least one
1 { earlier(table, harmonica), earlier(table, vase) } 1.
% At most one
:- earlier(table, harmonica), earlier(table, vase).

% Define option atoms based on answer choices
mirror_june2 :- assigned(mirror, 2).
lamp_june2 :- assigned(lamp, 2).
vase_june2 :- assigned(vase, 2).
lamp_june3 :- assigned(lamp, 3).
mirror_june5 :- assigned(mirror, 5).

option(a) :- mirror_june2.
option(b) :- lamp_june2.
option(c) :- vase_june2.
option(d) :- lamp_june3.
option(e) :- mirror_june5.

#show option/1.