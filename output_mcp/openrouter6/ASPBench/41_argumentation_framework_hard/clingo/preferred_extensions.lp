% Abstract Argumentation Framework with Hierarchies and Attack Types
% Find all preferred extensions (maximal admissible sets)

% 1. Define arguments and their levels
argument(a1). argument(a2). argument(a3). argument(a4). argument(a5). argument(a6).
argument(a7). argument(a8). argument(a9). argument(a10). argument(a11). argument(a12).
argument(a13). argument(a14). argument(a15). argument(a16).

level(1, a1). level(1, a2). level(1, a3). level(1, a4). level(1, a5). level(1, a6).
level(2, a7). level(2, a8). level(2, a9). level(2, a10). level(2, a11). level(2, a12).
level(3, a13). level(3, a14). level(3, a15). level(3, a16).

% 2. Define attacks
% Strong attacks (always successful)
strong_attack(a2, a1). strong_attack(a9, a8). strong_attack(a14, a13). strong_attack(a15, a16).
strong_attack(a1, a14). strong_attack(a16, a15). strong_attack(a1, a3). strong_attack(a1, a4).
strong_attack(a13, a7). strong_attack(a13, a10). strong_attack(a3, a5). strong_attack(a5, a3).

% Weak attacks (successful only if attacker level > target level)
weak_attack(a8, a2). weak_attack(a13, a9). weak_attack(a8, a5). weak_attack(a8, a6).
weak_attack(a16, a11). weak_attack(a16, a12). weak_attack(a2, a7). weak_attack(a10, a13).

% 3. Define successful attacks
successful_attack(A, B) :- strong_attack(A, B).
successful_attack(A, B) :- weak_attack(A, B), level(LA, A), level(LB, B), LA > LB.

% 4. Define extension (choice rule for any subset of arguments)
{ in_ext(A) : argument(A) }.

% 5. Conflict-free constraint: No successful attacks between members
:- in_ext(A), in_ext(B), A != B, successful_attack(A, B).

% 6. Self-defending constraint
% For every member A and external attacker B, B must be defended
% B is defended if some member attacks B
defended(B) :- in_ext(C), successful_attack(C, B).
:- in_ext(A), not in_ext(B), successful_attack(B, A), not defended(B).

% 7. Maximality: No external argument can be added while preserving admissibility
% For any argument X not in extension, adding X would violate conflict-free or self-defending
% We encode this by requiring that for each X not in extension, at least one of the following holds:
%   a) X attacks some member (conflict-free violation)
%   b) Some member attacks X (conflict-free violation)
%   c) X is attacked by some external B that is not defended (self-defending violation)
%   d) X attacks some external B that is not defended (self-defending violation for B)
% Actually, simpler: The set in_ext ∪ {X} is not admissible.
% We can check this by requiring that for each X not in extension, either:
%   - X attacks some member (conflict-free violation)
%   - Some member attacks X (conflict-free violation)
%   - There exists some A in in_ext ∪ {X} and some B not in in_ext ∪ {X} such that B attacks A and no member attacks B.
% This is complex. Let's use a different approach: define admissible sets and ensure maximality.

% Let's define admissible sets as those satisfying conflict-free and self-defending.
% Then preferred extensions are maximal admissible sets.

% We'll use a helper predicate to check if a set is admissible.
% But we need to check maximality: for any X not in extension, the set is not admissible.
% We can encode this by requiring that for each X not in extension, adding X violates either conflict-free or self-defending.

% For each X not in extension, check if adding X would keep conflict-free:
%   X must not attack any member, and no member must attack X.
% If that holds, then check self-defending: for every A in extension ∪ {X} and every B not in extension ∪ {X} that attacks A, there must be a defender.
% If both hold, then X can be added, violating maximality.

% So maximality constraint: For each X not in extension, it is NOT the case that both:
%   (i) X does not attack any member and no member attacks X
%   (ii) For all A in extension ∪ {X} and all B not in extension ∪ {X}, if B attacks A then there is a defender in extension ∪ {X}.

% We'll encode this with helper predicates.

% Helper: X is conflict-free with extension (i.e., adding X doesn't cause conflict-free violation)
conflict_free_with_ext(X) :-
    argument(X), not in_ext(X),
    not (in_ext(Y), successful_attack(X, Y)),
    not (in_ext(Y), successful_attack(Y, X)).

% Helper: For a given X, check self-defending of extension ∪ {X}
% We need to check for all A in extension ∪ {X} and all B not in extension ∪ {X}
% If B attacks A, then there must be a defender in extension ∪ {X}.
% We'll define a predicate that holds if self-defending is satisfied for extension ∪ {X}.
self_defending_with_ext(X) :-
    argument(X), not in_ext(X),
    % For all A in extension ∪ {X}
    (in_ext(A) ; A = X),
    % For all B not in extension ∪ {X}
    argument(B), not in_ext(B), B != X,
    % If B attacks A, then there must be a defender
    successful_attack(B, A),
    #count{C : (in_ext(C) ; C = X), successful_attack(C, B)} > 0.

% But the above rule is not correct because it requires that for every A and B, if B attacks A then there is a defender.
% Actually, the rule should be: if there exists some A and B such that B attacks A and no defender, then self_defending_with_ext fails.
% So we need a constraint that says: if there exists A, B such that B attacks A and no defender, then self_defending_with_ext is false.
% We can encode this as: self_defending_with_ext(X) holds if there is no such A, B.

% Let's define a predicate that holds if there is a violation for extension ∪ {X}.
violation(X) :-
    argument(X), not in_ext(X),
    % Conflict-free violation
    ( (in_ext(Y), successful_attack(X, Y)) ; (in_ext(Y), successful_attack(Y, X)) ).

violation(X) :-
    argument(X), not in_ext(X),
    % Self-defending violation: there exists A in extension ∪ {X} and B not in extension ∪ {X} such that B attacks A and no defender
    (in_ext(A) ; A = X),
    argument(B), not in_ext(B), B != X,
    successful_attack(B, A),
    #count{C : (in_ext(C) ; C = X), successful_attack(C, B)} = 0.

% Maximality: For every X not in extension, violation(X) must hold (i.e., adding X would violate admissibility)
:- argument(X), not in_ext(X), not violation(X).

% 8. Output the extension
#show in_ext/1.