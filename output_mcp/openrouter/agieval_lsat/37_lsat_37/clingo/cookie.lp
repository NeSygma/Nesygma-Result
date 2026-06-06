% Days are represented as numbers: 1=Mon,2=Tue,3=Wed,4=Thu,5=Fri.

% Choice of exactly one option
1 { option(a); option(b); option(c); option(d); option(e) } 1.

% Option A data
oat_day_opt(a,1). oat_day_opt(a,3). oat_day_opt(a,4).
peanut_day_opt(a,3). peanut_day_opt(a,4). peanut_day_opt(a,5).
sugar_day_opt(a,1). sugar_day_opt(a,4). sugar_day_opt(a,5).

% Option B data
oat_day_opt(b,1). oat_day_opt(b,2). oat_day_opt(b,4).
peanut_day_opt(b,2). peanut_day_opt(b,3). peanut_day_opt(b,4).
sugar_day_opt(b,1). sugar_day_opt(b,3). sugar_day_opt(b,4).

% Option C data
oat_day_opt(c,2). oat_day_opt(c,3). oat_day_opt(c,4).
peanut_day_opt(c,3). peanut_day_opt(c,4). peanut_day_opt(c,5).
sugar_day_opt(c,2). sugar_day_opt(c,4). sugar_day_opt(c,5).

% Option D data
oat_day_opt(d,1). oat_day_opt(d,2). oat_day_opt(d,4).
peanut_day_opt(d,1). peanut_day_opt(d,3). peanut_day_opt(d,4).
sugar_day_opt(d,1). sugar_day_opt(d,4). sugar_day_opt(d,5).

% Option E data
oat_day_opt(e,1). oat_day_opt(e,4). oat_day_opt(e,5).
peanut_day_opt(e,2). peanut_day_opt(e,3). peanut_day_opt(e,4).
sugar_day_opt(e,1). sugar_day_opt(e,4). sugar_day_opt(e,5).

% Map selected option to concrete schedule
day_of(oatmeal, D) :- option(X), oat_day_opt(X, D).
day_of(peanut, D) :- option(X), peanut_day_opt(X, D).
day_of(sugar, D) :- option(X), sugar_day_opt(X, D).

% Ensure each kind has exactly three days (redundant but safe)
:- N = #count { D : day_of(oatmeal, D) }, N != 3.
:- N = #count { D : day_of(peanut, D) }, N != 3.
:- N = #count { D : day_of(sugar, D) }, N != 3.

% At least one batch on Monday (day 1)
:- not day_of(_, 1).

% Define ordering positions for each kind
first(K, D) :- day_of(K, D), N = #count { D2 : day_of(K, D2), D2 < D }, N = 0.
second(K, D) :- day_of(K, D), N = #count { D2 : day_of(K, D2), D2 < D }, N = 1.
third(K, D) :- day_of(K, D), N = #count { D2 : day_of(K, D2), D2 < D }, N = 2.

% Constraint: Oatmeal second batch day equals Peanut first batch day
:- second(oatmeal, D1), first(peanut, D2), D1 != D2.

% Constraint: Sugar second batch must be Thursday (day 4)
:- second(sugar, D), D != 4.

% Show which option is possible
option(a) :- option(a).
option(b) :- option(b).
option(c) :- option(c).
option(d) :- option(d).
option(e) :- option(e).

#show option/1.