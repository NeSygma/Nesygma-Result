%% Band Solo Problem
%% Members: guitarist, keyboard, percussionist, saxophonist, trumpeter, violinist
%% Positions: 1 through 6

% Define positions
position(1..6).

% Define band members
member(guitarist; keyboard; percussionist; saxophonist; trumpeter; violinist).

% Each member gets exactly one position
1 { assigned(M, P) : position(P) } 1 :- member(M).

% Each position gets exactly one member
1 { assigned(M, P) : member(M) } 1 :- position(P).

% Constraint 2: Guitarist does not perform the fourth solo
:- assigned(guitarist, 4).

% Helper: position P1 is earlier than position P2
earlier(P1, P2) :- position(P1), position(P2), P1 < P2.

% Constraint 3: Percussionist performs before keyboard player
:- assigned(percussionist, P1), assigned(keyboard, P2), not earlier(P1, P2).

% Constraint 4: Keyboard after violinist AND before guitarist
:- assigned(violinist, Pv), assigned(keyboard, Pk), not earlier(Pv, Pk).
:- assigned(keyboard, Pk), assigned(guitarist, Pg), not earlier(Pk, Pg).

% Constraint 5: Saxophonist performs after EITHER percussionist OR trumpeter, but NOT both
% Define sax_after_perc
sax_after_perc :- assigned(saxophonist, Ps), assigned(percussionist, Pp), Ps > Pp.
% Define sax_after_trump
sax_after_trump :- assigned(saxophonist, Ps), assigned(trumpeter, Pt), Ps > Pt.

% XOR: exactly one is true
:- sax_after_perc, sax_after_trump.               % not both
:- not sax_after_perc, not sax_after_trump.       % not neither

%% Given condition: violinist performs the fourth solo
:- not assigned(violinist, 4).

%% Evaluate each option:
% (A) percussionist before violinist
option_a_holds :- assigned(percussionist, Pp), assigned(violinist, Pv), earlier(Pp, Pv).
% (B) trumpeter before violinist
option_b_holds :- assigned(trumpeter, Pt), assigned(violinist, Pv), earlier(Pt, Pv).
% (C) trumpeter before guitarist
option_c_holds :- assigned(trumpeter, Pt), assigned(guitarist, Pg), earlier(Pt, Pg).
% (D) saxophonist before violinist
option_d_holds :- assigned(saxophonist, Psx), assigned(violinist, Pv), earlier(Psx, Pv).
% (E) trumpeter before saxophonist
option_e_holds :- assigned(trumpeter, Pt), assigned(saxophonist, Psx), earlier(Pt, Psx).

#show assigned/2.
#show option_a_holds/0.
#show option_b_holds/0.
#show option_c_holds/0.
#show option_d_holds/0.
#show option_e_holds/0.