% Domain facts
pos_range(1). pos_range(2). pos_range(3). pos_range(4). pos_range(5). pos_range(6). pos_range(7).

% Persons
person(peters). person(quinn). person(rovero). person(stanton). person(tao). person(villas). person(white).

% Bijection constraints
1 { pos(Person,Pos) : pos_range(Pos) } 1 :- person(Person).
1 { pos(Person,Pos) : person(Person) } 1 :- pos_range(Pos).

% Fixed positions
pos(peters,4). pos(tao,2).

% Constraints
:- pos(stanton,1). :- pos(stanton,3).
:- pos(quinn,PosQ), pos(rovero,PosR), PosQ >= PosR.
:- pos(villas,PosV), pos(white,PosW), PosV+1 != PosW.

% Map the correct answer to option/1 (MANDATORY)
option(a) :- pos(quinn,3).
option(b) :- pos(rovero,5).
option(c) :- pos(stanton,6).
option(d) :- pos(villas,6).
option(e) :- pos(white,3).

% Ensure exactly one option is true
1 { option(a); option(b); option(c); option(d); option(e) } 1.

#show option/1.