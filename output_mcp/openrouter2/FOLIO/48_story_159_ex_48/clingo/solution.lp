% Facts
season(spring). season(summer). season(fall). season(winter).
student(emma). student(mia). student(james).

% Long vacation desire
longvac(james).

% Favorite season facts
favorite(emma, summer).

% Rule: longvac -> favorite summer
favorite(Stu, summer) :- longvac(Stu).

% Choice rule for Mia's favorite season: exactly one season, not summer
{ favorite(mia, S) : season(S), S != summer } 1 :- student(mia).

% Ensure each student has exactly one favorite season
1 { favorite(Stu, S) : season(S) } 1 :- student(Stu).

% Conclusion evaluation
answer(true) :- conclusion_true.
answer(false) :- conclusion_false.
answer(uncertain) :- not conclusion_true, not conclusion_false.

#show answer/1.