% Premises from the problem
show(badults).
channel(bbc_two).
channel(bbc_three).

% Premise 1: Badults is a British Sitcom series starring members of Pappy's
% Since the premise states "members" (plural), we need at least one member
% We'll use a choice rule but with a constraint to ensure at least one exists
{ member_of_pappys(Person) } :- show(badults), Person = person1.
% Constraint: At least one member of Pappy's must exist (from premise 1)
:- not member_of_pappys(_).

% Premise 1 continued: Badults stars members of Pappy's
starring(badults, Person) :- member_of_pappys(Person).

% Premise 2: Badults was piloted in July 2013 on BBC Three
piloted(badults, bbc_three, "July_2013").

% Helper: A person stars in a show piloted on a channel
stars_in_piloted_on(Person, Channel) :-
    starring(Show, Person),
    piloted(Show, Channel, _).

% Conclusion evaluation:
% "No members of Pappy's have starred in a show piloting on BBC Two or BBC Three"
% This is a universal negative statement.

% Positive logic for True: The conclusion is true if there are no members of Pappy's
% OR if there are members but none of them star in a show piloted on BBC Two or BBC Three
conclusion_true :-
    % Either no members exist (vacuously true)
    not member_of_pappys(_).

conclusion_true :-
    % Or there are members but none star in a show piloted on BBC Two or BBC Three
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