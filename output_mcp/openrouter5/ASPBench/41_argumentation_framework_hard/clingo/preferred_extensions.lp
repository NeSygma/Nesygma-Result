%% Instance Data: Arguments and Levels
arg(a1; a2; a3; a4; a5; a6; a7; a8; a9; a10; a11; a12; a13; a14; a15; a16).

level(a1,1). level(a2,1). level(a3,1). level(a4,1). level(a5,1). level(a6,1).
level(a7,2). level(a8,2). level(a9,2). level(a10,2). level(a11,2). level(a12,2).
level(a13,3). level(a14,3). level(a15,3). level(a16,3).

%% Strong Attacks (always successful)
strong_attack(a2,a1). strong_attack(a9,a8). strong_attack(a14,a13). strong_attack(a15,a16).
strong_attack(a1,a14). strong_attack(a16,a15). strong_attack(a1,a3). strong_attack(a1,a4).
strong_attack(a13,a7). strong_attack(a13,a10). strong_attack(a3,a5). strong_attack(a5,a3).

%% Weak Attacks (successful only if attacker level > target level)
weak_attack(a8,a2). weak_attack(a13,a9). weak_attack(a8,a5). weak_attack(a8,a6).
weak_attack(a16,a11). weak_attack(a16,a12). weak_attack(a2,a7). weak_attack(a10,a13).

%% Derive successful attacks
successful_attack(A,B) :- strong_attack(A,B).
successful_attack(A,B) :- weak_attack(A,B), level(A,LA), level(B,LB), LA > LB.

%% Choice: which arguments are in the extension
{ in_ext(A) } :- arg(A).

%% Condition 1: Conflict-Free
:- in_ext(A), in_ext(B), successful_attack(A,B).

%% Condition 2: Self-Defending
%% For every A in_ext and every B not in_ext with successful_attack(B,A),
%% there must exist C in_ext with successful_attack(C,B).
defended_against(B) :- in_ext(C), successful_attack(C,B).
:- in_ext(A), arg(B), not in_ext(B), successful_attack(B,A), not defended_against(B).

%% Condition 3: Maximal Admissible (Preferred Extension)
%% Check if there exists X not in in_ext such that in_ext U {X} is admissible.

%% X conflicts with the extension if X attacks or is attacked by a member
conflict_with_ext(X) :- in_ext(A), successful_attack(X,A).
conflict_with_ext(X) :- in_ext(A), successful_attack(A,X).

%% X self-attacks
self_attack(X) :- successful_attack(X,X).

%% For defense: For each attacker Y of any member M in in_ext U {X},
%% there must be a defender D in in_ext U {X} that attacks Y.

%% Y attacks some member M in in_ext, and no one in in_ext U {X} defends against Y
undefended_attack_in_ext(X,Y) :-
    in_ext(M),
    successful_attack(Y,M),
    arg(Y), not in_ext(Y), Y != X,
    not in_ext(C), successful_attack(C,Y),
    not successful_attack(X,Y).

%% Y attacks X, and no one in in_ext U {X} defends against Y
undefended_attack_on_X(X,Y) :-
    successful_attack(Y,X),
    arg(Y), not in_ext(Y), Y != X,
    not in_ext(C), successful_attack(C,Y),
    not successful_attack(X,Y).

%% X is addable if no conflict, no self-attack, and no undefended attacks
addable(X) :-
    arg(X), not in_ext(X),
    not conflict_with_ext(X),
    not self_attack(X),
    not undefended_attack_in_ext(X,_),
    not undefended_attack_on_X(X,_).

%% If any X is addable, the extension is not maximal
not_maximal :- addable(X).

%% The extension must be maximal
:- not_maximal.

%% Show the extension
#show in_ext/1.