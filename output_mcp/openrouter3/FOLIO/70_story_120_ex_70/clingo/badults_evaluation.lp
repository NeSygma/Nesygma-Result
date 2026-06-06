% Premises from the problem
show(badults).
channel(bbc_two).
channel(bbc_three).

% Premise 1: Badults is a British Sitcom series starring members of Pappy's
% We need to represent members of Pappy's - since they're not named, we'll use a choice rule
{ member_of_pappys(Person) } :- show(badults), Person = person1.  % At least one member exists
starring(badults, Person) :- member_of_pappys(Person).

% Premise 2: Badults was piloted in July 2013 on BBC Three
piloted(badults, bbc_three, "July_2013").

% Premise 3: Working title (not needed for conclusion evaluation)
% Premise 4: Script editor (not needed for conclusion evaluation)

% Helper: A person stars in a show piloted on a channel
stars_in_piloted_on(Person, Channel) :-
    starring(Show, Person),
    piloted(Show, Channel, _).

% Conclusion: No members of Pappy's have starred in a show piloting on BBC Two or BBC Three
% This is equivalent to: For all members of Pappy's, they do NOT star in a show piloted on BBC Two or BBC Three
conclusion_true :-
    % If there are no members of Pappy's, the statement is vacuously true
    not member_of_pappys(_).

conclusion_true :-
    % If there are members, none of them star in a show piloted on BBC Two or BBC Three
    member_of_pappys(Person),
    not stars_in_piloted_on(Person, bbc_two),
    not stars_in_piloted_on(Person, bbc_three).

% Positive logic for False: The conclusion is false if there exists at least one member of Pappy's
% who stars in a show piloted on BBC Two or BBC Three
conclusion_false :-
    member_of_pappys(Person),
    stars_in_piloted_on(Person, bbc_two).

conclusion_false :-
    member_of_pappys(Person),
    stars_in_piloted_on(Person, bbc_three).

% Final Answer Mapping
answer(true) :- conclusion_true.
answer(false) :- conclusion_false.
answer(uncertain) :- not conclusion_true, not conclusion_false.
answer(inconsistent) :- conclusion_true, conclusion_false.

% Show relevant information
#show show/1.
#show member_of_pappys/1.
#show starring/2.
#show piloted/3.
#show stars_in_piloted_on/2.
#show conclusion_true.
#show conclusion_false.
#show answer/1.