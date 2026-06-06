% Define the time horizon (not strictly necessary here, but useful for planning-like problems)
time(0..1).

% --- Arguments and Levels ---
argument(a1). argument(a2). argument(a3). argument(a4). argument(a5).
argument(a6). argument(a7). argument(a8). argument(a9). argument(a10).
argument(a11). argument(a12). argument(a13). argument(a14). argument(a15). argument(a16).

% Level assignments
level(a1,1). level(a2,1). level(a3,1). level(a4,1). level(a5,1). level(a6,1).
level(a7,2). level(a8,2). level(a9,2). level(a10,2). level(a11,2). level(a12,2).
level(a13,3). level(a14,3). level(a15,3). level(a16,3).

% --- Strong Attacks (always successful) ---
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

% --- Weak Attacks (successful only if attacker level > target level) ---
weak_attack(a8,a2).
weak_attack(a13,a9).
weak_attack(a8,a5).
weak_attack(a8,a6).
weak_attack(a16,a11).
weak_attack(a16,a12).
weak_attack(a2,a7).
weak_attack(a10,a13).

% --- Helper: All attacks (strong or weak) ---
attack(X,Y) :- strong_attack(X,Y).
attack(X,Y) :- weak_attack(X,Y).

% --- Helper: Successful attack (strong always succeeds, weak succeeds if level(X) > level(Y)) ---
successful_attack(X,Y) :- strong_attack(X,Y).
successful_attack(X,Y) :- weak_attack(X,Y), level(X,LX), level(Y,LY), LX > LY.

% --- Choice Rule: Generate candidate extensions ---
{ in_extension(X) : argument(X) }.

% --- Conflict-Free: No two arguments in the extension have a successful attack between them ---
:- in_extension(X), in_extension(Y), X != Y, successful_attack(X,Y).

% --- Self-Defending: For every external successful attack on an extension member, there is a counter-attack from within the extension ---
:- in_extension(Y), argument(X), successful_attack(X,Y), not in_extension(X), not counter_attacked(X,Y).

counter_attacked(X,Y) :- in_extension(Z), successful_attack(Z,X), argument(Y).

% --- Show the extensions ---
#show in_extension/1.