%% Problem: Bakery cookies scheduling
%% 3 kinds: oatmeal, peanut_butter, sugar
%% 3 batches of each kind per week (Mon-Fri)
%% Each batch made on a single day
%% Conditions:
%% 1. No two batches of same kind on same day
%% 2. At least one batch on Monday
%% 3. Second batch of oatmeal = same day as first batch of peanut butter
%% 4. Second batch of sugar cookies is on Thursday
%% Additional: No batch on Wednesday
%% Q: Which must be true?

%% Days of the week (Monday through Friday)
day(mon; tue; wed; thu; fri).

%% Cookie kinds
kind(oatmeal; peanut_butter; sugar).

%% Batch numbers 1,2,3 for each kind
batch(1..3).

%% Each batch of each kind is assigned to exactly one day
{ assigned(Kind, Batch, Day) : day(Day) } 1 :- kind(Kind), batch(Batch).

%% Exactly 3 batches of each kind (already enforced by choice rule above)

%% Condition 1: No two batches of same kind on same day
:- assigned(K, B1, D), assigned(K, B2, D), B1 != B2.

%% Condition 2: At least one batch on Monday
:- not assigned(_, _, mon).

%% Condition 3: Second batch of oatmeal = same day as first batch of peanut butter
:- assigned(oatmeal, 2, D1), assigned(peanut_butter, 1, D2), D1 != D2.

%% Condition 4: Second batch of sugar cookies is on Thursday
assigned(sugar, 2, thu).

%% Additional condition: No batch on Wednesday
:- assigned(_, _, wed).

%% Now evaluate the options under this scenario.
%% We need to determine what MUST be true.

%% Option A: Exactly three batches of cookies are made on Tuesday.
%% Count batches on Tuesday
tue_count(N) :- N = #count{K,B : assigned(K,B,tue)}.

%% Option B: Exactly three batches of cookies are made on Friday.
fri_count(N) :- N = #count{K,B : assigned(K,B,fri)}.

%% Option C: At least two batches of cookies are made on Monday.
mon_count(N) :- N = #count{K,B : assigned(K,B,mon)}.

%% Option D: At least two batches of cookies are made on Thursday.
thu_count(N) :- N = #count{K,B : assigned(K,B,thu)}.

%% Option E: Fewer batches on Monday than on Tuesday.
fewer_mon_tue :- mon_count(M), tue_count(T), M < T.

%% Now we need to determine which option MUST be true in ALL valid models.
%% We'll use a "must_be_true" approach: an option is forced if its negation leads to unsat.

%% We'll compute all answer sets and check each option.
%% But since we need a single answer, we can use constraints to test each option.

%% Let's use a different approach: compute all possible models and see what's forced.
%% We'll use #show to see the counts.

#show assigned/3.
#show mon_count/1.
#show tue_count/1.
#show thu_count/1.
#show fri_count/1.
#show fewer_mon_tue/1.