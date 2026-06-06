% Items
item(harmonica). item(lamp). item(mirror). item(sundial). item(table). item(vase).

% Days
 day(1). day(2). day(3). day(4). day(5). day(6).

% Assignment facts for each option
assignment(a, harmonica, 1). assignment(a, table, 2). assignment(a, sundial, 3). assignment(a, lamp, 4). assignment(a, vase, 5). assignment(a, mirror, 6).
assignment(b, lamp, 1). assignment(b, harmonica, 2). assignment(b, sundial, 3). assignment(b, mirror, 4). assignment(b, vase, 5). assignment(b, table, 6).
assignment(c, harmonica, 1). assignment(c, sundial, 2). assignment(c, table, 3). assignment(c, mirror, 4). assignment(c, lamp, 5). assignment(c, vase, 6).
assignment(d, sundial, 1). assignment(d, mirror, 2). assignment(d, harmonica, 3). assignment(d, table, 4). assignment(d, vase, 5). assignment(d, lamp, 6).
assignment(e, vase, 1). assignment(e, sundial, 2). assignment(e, lamp, 3). assignment(e, harmonica, 4). assignment(e, table, 5). assignment(e, mirror, 6).

% Choose one option
{opt(a); opt(b); opt(c); opt(d); opt(e)} 1.

% Derived chosen option
chosen(Option) :- opt(Option).

% Derive day facts from chosen option
 day(Item, Day) :- chosen(Option), assignment(Option, Item, Day).

% Ensure each item has exactly one day
1 { day(Item, Day) : day(Day) } 1 :- item(Item).
% Ensure each day has exactly one item
1 { day(Item, Day) : item(Item) } 1 :- day(Day).

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