% Positive version: original conclusion as conjecture
% Conclusion: No members of Pappy's have starred in a show piloting on BBC Two or BBC Three.
% Formalized: ! [X, Y] : ((member_of_pappys(X) & stars_in(X, Y) & pilots_on(Y, Z) & (Z = bbc_two | Z = bbc_three)) => $false)
% Equivalently: ~? [X, Y, Z] : (member_of_pappys(X) & stars_in(X, Y) & pilots_on(Y, Z) & (Z = bbc_two | Z = bbc_three))

fof(distinct_channels, axiom, (bbc_two != bbc_three & bbc_two != bbc_three_alt & bbc_three != bbc_three_alt)).
fof(badults_is_show, axiom, badults = badults_show).  % identity for show

% Premise 1: Badults is a British Sitcom series starring members of Pappy's.
fof(premise1, axiom, ! [X] : (member_of_pappys(X) & stars_in(X, badults))).

% Premise 2: Badults was piloted in July 2013 on BBC Three.
fof(premise2, axiom, pilots_on(badults, bbc_three)).

% Premise 3: The Working title "The Secret Dude Society" was used for Badults.
% (irrelevant to conclusion)

% Premise 4: Andrew Collins was the script editor for Badults.
% (irrelevant to conclusion)

% Conclusion: No members of Pappy's have starred in a show piloting on BBC Two or BBC Three.
fof(conclusion, conjecture, ~? [X, Y, Z] : (member_of_pappys(X) & stars_in(X, Y) & pilots_on(Y, Z) & (Z = bbc_two | Z = bbc_three))).