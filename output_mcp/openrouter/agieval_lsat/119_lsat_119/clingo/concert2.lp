% Bands
band(uneasy). band(vegemite). band(wellspring). band(xpert). band(yardsign). band(zircon).

% Slots 1..6
slotnum(1..6).

% Each band assigned to exactly one slot
1 { slot(B,S) : slotnum(S) } 1 :- band(B).
% No two bands share a slot
:- slot(B1,S), slot(B2,S), B1 != B2.

% Constraints from problem
% Vegemite earlier than Zircon
:- slot(vegemite,Sv), slot(zircon,Sz), Sv >= Sz.
% Wellspring earlier than Xpert
:- slot(wellspring,Sw), slot(xpert,Sx), Sw >= Sx.
% Zircon earlier than Xpert
:- slot(zircon,Sz), slot(xpert,Sx), Sz >= Sx.
% Uneasy in last three slots (4,5,6)
:- slot(uneasy,Su), Su <= 3.
% Yardsign in first three slots (1,2,3)
:- slot(yardsign,Sy), Sy >= 4.
% Zircon immediately before Wellspring
:- slot(zircon,Sz), slot(wellspring,Sw), Sw != Sz + 1.

% Options conditions
option(a) :- slot(uneasy,5).   % A
option(b) :- slot(vegemite,1). % B
option(c) :- slot(xpert,5).    % C
option(d) :- slot(yardsign,2). % D
option(e) :- slot(zircon,3).   % E

% Force the must-be-true option and forbid others
:- not option(e).
:- option(a).
:- option(b).
:- option(c).
:- option(d).

#show option/1.