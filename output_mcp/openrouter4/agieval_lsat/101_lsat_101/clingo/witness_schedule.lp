% Exactly five witnesses
witness(franco; garcia; hong; iturbe; jackson).

% Three days
day(mon; tue; wed).

% Each witness testifies on exactly one day
1 { assigned(W, D) : day(D) } 1 :- witness(W).

% Constraint 1: Franco and Garcia not same day
:- assigned(franco, D), assigned(garcia, D).

% Constraint 2: Iturbe testifies on Wednesday
assigned(iturbe, wed).

% Constraint 3: Exactly two witnesses on Tuesday
:- #count { W : assigned(W, tue) } != 2.

% Constraint 4: Hong does not testify on Monday
:- assigned(hong, mon).

% Constraint 5: At least one witness on Monday
:- #count { W : assigned(W, mon) } = 0.

% Additional: Jackson is the only witness scheduled to testify on Monday
assigned(jackson, mon).
:- assigned(W, mon), W != jackson.

% Show the schedule
#show assigned/2.

% Define which options hold in this model
option_a_holds :- assigned(franco, wed).
option_b_holds :- assigned(hong, tue).
option_c_holds :- assigned(garcia, tue).
option_d_holds :- assigned(franco, D), assigned(hong, D).
option_e_holds :- assigned(garcia, D), assigned(hong, D).

#show option_a_holds/0.
#show option_b_holds/0.
#show option_c_holds/0.
#show option_d_holds/0.
#show option_e_holds/0.