% ... add base constraints and rules ...

employee(robertson). employee(souza). employee(togowa). employee(vaughn). employee(xu). employee(young).

space(1). space(2). space(3). space(4). space(5). space(6).

% Each employee gets exactly one space
1 { assign(E,S) : space(S) } 1 :- employee(E).
% Each space assigned to exactly one employee
1 { assign(E,S) : employee(E) } 1 :- space(S).

% Constraints
:- assign(young,S1), assign(togowa,S2), S1 <= S2.
:- assign(xu,S1), assign(souza,S2), S1 <= S2.
:- assign(robertson,S1), assign(young,S2), S1 <= S2.
:- assign(robertson,S), S > 4.
% Assumption: Togowa > Souza
:- assign(togowa,S1), assign(souza,S2), S1 <= S2.

% Force young=2
assign(young,2).

#show assign/2.