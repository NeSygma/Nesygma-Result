% Domains
pos(1). pos(2). pos(3). pos(4). pos(5). pos(6).

% Car types
type(a). type(b). type(c).

% Exactly one type per position
1 { type(Pos, T) : type(T) } 1 :- pos(Pos).

% Count constraints for each type
#count { Pos : type(Pos, a) } = 1.
#count { Pos : type(Pos, b) } = 2.
#count { Pos : type(Pos, c) } = 3.

% Option definitions
opt1(Pos) :- type(Pos, a).   % A has option1
opt1(Pos) :- type(Pos, c).   % C has option1
opt2(Pos) :- type(Pos, a).   % A has option2
opt3(Pos) :- type(Pos, b).   % B has option3

% Sliding window constraints for option1 (max 2 in any 3 consecutive)
:- opt1(1), opt1(2), opt1(3).
:- opt1(2), opt1(3), opt1(4).
:- opt1(3), opt1(4), opt1(5).
:- opt1(4), opt1(5), opt1(6).

% Sliding window constraints for option2 (max 1 in any 2 consecutive)
:- opt2(1), opt2(2).
:- opt2(2), opt2(3).
:- opt2(3), opt2(4).
:- opt2(4), opt2(5).
:- opt2(5), opt2(6).

% Sliding window constraints for option3 (max 1 in any 2 consecutive)
:- opt3(1), opt3(2).
:- opt3(2), opt3(3).
:- opt3(3), opt3(4).
:- opt3(4), opt3(5).
:- opt3(5), opt3(6).

% Show solution
#show type/2.
#show opt1/1.
#show opt2/1.
#show opt3/1.