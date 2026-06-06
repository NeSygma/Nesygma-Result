% Bands
band(uneasy). band(vegemite). band(wellspring). band(xpert). band(yardsign). band(zircon).

% Slots
slotnum(1..6).

% Assign each band to exactly one slot
1 { slot(B,S) : slotnum(S) } 1 :- band(B).
% No two bands share a slot
:- slot(B1,S), slot(B2,S), B1 != B2.

% Constraints
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

% Counterexample A: Uneasy not in slot 5
{use_a}.
:- use_a, slot(uneasy,5).
counterexample_a :- use_a.

% Counterexample B: Vegemite not in slot 1
{use_b}.
:- use_b, slot(vegemite,1).
counterexample_b :- use_b.

% Counterexample C: Xpert not in slot 5
{use_c}.
:- use_c, slot(xpert,5).
counterexample_c :- use_c.

% Counterexample D: Yardsign not in slot 2
{use_d}.
:- use_d, slot(yardsign,2).
counterexample_d :- use_d.

% Counterexample E: Zircon not in slot 3
{use_e}.
:- use_e, slot(zircon,3).
counterexample_e :- use_e.

% Options mapping: an option is true if its counterexample cannot be realized
option(a) :- not counterexample_a.
option(b) :- not counterexample_b.
option(c) :- not counterexample_c.
option(d) :- not counterexample_d.
option(e) :- not counterexample_e.

#show option/1.