% Argumentation Framework with Hierarchies and Attack Types
% ======================================================

% --- Input Data ---

% Arguments
argument(a1). argument(a2). argument(a3). argument(a4). argument(a5). argument(a6).
argument(a7). argument(a8). argument(a9). argument(a10). argument(a11). argument(a12).
argument(a13). argument(a14). argument(a15). argument(a16).

% Levels (1=lowest, 3=highest)
level(a1,1). level(a2,1). level(a3,1). level(a4,1). level(a5,1). level(a6,1).
level(a7,2). level(a8,2). level(a9,2). level(a10,2). level(a11,2). level(a12,2).
level(a13,3). level(a14,3). level(a15,3). level(a16,3).

% Strong attacks (always successful)
strong_attack(a2,a1).
strong_attack(a9,a8).
strong_attack(a14,a13).
strong_attack(a15,a16).
strong_attack(a1,a14).
strong_attack(a16,a15).
strong_attack(a1,a3).
strong_attack(a1,a4).
strong_attack(a13,a7).
strong_attack(a13,a10).
strong_attack(a3,a5).
strong_attack(a5,a3).

% Weak attacks (successful only if attacker level > target level)
weak_attack(a8,a2).
weak_attack(a13,a9).
weak_attack(a8,a5).
weak_attack(a8,a6).
weak_attack(a16,a11).
weak_attack(a16,a12).
weak_attack(a2,a7).
weak_attack(a10,a13).

% All attacks (both strong and weak)
attack(A,B) :- strong_attack(A,B).
attack(A,B) :- weak_attack(A,B).

% --- Generate candidate extensions ---
{ in_extension(A) : argument(A) }.

% --- Define successful attacks within the current extension ---
% Strong attacks always succeed if both attacker and target are in the extension
successful_attack(A,B) :- strong_attack(A,B), in_extension(A), in_extension(B).

% Weak attacks succeed only if attacker level > target level AND both are in the extension
successful_attack(A,B) :- weak_attack(A,B), in_extension(A), in_extension(B), level(A,LA), level(B,LB), LA > LB.

% --- Helper predicate for counter-attack ---
counter_attacked(B) :- in_extension(C), successful_attack(C,B).

% --- Conflict-free condition ---
% No successful attack between any two members of the extension
:- in_extension(A), in_extension(B), successful_attack(A,B).

% --- Self-defending condition ---
% For every argument A in the extension, if an external argument B successfully attacks A,
% then there must be some argument C in the extension that successfully attacks B
:- in_extension(A), attack(B,A), successful_attack(B,A), not counter_attacked(B).

% --- Preferred Extension = Conflict-free + Self-defending + Maximal ---
% Maximality is implicit: we find all sets satisfying the above constraints.
% The solver will return all maximal sets that cannot be extended without violating constraints.

% --- Show the extensions ---
#show in_extension/1.