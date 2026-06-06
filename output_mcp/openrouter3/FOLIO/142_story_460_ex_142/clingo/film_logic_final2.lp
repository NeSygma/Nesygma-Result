% Film Logic Problem - Final
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
% This is an exclusive OR (either...or typically means exclusive in logic problems)
% But if it's family-friendly animated, it's automatically appropriate for all ages (by premises 4 and 3)
% So if it's family-friendly animated, it's both, which violates exclusive OR
% Therefore, Hachi cannot be family-friendly animated if premise 7 is exclusive OR
% Let's model exclusive OR: exactly one of these must be true
% 1 { family_friendly_animated("hachi_dogs_tale"), appropriate_all_ages("hachi_dogs_tale") } 1.

% Actually, let's re-examine the problem statement:
% "Hachi: A dog's Tale is either a family-friendly animated film or is appropriate for people of all ages."
% In natural language, "either A or B" can be inclusive or exclusive depending on context.
% Given that the conclusion uses "either...or" for an exclusive OR, let's assume premise 7 is also exclusive OR.

% But if premise 7 is exclusive OR, and family-friendly animated implies appropriate for all ages,
% then Hachi cannot be family-friendly animated. So Hachi must be appropriate for all ages but NOT family-friendly animated.

% Let's model this:
% If Hachi is family-friendly animated, then it's appropriate for all ages (by premises 4 and 3).
% But premise 7 says exactly one of {family_friendly_animated, appropriate_all_ages} is true.
% So Hachi cannot be family-friendly animated.
% Therefore, Hachi must be appropriate for all ages but NOT family-friendly animated.

% Add constraint: Hachi cannot be both family-friendly animated and appropriate for all ages
% (This follows from exclusive OR interpretation of premise 7)
:- family_friendly_animated("hachi_dogs_tale"), appropriate_all_ages("hachi_dogs_tale").

% Also, at least one must be true (inclusive OR part of exclusive OR)
% Actually, exclusive OR means exactly one is true, so we need both constraints
% But we already have the constraint that they can't both be true
% We also need to ensure at least one is true
% However, if we force at least one to be true, and they can't both be true, then exactly one is true
% But we need to be careful: if Hachi is family-friendly animated, then it's appropriate for all ages
% So we can't have family-friendly animated true without appropriate_all_ages true
% Therefore, the only way to satisfy exclusive OR is:
% family_friendly_animated(hachi) = false AND appropriate_all_ages(hachi) = true
% OR
% family_friendly_animated(hachi) = true AND appropriate_all_ages(hachi) = false (impossible due to premises 4 and 3)
% So the only consistent assignment is: family_friendly_animated(hachi) = false, appropriate_all_ages(hachi) = true

% Let's add this as a constraint
% Actually, we don't need to add it as a constraint; it will be derived from the other constraints
% But we need to ensure that at least one of the two is true (from premise 7)
% However, if we don't force it, Clingo might make both false, which would violate premise 7
% So we need to force at least one to be true
% But if we force at least one to be true, and we have the constraint that they can't both be true,
% then we have exclusive OR

% Force at least one to be true
% But we can't use { ... } 1 because that would allow both to be true
% Instead, we use a constraint that forbids both being false
:- not appropriate_all_ages("hachi_dogs_tale"), not family_friendly_animated("hachi_dogs_tale").

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