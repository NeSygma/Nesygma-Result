% Items
item(harmonica). item(lamp). item(mirror). item(sundial). item(table). item(vase).

% Days
day(1). day(2). day(3). day(4). day(5). day(6).

% Option choice
{ opt(a); opt(b); opt(c); opt(d); opt(e) } 1.

% Assignments
assignment_a(harmonica,1). assignment_a(table,2). assignment_a(sundial,3). assignment_a(lamp,4). assignment_a(vase,5). assignment_a(mirror,6).
assignment_b(lamp,1). assignment_b(harmonica,2). assignment_b(sundial,3). assignment_b(mirror,4). assignment_b(vase,5). assignment_b(table,6).
assignment_c(harmonica,1). assignment_c(sundial,2). assignment_c(table,3). assignment_c(mirror,4). assignment_c(lamp,5). assignment_c(vase,6).
assignment_d(sundial,1). assignment_d(mirror,2). assignment_d(harmonica,3). assignment_d(table,4). assignment_d(vase,5). assignment_d(lamp,6).
assignment_e(vase,1). assignment_e(sundial,2). assignment_e(lamp,3). assignment_e(harmonica,4). assignment_e(table,5). assignment_e(mirror,6).

% Day facts conditional on chosen option
day(Item, D) :- opt(a), assignment_a(Item, D).
day(Item, D) :- opt(b), assignment_b(Item, D).
day(Item, D) :- opt(c), assignment_c(Item, D).
day(Item, D) :- opt(d), assignment_d(Item, D).
day(Item, D) :- opt(e), assignment_e(Item, D).

% Ensure each item has exactly one day
1 { day(Item, D) : day(D) } 1 :- item(Item).
% Ensure each day has exactly one item
1 { day(Item, D) : item(Item) } 1 :- day(D).

% Define earlier predicate
earlier(X,Y) :- day(X, DX), day(Y, DY), DX < DY.

% Constraints
:- day(sundial, 1).
:- not earlier(sundial, mirror).
:- not earlier(sundial, vase).
:- earlier(harmonica, lamp), not earlier(mirror, lamp).
:- earlier(table, harmonica), earlier(table, vase).
:- not earlier(table, harmonica), not earlier(table, vase).

% Map correct answer to option/1
option(a) :- opt(a).
option(b) :- opt(b).
option(c) :- opt(c).
option(d) :- opt(d).
option(e) :- opt(e).

#show option/1.