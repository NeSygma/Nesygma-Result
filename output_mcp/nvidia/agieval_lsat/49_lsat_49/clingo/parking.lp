emp(robertson). emp(souza). emp(togowa). emp(vaughn). emp(xu). emp(young).
space(1). space(2). space(3). space(4). space(5). space(6).

{ assigned(E,S) : space(S) } 1 :- emp(E).
{ assigned(E,S) : emp(E) } 1 :- space(S).

allowed_R(1). allowed_R(2). allowed_R(3). allowed_R(4).
{ assigned(robertson,R) : allowed_R(R) } 1.

:- assigned(young,Y), assigned(togowa,T), Y <= T.
:- assigned(xu,X), assigned(souza,S), X <= S.
:- assigned(robertson,R), assigned(young,Y), R <= Y.
:- assigned(togowa,T), assigned(souza,S), T <= S.

option(a) :- assigned(young,2).
option(b) :- assigned(vaughn,5).
option(c) :- assigned(togowa,3).
option(d) :- assigned(souza,2).
option(e) :- assigned(robertson,3).

#show option/1.