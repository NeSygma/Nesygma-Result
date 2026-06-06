% Facts
rep(kim). rep(mahr). rep(parra). rep(quinn). rep(stuckey). rep(tiao). rep(udall).

% Each rep assigned to exactly one zone
1 { zone(Rep, 1); zone(Rep, 2); zone(Rep, 3) } 1 :- rep(Rep).

% Exactly one of Parra or Tiao in Zone 1
1 { zone(parra, 1); zone(tiao, 1) } 1.

% Exactly one of Tiao or Udall in Zone 2
1 { zone(tiao, 2); zone(udall, 2) } 1.

% Parra and Quinn same zone
zone(parra, Z) :- zone(quinn, Z).
zone(quinn, Z) :- zone(parra, Z).

% Stuckey and Udall same zone
zone(stuckey, Z) :- zone(udall, Z).
zone(udall, Z) :- zone(stuckey, Z).

% Mahr and Stuckey same zone (assumption)
zone(mahr, Z) :- zone(stuckey, Z).
zone(stuckey, Z) :- zone(mahr, Z).

% More reps in Zone 3 than Zone 2
:- #count{Rep : zone(Rep, 3)} <= #count{Rep : zone(Rep, 2)}.

% Choice atoms for each answer
choiceA :- zone(kim, 2).
choiceB :- zone(mahr, 1).
choiceC :- zone(parra, 3).
choiceD :- zone(stuckey, 2).
choiceE :- zone(tiao, 1).

% Option selection
1 { option(a); option(b); option(c); option(d); option(e) } 1.

% Option must be consistent with choice
:- option(a), not choiceA.
:- option(b), not choiceB.
:- option(c), not choiceC.
:- option(d), not choiceD.
:- option(e), not choiceE.

#show option/1.