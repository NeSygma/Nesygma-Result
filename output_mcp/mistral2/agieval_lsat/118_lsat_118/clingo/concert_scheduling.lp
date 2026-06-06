% Base facts: slots and bands
slot(1..6).
band(uneasy; vegemite; wellspring; xpert; yardsign; zircon).

% Assign each band to a unique slot
1 { assigned(B, S) : slot(S) } 1 :- band(B).
:- assigned(B1, S), assigned(B2, S), B1 != B2.

% Constraints from the problem statement
% 1. Vegemite performs in an earlier slot than Zircon
:- assigned(vegemite, S1), assigned(zircon, S2), S1 >= S2.

% 2. Wellspring and Zircon each perform in an earlier slot than Xpert
:- assigned(wellspring, S1), assigned(xpert, S2), S1 >= S2.
:- assigned(zircon, S1), assigned(xpert, S2), S1 >= S2.

% 3. Uneasy performs in one of the last three slots
:- assigned(uneasy, S), S < 4.

% 4. Yardsign performs in one of the first three slots
:- assigned(yardsign, S), S > 3.

% Additional constraint: Vegemite performs in slot three
:- assigned(vegemite, S), S != 3.
assigned(vegemite, 3).

% Helper predicates for answer choices
% (A) Uneasy performs in an earlier slot than Xpert
answer_a :- assigned(uneasy, S1), assigned(xpert, S2), S1 < S2.

% (B) Wellspring performs in an earlier slot than Zircon
answer_b :- assigned(wellspring, S1), assigned(zircon, S2), S1 < S2.

% (C) Xpert performs in an earlier slot than Uneasy
answer_c :- assigned(xpert, S1), assigned(uneasy, S2), S1 < S2.

% (D) Yardsign performs in an earlier slot than Wellspring
answer_d :- assigned(yardsign, S1), assigned(wellspring, S2), S1 < S2.

% (E) Zircon performs in an earlier slot than Uneasy
answer_e :- assigned(zircon, S1), assigned(uneasy, S2), S1 < S2.

% Map the correct answer to option/1
option(a) :- answer_a.
option(b) :- answer_b.
option(c) :- answer_c.
option(d) :- answer_d.
option(e) :- answer_e.

#show option/1.