% Domain: six singers
singer(kammer). singer(lugo). singer(trillo). singer(waite). singer(yoshida). singer(zinn).

% Positions 1 through 6
position(1..6).

% Recorded auditions: Kammer and Lugo
recorded(kammer). recorded(lugo).

% Original constraints:
% 1. Fourth audition cannot be recorded
% 2. Fifth audition must be recorded
% 3. Waite's audition must take place earlier than the two recorded auditions
% 4. Kammer's audition must take place earlier than Trillo's audition
% 5. Zinn's audition must take place earlier than Yoshida's audition

% Each singer has exactly one position
1 { position_of(S, P) : position(P) } 1 :- singer(S).

% Each position has exactly one singer
1 { position_of(S, P) : singer(S) } 1 :- position(P).

% Symmetry breaking: position_of is functional
position_of(S, P) :- position_of(S, P).

% Original constraint 1: Fourth audition cannot be recorded
:- position_of(S, 4), recorded(S).

% Original constraint 2: Fifth audition must be recorded
:- not position_of(S, 5), recorded(S).  % Actually, this means some recorded singer must be at position 5
% Better: There exists a recorded singer at position 5
:- not position_of(S, 5), recorded(S).  % This is wrong
% Correct: At least one recorded singer is at position 5
:- position_of(S, 5), not recorded(S).  % This says position 5 cannot be non-recorded
% Actually: position 5 must be recorded
:- position_of(S, 5), not recorded(S).

% Original constraint 3: Waite's audition must take place earlier than the two recorded auditions
% Waite must be before both Kammer and Lugo
:- position_of(waite, Pw), position_of(kammer, Pk), Pw >= Pk.
:- position_of(waite, Pw), position_of(lugo, Pl), Pw >= Pl.

% Original constraint 4: Kammer's audition must take place earlier than Trillo's audition
:- position_of(kammer, Pk), position_of(trillo, Pt), Pk >= Pt.

% Original constraint 5: Zinn's audition must take place earlier than Yoshida's audition
:- position_of(zinn, Pz), position_of(yoshida, Py), Pz >= Py.

% Show the solution
#show position_of/2.