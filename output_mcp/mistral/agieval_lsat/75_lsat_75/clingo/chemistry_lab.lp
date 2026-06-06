% Define days and times
day(wednesday). day(thursday). day(friday).
time(morning). time(afternoon).

% Define assistants
assistant(julio). assistant(kevin). assistant(lan). assistant(nessa). assistant(olivia). assistant(rebecca).

% Given: Julio leads Thursday afternoon session
assigned(julio, thursday, afternoon).

% Choice rule for other assistants' assignments
{ assigned(A, D, T) : assistant(A), day(D), time(T) } :- assistant(A), A != julio.

% Constraint 1: Kevin and Rebecca must lead sessions on the same day
:- assigned(kevin, D1, _), assigned(rebecca, D2, _), D1 != D2.

% Constraint 2: Lan and Olivia cannot lead sessions on the same day
:- assigned(lan, D1, _), assigned(olivia, D2, _), D1 == D2.

% Constraint 3: Nessa must lead an afternoon session
:- assigned(nessa, _, T), T != afternoon.

% Constraint 4: Julio's session must be on an earlier day than Olivia's
% Define day ordering
day_order(wednesday, thursday).
day_order(wednesday, friday).
day_order(thursday, friday).

:- assigned(olivia, D, _), day_order(D, thursday).

% Determine possible assignments for each assistant (excluding Julio)
% Kevin
possible_kevin(D, T) :-
    assigned(kevin, D, T),
    assigned(rebecca, D, _).

% Rebecca
possible_rebecca(D, T) :-
    assigned(rebecca, D, T),
    assigned(kevin, D, _).

% Lan
possible_lan(D, T) :-
    assigned(lan, D, T),
    not assigned(olivia, D, _).

% Olivia
possible_olivia(D, T) :-
    assigned(olivia, D, T),
    not assigned(lan, D, _),
    not day_order(D, thursday).

% Nessa
possible_nessa(D, T) :-
    assigned(nessa, D, T),
    T == afternoon.

% Count unique assignments
unique_kevin :- 1 { possible_kevin(D, T) : day(D), time(T) } 1.
unique_rebecca :- 1 { possible_rebecca(D, T) : day(D), time(T) } 1.
unique_lan :- 1 { possible_lan(D, T) : day(D), time(T) } 1.
unique_olivia :- 1 { possible_olivia(D, T) : day(D), time(T) } 1.
unique_nessa :- 1 { possible_nessa(D, T) : day(D), time(T) } 1.

% Map the correct answer to option/1
option(a) :- unique_kevin, not unique_rebecca, not unique_lan, not unique_olivia, not unique_nessa.
option(a) :- unique_rebecca, not unique_kevin, not unique_lan, not unique_olivia, not unique_nessa.
option(a) :- unique_lan, not unique_kevin, not unique_rebecca, not unique_olivia, not unique_nessa.
option(a) :- unique_olivia, not unique_kevin, not unique_rebecca, not unique_lan, not unique_nessa.
option(a) :- unique_nessa, not unique_kevin, not unique_rebecca, not unique_lan, not unique_olivia.

option(b) :- unique_kevin, unique_rebecca, not unique_lan, not unique_olivia, not unique_nessa.
option(b) :- unique_kevin, unique_lan, not unique_rebecca, not unique_olivia, not unique_nessa.
option(b) :- unique_kevin, unique_olivia, not unique_rebecca, not unique_lan, not unique_nessa.
option(b) :- unique_kevin, unique_nessa, not unique_rebecca, not unique_lan, not unique_olivia.
option(b) :- unique_rebecca, unique_lan, not unique_kevin, not unique_olivia, not unique_nessa.
option(b) :- unique_rebecca, unique_olivia, not unique_kevin, not unique_lan, not unique_nessa.
option(b) :- unique_rebecca, unique_nessa, not unique_kevin, not unique_lan, not unique_olivia.
option(b) :- unique_lan, unique_olivia, not unique_kevin, not unique_rebecca, not unique_nessa.
option(b) :- unique_lan, unique_nessa, not unique_kevin, not unique_rebecca, not unique_olivia.
option(b) :- unique_olivia, unique_nessa, not unique_kevin, not unique_rebecca, not unique_lan.

option(c) :- unique_kevin, unique_rebecca, unique_lan, not unique_olivia, not unique_nessa.
option(c) :- unique_kevin, unique_rebecca, unique_olivia, not unique_lan, not unique_nessa.
option(c) :- unique_kevin, unique_rebecca, unique_nessa, not unique_lan, not unique_olivia.
option(c) :- unique_kevin, unique_lan, unique_olivia, not unique_rebecca, not unique_nessa.
option(c) :- unique_kevin, unique_lan, unique_nessa, not unique_rebecca, not unique_olivia.
option(c) :- unique_kevin, unique_olivia, unique_nessa, not unique_rebecca, not unique_lan.
option(c) :- unique_rebecca, unique_lan, unique_olivia, not unique_kevin, not unique_nessa.
option(c) :- unique_rebecca, unique_lan, unique_nessa, not unique_kevin, not unique_olivia.
option(c) :- unique_rebecca, unique_olivia, unique_nessa, not unique_kevin, not unique_lan.
option(c) :- unique_lan, unique_olivia, unique_nessa, not unique_kevin, not unique_rebecca.

option(d) :- unique_kevin, unique_rebecca, unique_lan, unique_olivia, not unique_nessa.
option(d) :- unique_kevin, unique_rebecca, unique_lan, unique_nessa, not unique_olivia.
option(d) :- unique_kevin, unique_rebecca, unique_olivia, unique_nessa, not unique_lan.
option(d) :- unique_kevin, unique_lan, unique_olivia, unique_nessa, not unique_rebecca.
option(d) :- unique_rebecca, unique_lan, unique_olivia, unique_nessa, not unique_kevin.

option(e) :- unique_kevin, unique_rebecca, unique_lan, unique_olivia, unique_nessa.

#show option/1.