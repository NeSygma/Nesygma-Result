% Film Logic Problem - Refined
% ============================

% Domain: Films
film("hachi_dogs_tale").

% Properties of films (as choice rules to allow exploration)
{ appropriate_all_ages(F) } :- film(F).
{ excessive_content(F) } :- film(F).
{ family_friendly_animated(F) } :- film(F).
{ in_frozen_series(F) } :- film(F).
{ general_audience(F) } :- film(F).

% Premise 1: If appropriate for all ages, then children can watch without guidance
% We'll derive children_can_watch from appropriate_all_ages
children_can_watch(F) :- appropriate_all_ages(F).

% Premise 2: If contains excessive content, children cannot watch without guidance
% This means: excessive_content(F) → ¬children_can_watch(F)
% Since children_can_watch(F) is derived from appropriate_all_ages(F),
% excessive_content(F) must imply ¬appropriate_all_ages(F)
:- excessive_content(F), appropriate_all_ages(F).

% Premise 3: If rated General Audience, then appropriate for all ages
appropriate_all_ages(F) :- general_audience(F).

% Premise 4: All family-friendly animated films are rated General Audience
general_audience(F) :- family_friendly_animated(F).

% Premise 5: All movies in the Frozen series are family-friendly animated films
family_friendly_animated(F) :- in_frozen_series(F).

% Premise 6: "Hachi: A dog's Tale" is a film (already stated as fact)

% Premise 7: "Hachi: A dog's Tale" is either family-friendly animated OR appropriate for all ages
% This is a choice: at least one of these must be true
{ family_friendly_animated("hachi_dogs_tale") ; appropriate_all_ages("hachi_dogs_tale") } 1.

% Additional constraint: If family-friendly animated, then appropriate for all ages
% (This follows from premises 4 and 3)
appropriate_all_ages(F) :- family_friendly_animated(F).

% Now, let's model the conclusion
% Conclusion: (excessive_content(hachi) ∧ in_frozen_series(hachi)) ∨ (¬excessive_content(hachi) ∧ ¬in_frozen_series(hachi))
% This is equivalent to: excessive_content(hachi) ↔ in_frozen_series(hachi)

% Define the conclusion as derived atoms
conclusion_true :- excessive_content("hachi_dogs_tale"), in_frozen_series("hachi_dogs_tale").
conclusion_true :- not excessive_content("hachi_dogs_tale"), not in_frozen_series("hachi_dogs_tale").

% Define when the conclusion is false
conclusion_false :- excessive_content("hachi_dogs_tale"), not in_frozen_series("hachi_dogs_tale").
conclusion_false :- not excessive_content("hachi_dogs_tale"), in_frozen_series("hachi_dogs_tale").

% Answer mapping
answer(true) :- conclusion_true.
answer(false) :- conclusion_false.
answer(uncertain) :- not conclusion_true, not conclusion_false.
answer(inconsistent) :- conclusion_true, conclusion_false.

% Show the answer
#show answer/1.
#show film/1.
#show appropriate_all_ages/1.
#show excessive_content/1.
#show family_friendly_animated/1.
#show in_frozen_series/1.
#show general_audience/1.
#show children_can_watch/1.