%% Band Solo Problem - Multiple Choice Answer
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

% Constraint 3: Percussionist performs before keyboard player
:- assigned(percussionist, P1), assigned(keyboard, P2), P1 >= P2.

% Constraint 4: Keyboard after violinist AND before guitarist
:- assigned(violinist, Pv), assigned(keyboard, Pk), Pv >= Pk.
:- assigned(keyboard, Pk), assigned(guitarist, Pg), Pk >= Pg.

% Constraint 5: Saxophonist performs after EITHER percussionist OR trumpeter, but NOT both
sax_after_perc :- assigned(saxophonist, Ps), assigned(percussionist, Pp), Ps > Pp.
sax_after_trump :- assigned(saxophonist, Ps), assigned(trumpeter, Pt), Ps > Pt.

% XOR: exactly one is true
:- sax_after_perc, sax_after_trump.               % not both
:- not sax_after_perc, not sax_after_trump.       % not neither

%% Given condition: violinist performs the fourth solo
:- not assigned(violinist, 4).

%% Evaluate each option:
option_a_holds :- assigned(percussionist, Pp), assigned(violinist, Pv), Pp < Pv.
option_b_holds :- assigned(trumpeter, Pt), assigned(violinist, Pv), Pt < Pv.
option_c_holds :- assigned(trumpeter, Pt), assigned(guitarist, Pg), Pt < Pg.
option_d_holds :- assigned(saxophonist, Psx), assigned(violinist, Pv), Psx < Pv.
option_e_holds :- assigned(trumpeter, Pt), assigned(saxophonist, Psx), Pt < Psx.

% Show all for debugging
#show assigned/2.
#show option_a_holds/0.
#show option_b_holds/0.
#show option_c_holds/0.
#show option_d_holds/0.
#show option_e_holds/0.