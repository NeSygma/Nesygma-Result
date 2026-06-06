% Minimal test - just person and type assignment
person(alice; bob; charlie; diana; ethan; fiona; george; hannah).
1 { type(P, "knight"); type(P, "knave") } 1 :- person(P).

groupA_knights(N) :- N = #count { P : person(P), type(P, "knight") }.

#show type/2.
#show groupA_knights/1.