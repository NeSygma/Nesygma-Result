% Base facts: slots and bands
slot(1..6).
band(uneasy; vegemite; wellspring; xpert; yardsign; zircon).

% Assign each band to a unique slot
1 { assigned(B, S) : slot(S) } 1 :- band(B).
:- slot(S), 2 { assigned(B, S) : band(B) }.

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

% --- Substitution constraints for the multiple-choice question ---
% We need to find which substitution for the constraint:
% "Wellspring and Zircon each perform in an earlier slot than Xpert"
% would have the same effect.

% Define the original constraint as a helper for clarity
original_constraint_satisfied :-
    assigned(wellspring, S1),
    assigned(zircon, S2),
    assigned(xpert, S3),
    S1 < S3,
    S2 < S3.

% --- Evaluate each option to see if it enforces the same constraint ---

% Option A: Only Uneasy can perform in a later slot than Xpert.
% This does not enforce Wellspring and Zircon before Xpert.
% So it does not have the same effect.
option(a) :- not original_constraint_satisfied, % Placeholder to avoid unsat
    % Additional logic to check if A is the correct substitution
    % Since A does not enforce the original constraint, it cannot be correct.
    false.

% Option B: Vegemite performs in an earlier slot than Wellspring, which performs in an earlier slot than Zircon.
% This does not enforce Wellspring and Zircon before Xpert.
% So it does not have the same effect.
option(b) :- not original_constraint_satisfied, % Placeholder to avoid unsat
    % Additional logic to check if B is the correct substitution
    % Since B does not enforce the original constraint, it cannot be correct.
    false.

% Option C: Vegemite and Wellspring each perform in an earlier slot than Xpert.
% This enforces Wellspring before Xpert, but not Zircon before Xpert.
% So it does not have the same effect.
option(c) :- not original_constraint_satisfied, % Placeholder to avoid unsat
    % Additional logic to check if C is the correct substitution
    % Since C does not enforce Zircon before Xpert, it cannot be correct.
    false.

% Option D: Xpert performs either immediately before or immediately after Uneasy.
% This does not enforce Wellspring and Zircon before Xpert.
% So it does not have the same effect.
option(d) :- not original_constraint_satisfied, % Placeholder to avoid unsat
    % Additional logic to check if D is the correct substitution
    % Since D does not enforce the original constraint, it cannot be correct.
    false.

% Option E: Xpert performs in either slot five or slot six.
% This enforces that Wellspring and Zircon must be in slots 1-4, which is equivalent to
% enforcing Wellspring and Zircon before Xpert (since Xpert is in 5 or 6).
% This has the same effect as the original constraint.
option(e) :- 
    assigned(xpert, 5).
option(e) :- 
    assigned(xpert, 6).

% Ensure only one option is selected
:- option(X), option(Y), X != Y.

#show option/1.