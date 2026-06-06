% Define the musicians
musician(guitarist; keyboard_player; percussionist; saxophonist; trumpeter; violinist).

% Define solo positions (1 to 6)
position(1..6).

% Choice rule: Assign each musician to a unique position
1 { solo(M, P) : position(P) } 1 :- musician(M).
:- position(P), 2 { solo(M, P) : musician(M) }.

% Constraint 1: Guitarist does not perform the 4th solo
:- solo(guitarist, 4).

% Constraint 2: Percussionist performs before keyboard player
:- solo(percussionist, P1), solo(keyboard_player, P2), P1 >= P2.

% Constraint 3: Keyboard player performs after violinist and before guitarist
:- solo(violinist, P1), solo(keyboard_player, P2), P1 >= P2.
:- solo(keyboard_player, P1), solo(guitarist, P2), P1 >= P2.

% Constraint 4: Saxophonist performs after exactly one of percussionist or trumpeter
% Helper predicates for saxophonist constraint
sax_after_perc :- solo(saxophonist, S), solo(percussionist, P), S > P.
sax_after_trump :- solo(saxophonist, S), solo(trumpeter, T), S > T.

% Saxophonist must perform after exactly one of percussionist or trumpeter
:- solo(saxophonist, _), sax_after_perc, sax_after_trump.
:- solo(saxophonist, _), not sax_after_perc, not sax_after_trump.

% Define the options as facts
% Option A: violinist, percussionist, saxophonist, guitarist, trumpeter, keyboard player
option_order(a, violinist, 1).
option_order(a, percussionist, 2).
option_order(a, saxophonist, 3).
option_order(a, guitarist, 4).
option_order(a, trumpeter, 5).
option_order(a, keyboard_player, 6).

% Option B: percussionist, violinist, keyboard player, trumpeter, saxophonist, guitarist
option_order(b, percussionist, 1).
option_order(b, violinist, 2).
option_order(b, keyboard_player, 3).
option_order(b, trumpeter, 4).
option_order(b, saxophonist, 5).
option_order(b, guitarist, 6).

% Option C: violinist, trumpeter, saxophonist, percussionist, keyboard player, guitarist
option_order(c, violinist, 1).
option_order(c, trumpeter, 2).
option_order(c, saxophonist, 3).
option_order(c, percussionist, 4).
option_order(c, keyboard_player, 5).
option_order(c, guitarist, 6).

% Option D: keyboard player, trumpeter, violinist, saxophonist, guitarist, percussionist
option_order(d, keyboard_player, 1).
option_order(d, trumpeter, 2).
option_order(d, violinist, 3).
option_order(d, saxophonist, 4).
option_order(d, guitarist, 5).
option_order(d, percussionist, 6).

% Option E: guitarist, violinist, keyboard player, percussionist, saxophonist, trumpeter
option_order(e, guitarist, 1).
option_order(e, violinist, 2).
option_order(e, keyboard_player, 3).
option_order(e, percussionist, 4).
option_order(e, saxophonist, 5).
option_order(e, trumpeter, 6).

% Check if the solo assignment matches the option order
valid_option(Opt) :-
    option_order(Opt, M, P),
    solo(M, P).

% Ensure all positions in the option are matched
valid_option(Opt) :-
    option_order(Opt, _, _),
    not invalid_option(Opt).

invalid_option(Opt) :-
    option_order(Opt, M, P),
    not solo(M, P).

% Map the correct answer to option/1
option(a) :- valid_option(a), not valid_option(b), not valid_option(c), not valid_option(d), not valid_option(e).
option(b) :- valid_option(b), not valid_option(a), not valid_option(c), not valid_option(d), not valid_option(e).
option(c) :- valid_option(c), not valid_option(a), not valid_option(b), not valid_option(d), not valid_option(e).
option(d) :- valid_option(d), not valid_option(a), not valid_option(b), not valid_option(c), not valid_option(e).
option(e) :- valid_option(e), not valid_option(a), not valid_option(b), not valid_option(c), not valid_option(d).

#show option/1.