fof(seasons, axiom, (season(spring) & season(summer) & season(fall) & season(winter))).
fof(distinct_seasons, axiom, (spring != summer & spring != fall & spring != winter & summer != fall & summer != winter & fall != winter)).
fof(distinct_people, axiom, (emma != mia & emma != james & mia != james)).
fof(student_emma, axiom, student(emma)).
fof(student_mia, axiom, student(mia)).
fof(student_james, axiom, student(james)).
fof(long_vacation_rule, axiom, ! [X] : ((student(X) & wants_long_vacation(X)) => favorite_season(X, summer))).
fof(emma_fav, axiom, favorite_season(emma, summer)).
fof(mia_not_same_as_emma, axiom, ! [S] : (favorite_season(emma, S) => ~favorite_season(mia, S))).
fof(james_wants, axiom, wants_long_vacation(james)).
fof(goal, conjecture, ~favorite_season(mia, spring)).