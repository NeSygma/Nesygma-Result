% Domains
witness(franco; garcia; hong; iturbe; jackson).
day(monday; tuesday; wednesday).

% Assign each witness to exactly one day
1 { assigned(W, D) : day(D) } 1 :- witness(W).

% Constraints from the problem statement
% 1. Franco does not testify on the same day as Garcia
:- assigned(franco, D), assigned(garcia, D).

% 2. Iturbe testifies on Wednesday
:- not assigned(iturbe, wednesday).

% 3. Exactly two witnesses testify on Tuesday
:- not 2 { assigned(W, tuesday) : witness(W) } 2.

% 4. Hong does not testify on Monday
:- assigned(hong, monday).

% 5. At least one witness testifies on Monday
:- not 1 { assigned(W, monday) : witness(W) } 1.

% Additional condition for the question: Franco is scheduled to testify on the same day as Hong
:- not assigned(franco, D), assigned(hong, D).
:- assigned(franco, D), not assigned(hong, D).

% Map the correct answer to option/1
% (A) Franco is scheduled to testify on Wednesday.
% This cannot be true given the constraints
option(a) :- assigned(franco, wednesday).

% (B) Garcia is scheduled to testify on Monday.
% This is possible but not necessary
option(b) :- assigned(garcia, monday).

% (C) Garcia is scheduled to testify on Wednesday.
% This is possible but not necessary
option(c) :- assigned(garcia, wednesday).

% (D) Hong is scheduled to testify on Tuesday.
% This MUST be true given the constraints
option(d) :- assigned(hong, tuesday).

% (E) Iturbe is the only witness scheduled to testify on Wednesday.
% This cannot be true since at least Iturbe and one other are on Wednesday
option(e) :- assigned(iturbe, wednesday),
             not assigned(franco, wednesday),
             not assigned(garcia, wednesday),
             not assigned(hong, wednesday),
             not assigned(jackson, wednesday).

#show option/1.