% Concert promoter problem

% Domains
slot(1..6).
band(uneasy; vegemite; wellspring; xpert; yardsign; zircon).

% Assignment: each slot gets exactly one band, each band gets exactly one slot
1 { assignment(S, B) : band(B) } 1 :- slot(S).
1 { assignment(S, B) : slot(S) } 1 :- band(B).

% Constraints
:- assignment(SV, vegemite), assignment(SZ, zircon), SV >= SZ.          % Vegemite before Zircon
:- assignment(SW, wellspring), assignment(SX, xpert), SW >= SX.        % Wellspring before Xpert
:- assignment(SZ, zircon), assignment(SX, xpert), SZ >= SX.            % Zircon before Xpert
:- assignment(SU, uneasy), SU < 4.                                     % Uneasy in last three slots
:- assignment(SY, yardsign), SY > 3.                                   % Yardsign in first three slots
:- assignment(SZ, zircon), assignment(SY, yardsign), SZ >= SY.         % Zircon before Yardsign (additional condition)

% Optimize: minimize Wellspring's slot
#minimize { S@1 : assignment(S, wellspring) }.

% Map the correct answer to option/1
% The optimal model will have Wellspring in the earliest possible slot.
option(a) :- assignment(2, wellspring).
option(b) :- assignment(3, wellspring).
option(c) :- assignment(4, wellspring).
option(d) :- assignment(5, wellspring).
option(e) :- assignment(6, wellspring).

#show option/1.