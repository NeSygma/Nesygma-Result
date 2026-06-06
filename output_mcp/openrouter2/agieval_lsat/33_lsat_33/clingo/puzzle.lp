% Domain facts
bay(1). bay(2). bay(3). bay(4). bay(5). bay(6).
cargo(fuel). cargo(grain). cargo(livestock). cargo(machinery). cargo(produce). cargo(textiles).

% Assignment: each bay has exactly one cargo, each cargo assigned to exactly one bay
1 { assigned(B,C) : cargo(C) } 1 :- bay(B).
1 { assigned(B,C) : bay(B) } 1 :- cargo(C).

% Constraints
% grain > livestock
:- assigned(B1,grain), assigned(B2,livestock), B1 <= B2.
% livestock > textiles
:- assigned(B2,livestock), assigned(B3,textiles), B2 <= B3.
% produce > fuel
:- assigned(B4,produce), assigned(B5,fuel), B4 <= B5.
% textiles adjacent to produce
:- assigned(B3,textiles), assigned(B4,produce), B3+1 != B4, B3-1 != B4.

% Force livestock at bay 5
:- not assigned(5,livestock).

% Map options
option(a) :- assigned(1,livestock).
option(b) :- assigned(2,livestock).
option(c) :- assigned(3,livestock).
option(d) :- assigned(5,livestock).
option(e) :- assigned(6,livestock).

#show option/1.