% Domains
pos(1). pos(2). pos(3). pos(4). pos(5). pos(6).

% Each position gets exactly one car type
1 { car_type(Pos, a), car_type(Pos, b), car_type(Pos, c) } :- pos(Pos).

% Global counts: exactly 1 A, 2 B, 3 C
1..1 { car_type(Pos, a) : pos(Pos) }.
2..2 { car_type(Pos, b) : pos(Pos) }.
3..3 { car_type(Pos, c) : pos(Pos) }.

% Option definitions
opt1(Pos) :- car_type(Pos, a).   % A has option1 (sunroof)
opt1(Pos) :- car_type(Pos, c).   % C has option1 (sunroof)
opt2(Pos) :- car_type(Pos, a).   % A has option2 (leather)
opt3(Pos) :- car_type(Pos, b).   % B has option3 (GPS)

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
#show car_type/2.
#show opt1/1.
#show opt2/1.
#show opt3/1.