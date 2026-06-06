% Slots are numbered 1 to 6
slot(1..6).

% Bands
band(uneasy). band(vegemite). band(wellspring). band(xpert). band(yardsign). band(zircon).

% Each band performs in exactly one slot
1 { performs(B, S) : slot(S) } 1 :- band(B).

% Each slot has exactly one band
1 { performs(B, S) : band(B) } 1 :- slot(S).

% Constraints:
% 1. Vegemite performs in an earlier slot than Zircon
:- performs(vegemite, S1), performs(zircon, S2), S1 >= S2.

% 2. Wellspring and Zircon each perform in an earlier slot than Xpert
:- performs(wellspring, S1), performs(xpert, S2), S1 >= S2.
:- performs(zircon, S1), performs(xpert, S2), S1 >= S2.

% 3. Uneasy performs in one of the last three slots
:- performs(uneasy, S), S <= 3.

% 4. Yardsign performs in one of the first three slots
:- performs(yardsign, S), S > 3.

% Define what makes each band valid in slot 5
valid_uneasy_in_5   :- performs(uneasy, 5).
valid_vegemite_in_5 :- performs(vegemite, 5).
valid_wellspring_in_5 :- performs(wellspring, 5).
valid_xpert_in_5    :- performs(xpert, 5).
valid_yardsign_in_5 :- performs(yardsign, 5).
valid_zircon_in_5   :- performs(zircon, 5).

% Define constraints that would be violated if a band is in slot 5
% Uneasy in slot 5 must not violate constraints (e.g., Zircon or Xpert in slot <=5)
invalid_uneasy_in_5 :-
    performs(uneasy, 5),
    (performs(zircon, S2), S2 =< 5 ; performs(xpert, S3), S3 =< 5).

invalid_vegemite_in_5 :-
    performs(vegemite, 5),
    performs(zircon, S2), S2 =< 5.

invalid_wellspring_in_5 :-
    performs(wellspring, 5),
    performs(xpert, S2), S2 =< 5.

invalid_xpert_in_5 :-
    performs(xpert, 5).

invalid_yardsign_in_5 :-
    performs(yardsign, 5).

invalid_zircon_in_5 :-
    performs(zircon, 5),
    performs(xpert, S2), S2 =< 5.

% If a band cannot be in slot 5, then the corresponding option is true
option(a) :- not valid_uneasy_in_5.
option(b) :- not valid_vegemite_in_5.
option(c) :- not valid_wellspring_in_5.
option(d) :- not valid_xpert_in_5.
option(e) :- not valid_zircon_in_5.

#show option/1.