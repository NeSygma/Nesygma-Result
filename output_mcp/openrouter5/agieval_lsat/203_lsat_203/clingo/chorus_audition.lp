% Define the six singers
singer(kammer; lugo; trillo; waite; yoshida; zinn).

% Define positions 1 through 6
position(1..6).

% Recorded singers: Kammer and Lugo
recorded(kammer).
recorded(lugo).
not_recorded(X) :- singer(X), not recorded(X).

% Each position gets exactly one singer
1 { assigned(P, S) : singer(S) } 1 :- position(P).

% Each singer is assigned to exactly one position
1 { assigned(P, S) : position(P) } 1 :- singer(S).

% Condition: The fourth audition cannot be recorded.
:- assigned(4, S), recorded(S).

% Condition: The fifth audition must be recorded.
:- assigned(5, S), not recorded(S).

% Condition: Waite's audition must take place earlier than the two recorded auditions.
% Waite must be before Kammer and before Lugo.
:- assigned(Pw, waite), assigned(Pk, kammer), Pw >= Pk.
:- assigned(Pw, waite), assigned(Pl, lugo), Pw >= Pl.

% Condition: Kammer's audition must take place earlier than Trillo's audition.
:- assigned(Pk, kammer), assigned(Pt, trillo), Pk >= Pt.

% Condition: Zinn's audition must take place earlier than Yoshida's audition.
:- assigned(Pz, zinn), assigned(Py, yoshida), Pz >= Py.

% Now determine which singer CANNOT be the second audition.
% We check each option: if there exists a valid schedule where that singer is at position 2,
% then that option is possible. If no valid schedule exists, it's impossible.

% For each singer, check if they can be at position 2
possible_second(S) :- singer(S), assigned(2, S).

% The answer is the singer who is NOT possible at position 2
answer_singer(S) :- singer(S), not possible_second(S).

% Map to options
option(a) :- answer_singer(kammer).
option(b) :- answer_singer(lugo).
option(c) :- answer_singer(trillo).
option(d) :- answer_singer(waite).
option(e) :- answer_singer(zinn).

#show option/1.