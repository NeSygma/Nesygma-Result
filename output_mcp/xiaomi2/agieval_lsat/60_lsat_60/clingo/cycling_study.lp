% Domain
rider(reynaldo). rider(seamus). rider(theresa). rider(yuki).
bicycle(f). bicycle(g). bicycle(h). bicycle(j).
day(day1). day(day2).

% ============================================================
% Encode each answer option as test(Option, Rider, Bicycle, Day)
% Format: F: Rider1, Rider2 means Rider1=day1, Rider2=day2
% ============================================================

% Option A: F: Seamus, Reynaldo; G: Yuki, Seamus; H: Theresa, Yuki; J: Reynaldo, Theresa
test(a, seamus, f, day1). test(a, reynaldo, f, day2).
test(a, yuki, g, day1). test(a, seamus, g, day2).
test(a, theresa, h, day1). test(a, yuki, h, day2).
test(a, reynaldo, j, day1). test(a, theresa, j, day2).

% Option B: F: Seamus, Yuki; G: Reynaldo, Theresa; H: Yuki, Seamus; J: Theresa, Reynaldo
test(b, seamus, f, day1). test(b, yuki, f, day2).
test(b, reynaldo, g, day1). test(b, theresa, g, day2).
test(b, yuki, h, day1). test(b, seamus, h, day2).
test(b, theresa, j, day1). test(b, reynaldo, j, day2).

% Option C: F: Yuki, Seamus; G: Seamus, Reynaldo; H: Theresa, Yuki; J: Reynaldo, Theresa
test(c, yuki, f, day1). test(c, seamus, f, day2).
test(c, seamus, g, day1). test(c, reynaldo, g, day2).
test(c, theresa, h, day1). test(c, yuki, h, day2).
test(c, reynaldo, j, day1). test(c, theresa, j, day2).

% Option D: F: Yuki, Seamus; G: Theresa, Reynaldo; H: Reynaldo, Theresa; J: Seamus, Yuki
test(d, yuki, f, day1). test(d, seamus, f, day2).
test(d, theresa, g, day1). test(d, reynaldo, g, day2).
test(d, reynaldo, h, day1). test(d, theresa, h, day2).
test(d, seamus, j, day1). test(d, yuki, j, day2).

% Option E: F: Yuki, Theresa; G: Seamus, Yuki; H: Theresa, Reynaldo; J: Reynaldo, Seamus
test(e, yuki, f, day1). test(e, theresa, f, day2).
test(e, seamus, g, day1). test(e, yuki, g, day2).
test(e, theresa, h, day1). test(e, reynaldo, h, day2).
test(e, reynaldo, j, day1). test(e, seamus, j, day2).

% ============================================================
% Constraints to check for each option
% ============================================================

% Constraint 1: Reynaldo cannot test F (on either day)
violates(O) :- test(O, reynaldo, f, _).

% Constraint 2: Yuki cannot test J (on either day)
violates(O) :- test(O, yuki, j, _).

% Constraint 3: Theresa must test H on at least one day
th_tests_h(O) :- test(O, theresa, h, _).
violates(O) :- option_letter(O), not th_tests_h(O).

% Constraint 4: Yuki's day1 bicycle must be tested by Seamus on day2
yuki_day1_bike(O, B) :- test(O, yuki, B, day1).
violates(O) :- yuki_day1_bike(O, B), not test(O, seamus, B, day2).

% Constraint 5: Each rider tests a different bicycle on day2 vs day1
violates(O) :- test(O, R, B, day1), test(O, R, B, day2).

% Helper: option letters
option_letter(a). option_letter(b). option_letter(c). option_letter(d). option_letter(e).

% An option is valid if it does NOT violate any constraint
valid(O) :- option_letter(O), not violates(O).

% Map to option/1
option(O) :- valid(O).

#show option/1.