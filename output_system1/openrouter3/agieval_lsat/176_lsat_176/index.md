# Benchmark Report (SYSTEM1): agieval_lsat - lsat_176

**Provider:** openrouter3
**Model:** xiaomi/mimo-v2-flash
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 48.15s


 SYSTEM 1 PURE REASONING AGENT

 Query: Exactly five students—Grecia, Hakeem, Joe, Katya, and Louise—are to work at a campus art gallery during a special exhibit that runs for exactly five days, Monday through Friday. Each day is divided into two nonoverlapping shifts—first and second—with each student working exactly two shifts. Each shift is worked by exactly one of the students according to the following scheduling restrictions: No student works both shifts of any day. On two consecutive days, Louise works the second shift. On two nonconsecutive days, Grecia works the first shift. Katya works on Tuesday and Friday. Hakeem and Joe work on the same day as each other at least once. Grecia and Louise never work on the same day as each other.Q: Which one of the following must be true? Answer Choices: (A)Grecia does not work at the gallery on Tuesday. (B)Hakeem does not work at the gallery on Wednesday. (C)Joe does not work at the gallery on Tuesday. (D)Joe does not work at the gallery on Thursday. (E)Louise does not work at the gallery on Tuesday.
A: Among A through E, the answer is

Return your final answer in JSON format like this: {"answer": "A or B or C or D or E"}.


We are given a logic puzzle with 5 students (Grecia, Hakeem, Joe, Katya, Louise) and 5 days (Monday–Friday). Each day has two shifts: first and second. Each student works exactly **two shifts total**, and **no student works both shifts on the same day**.

Additional constraints:

1. **Louise works the second shift on two consecutive days.**
2. **Grecia works the first shift on two nonconsecutive days.**
3. **Katya works on Tuesday and Friday.**
4. **Hakeem and Joe work on the same day at least once.**
5. **Grecia and Louise never work on the same day.**

We are to determine which of the answer choices **must be true**.

---

### Step 1: Understand the structure

- 5 days × 2 shifts = 10 total shifts.
- 5 students × 2 shifts each = 10 shifts → all shifts are filled.
- Each day has exactly 2 different students (since no one works both shifts on a day).
- So each day is assigned to **two distinct students**, one for first shift, one for second.

We can think of each day as a pair: (First, Second)

We’ll denote the schedule as:

- Monday: (F1, S1)
- Tuesday: (F2, S2)
- Wednesday: (F3, S3)
- Thursday: (F4, S4)
- Friday: (F5, S5)

Each student appears in exactly two of these 10 positions (as either F or S), never twice in the same day.

---

### Step 2: Apply Katya’s constraint

> Katya works on Tuesday and Friday.

So Katya appears **once on Tuesday** (either first or second shift), and **once on Friday** (either first or second shift). That accounts for her two shifts.

So Katya is **not available** on Monday, Wednesday, or Thursday.

---

### Step 3: Apply Louise’s constraint

> Louise works the second shift on two **consecutive** days.

So Louise is in the **second shift** on two days that are consecutive, e.g., Mon-Tue, Tue-Wed, Wed-Thu, or Thu-Fri.

She has exactly two shifts total, so **both of her shifts are second shifts**, on consecutive days.

So Louise appears **only** on two consecutive days, both in the second shift.

Thus, Louise is **not available** on the other three days.

Also, since she only works second shift, she never works first shift.

---

### Step 4: Apply Grecia’s constraint

> Grecia works the first shift on two **nonconsecutive** days.

So Grecia’s two shifts are both **first shifts**, on nonconsecutive days.

So Grecia appears on two days (not adjacent), both in first shift.

She is not available on the other three days.

Also, Grecia and Louise **never work on the same day**.

Since Louise works on two consecutive days (second shift), Grecia **cannot** be scheduled on either of those days.

So Grecia’s two days must be among the **other three days**, and must be nonconsecutive.

But there are only 5 days total. Louise occupies 2 consecutive days. So only 3 days remain for Grecia.

From those 3 days, Grecia must pick **two nonconsecutive** days.

Let’s consider possible placements for Louise.

---

### Step 5: Consider possible placements for Louise

Louise works second shift on two consecutive days. Possible pairs:

- Mon-Tue
- Tue-Wed
- Wed-Thu
- Thu-Fri

We’ll analyze each possibility and see what constraints it imposes.

But first, recall that **Katya works on Tuesday and Friday**.

So Tuesday and Friday are **occupied by Katya** (one shift each). That means **Louise cannot work on Tuesday or Friday**, **if** that would conflict with Katya? Wait — actually, **multiple students can work on the same day**, just not the same shift. Since each day has two shifts, and Katya takes one of them (either first or second), the other shift can be someone else.

So **Louise can work on Tuesday or Friday**, as long as she takes the other shift from Katya.

But remember: **Louise only works second shift**.

So if Louise works on Tuesday, she must be **second shift**, and Katya must be **first shift** on Tuesday.

Similarly, if Louise works on Friday, she must be **second shift**, and Katya must be **first shift** on Friday.

Alternatively, if Katya is second shift on Tuesday, then Louise **cannot** work Tuesday (since Louise only does second shift, and only one person per shift).

So **Louise and Katya can share a day only if Katya is first shift and Louise is second shift**.

Same for Friday.

Now, Grecia and Louise **never share a day**, so Grecia cannot be on any day Louise works.

So Grecia’s two days must be among the days **Louise does not work**.

Also, Grecia works **first shift** on her two days.

Now, let’s consider each possible Louise pair and see what’s possible.

---

### Case 1: Louise works Mon (2nd) and Tue (2nd)

Then Louise is on Mon and Tue.

So Grecia cannot be on Mon or Tue.

Grecia must work two **nonconsecutive** days among Wed, Thu, Fri.

Possible nonconsecutive pairs from {Wed, Thu, Fri}:

- Wed and Fri → OK (nonconsecutive)
- Wed and Thu → consecutive → not allowed
- Thu and Fri → consecutive → not allowed

So only possible: **Wed and Fri**

So Grecia works first shift on Wed and Fri.

Now, Katya works on Tue and Fri.

On Friday: Grecia is first shift, Katya must be second shift (since only one per shift). OK.

On Tuesday: Louise is second shift, so Katya must be first shift on Tuesday. OK.

Now check total shifts per student:

- Louise: Mon (2nd), Tue (2nd) → done
- Grecia: Wed (1st), Fri (1st) → done
- Katya: Tue (1st), Fri (2nd) → done

Now we have used:

- Mon: 2nd = Louise → need 1st = someone (not Grecia, not Louise, not Katya) → must be Hakeem or Joe
- Tue: 1st = Katya, 2nd = Louise → done
- Wed: 1st = Grecia → need 2nd = someone (not Grecia, not Louise, not Katya) → Hakeem or Joe
- Thu: both shifts unassigned → need two students (not Grecia, not Louise, not Katya) → again only Hakeem and Joe available
- Fri: 1st = Grecia, 2nd = Katya → done

So Monday, Wednesday, Thursday need to be filled by Hakeem and Joe only.

But each of Hakeem and Joe must work **exactly two shifts**.

Let’s count available shifts for them:

- Monday: 1 shift
- Wednesday: 1 shift
- Thursday: 2 shifts

Total = 4 shifts → perfect for two students × 2 shifts.

Now, constraint: Hakeem and Joe must work **on the same day at least once**.

So among Mon, Wed, Thu, they must share at least one day.

Possible.

Now, check if any of the answer choices are **forced** in this case.

Answer choices:

(A) Grecia does not work on Tuesday → In this case, Grecia works Wed/Fri → so **true** in this case.

(B) Hakeem does not work on Wednesday → Not necessarily; could work Wed.

(C) Joe does not work on Tuesday → True, since Tuesday is full (Katya/Louise). So Joe doesn’t work Tuesday.

(D) Joe does not work on Thursday → Not necessarily; could work Thu.

(E) Louise does not work on Tuesday → **False** in this case; she **does** work Tuesday.

So in this case, (E) is false, (A) and (C) are true.

But we need what **must be true** in **all** valid schedules.

So we need to test other Louise placements to see if (A) or (C) always hold.

---

### Case 2: Louise works Tue (2nd) and Wed (2nd)

Then Louise is on Tue and Wed.

Grecia cannot be on Tue or Wed.

Grecia must pick two nonconsecutive days from {Mon, Thu, Fri}

Possible nonconsecutive pairs:

- Mon & Thu → OK (not adjacent)
- Mon & Fri → OK
- Thu & Fri → **consecutive** → not allowed

So Grecia can be on (Mon, Thu) or (Mon, Fri)

Now, Katya is on Tue and Fri.

On Tuesday: Louise is 2nd → Katya must be 1st → OK

On Friday: Katya is either 1st or 2nd.

Now consider Grecia options.

#### Subcase 2a: Grecia on Mon and Thu (both 1st)

Then:

- Mon: 1st = Grecia → 2nd = ?
- Tue: 1st = Katya, 2nd = Louise
- Wed: 1st = ?, 2nd = Louise
- Thu: 1st = Grecia → 2nd = ?
- Fri: Katya = ? shift

Now, who’s available for remaining shifts?

Used so far:

- Grecia: Mon, Thu
- Louise: Tue, Wed
- Katya: Tue, Fri

Remaining students: Hakeem, Joe

Remaining shifts:

- Mon: 2nd
- Wed: 1st
- Thu: 2nd
- Fri: 1st or 2nd (whichever Katya doesn’t take)

Total shifts left: 4 → again Hakeem and Joe must fill them.

Now, can we assign so that Hakeem and Joe share a day?

Possible shared days: Mon (only 2nd open), Wed (only 1st open), Thu (only 2nd open), Fri (1 shift open)

They can share a day only if both shifts of a day are assigned to them — but each day only has one open shift in this setup.

Wait: On Friday, Katya takes one shift, so only one shift left → can't share Friday.

On Mon: only 2nd open → only one of them can work.

Same for Wed (only 1st open), Thu (only 2nd open).

So **no day has two open shifts** for Hakeem and Joe to share.

Thus, **they cannot work on the same day** → violates constraint #4.

Therefore, **Subcase 2a is invalid**.

#### Subcase 2b: Grecia on Mon and Fri (both 1st)

Then:

- Mon: 1st = Grecia
- Fri: 1st = Grecia

Katya is on Tue and Fri → on Fri, Grecia is 1st, so Katya must be 2nd.

Tue: Louise is 2nd → Katya must be 1st.

So Katya: Tue (1st), Fri (2nd) → OK

Louise: Tue (2nd), Wed (2nd)

Grecia: Mon (1st), Fri (1st)

Now used shifts:

- Mon: 1st = Grecia → 2nd = ?
- Tue: 1st = Katya, 2nd = Louise
- Wed: 2nd = Louise → 1st = ?
- Thu: both shifts open
- Fri: 1st = Grecia, 2nd = Katya

Remaining shifts: Mon (2nd), Wed (1st), Thu (1st), Thu (2nd) → 4 shifts

Again, only Hakeem and Joe available.

Now, can they share a day?

- Mon: only 2nd open → only one can work
- Wed: only 1st open → only one
- Thu: both shifts open → **both can work Thu**

So they can share Thursday → satisfies constraint #4.

So this subcase is **valid**.

Now check answer choices in this valid schedule:

- (A) Grecia does not work on Tuesday → Grecia works Mon/Fri → **true**
- (C) Joe does not work on Tuesday → Tuesday is Katya/Louise → **true**
- (E) Louise does not work on Tuesday → **false** (she does)

So again, (A) and (C) hold.

Now check if (C) could ever be false.

Is there any valid schedule where **Joe works on Tuesday**?

Tuesday has two shifts: first and second.

We know **Katya works on Tuesday** (constraint). So Katya takes one shift.

Louise may or may not work Tuesday.

But if Louise **does not** work Tuesday, then second shift is open.

Could Joe take that?

But wait: if Louise does **not** work Tuesday, then her two consecutive second-shift days must be elsewhere.

Let’s test a case where Louise **does not** work Tuesday.

That would be Louise on Wed-Thu or Thu-Fri.

Let’s try **Louise on Thu-Fri** (Case 4). We’ll come back to whether Joe can work Tuesday.

But first, continue with current case analysis.

---

### Case 3: Louise works Wed (2nd) and Thu (2nd)

Then Louise is on Wed, Thu.

Grecia cannot be on Wed or Thu.

Grecia must pick two nonconsecutive days from {Mon, Tue, Fri}

Possible pairs:

- Mon & Tue → consecutive → not allowed
- Mon & Fri → OK
- Tue & Fri → OK

So Grecia can be (Mon, Fri) or (Tue, Fri)

Now, Katya is on Tue and Fri.

Consider each.

#### Subcase 3a: Grecia on Mon and Fri

Then:

- Mon: 1st = Grecia
- Fri: 1st = Grecia

Katya on Tue and Fri → on Fri, Grecia is 1st, so Katya must be 2nd.

On Tue: Katya can be 1st or 2nd.

Louise: Wed (2nd), Thu (2nd)

Now used shifts:

- Mon: 1st = Grecia → 2nd = ?
- Tue: Katya = ? shift
- Wed: 2nd = Louise → 1st = ?
- Thu: 2nd = Louise → 1st = ?
- Fri: 1st = Grecia, 2nd = Katya

Remaining shifts:

- Mon: 2nd
- Tue: 1st or 2nd (whichever Katya doesn’t take)
- Wed: 1st
- Thu: 1st

Total = 4 shifts → Hakeem and Joe

Now, can they share a day?

Each of these days has only **one** open shift:

- Mon: 2nd
- Tue: one shift
- Wed: 1st
- Thu: 1st

So **no day has two open shifts** → Hakeem and Joe cannot share a day → **invalid**

#### Subcase 3b: Grecia on Tue and Fri

Then Grecia works first shift on Tue and Fri.

But Katya also works on Tue and Fri.

So on Tuesday: Grecia = 1st, so Katya must be 2nd.

On Friday: Grecia = 1st, so Katya = 2nd.

So Katya: Tue (2nd), Fri (2nd)

Louise: Wed (2nd), Thu (2nd)

Now used shifts:

- Tue: 1st = Grecia, 2nd = Katya
- Fri: 1st = Grecia, 2nd = Katya
- Wed: 2nd = Louise → 1st = ?
- Thu: 2nd = Louise → 1st = ?
- Mon: both shifts open

Remaining shifts: Mon (2 shifts), Wed (1st), Thu (1st) → total 4 shifts

Again, only Hakeem and Joe.

Now, can they share a day?

- Mon: both shifts open → they can share Monday → OK

So this is **valid**.

Now check answer choices:

- Grecia works Tue and Fri → so (A) “Grecia does not work on Tuesday” is **false** in this case!

So (A) is **not always true**.

Now check (C): Joe does not work on Tuesday.

In this schedule, Tuesday shifts are:

- 1st = Grecia
- 2nd = Katya

So Joe **cannot** work Tuesday → (C) is **true** here.

So (A) is **not must-be-true**, but (C) still holds.

Now check if (C) can ever be false.

Is there any valid schedule where **Joe works on Tuesday**?

That would require Joe to take one of Tuesday’s shifts.

But Tuesday must have Katya (constraint). So only one other shift available.

So Joe could take the other shift **if** Louise is not working Tuesday.

So let's try to construct a valid schedule where **Louise does not work Tuesday**, and Joe takes the other shift.

That would be Louise on **Wed-Thu** or **Thu-Fri**.

We just did Wed-Thu → in that case, Tuesday had Grecia and Katya (in subcase 3b), so no room for Joe.

But what if Grecia is **not** on Tuesday?

In Case 3 (Louise = Wed-Thu), Grecia could be on Mon & Fri (subcase 3a), but that was invalid due to Hakeem/Joe not sharing a day.

But maybe another Louise placement.

### Case 4: Louise works Thu (2nd) and Fri (2nd)

Then Louise is on Thu, Fri.

Grecia cannot be on Thu or Fri.

Grecia must pick two nonconsecutive days from {Mon, Tue, Wed}

Possible pairs:

- Mon & Wed → OK (nonconsecutive)
- Mon & Tue → consecutive → not allowed
- Tue & Wed → consecutive → not allowed

So only possibility: **Mon and Wed**

So Grecia = Mon (1st), Wed (1st)

Katya = Tue, Fri

Now, on Friday: Louise is 2nd, so Katya must be 1st (since only one per shift)

On Tuesday: Katya can be 1st or 2nd.

Now used shifts:

- Mon: 1st = Grecia → 2nd = ?
- Tue: Katya = ? shift
- Wed: 1st = Grecia → 2nd = ?
- Thu: 2nd = Louise → 1st = ?
- Fri: 1st = Katya, 2nd = Louise

Remaining shifts:

- Mon: 2nd
- Tue: 1 shift (whichever Katya doesn’t take)
- Wed: 2nd
- Thu: 1st

Total = 4 shifts → Hakeem and Joe

Now, can they share a day?

Each day has only one open shift:

- Mon: 2nd
- Tue: one shift
- Wed: 2nd
- Thu: 1st

No day has two open shifts → **cannot share a day** → **invalid**

So Louise on Thu-Fri leads to **no valid schedule**.

Thus, **only valid Louise placements are**:

- Mon-Tue
- Tue-Wed (with Grecia on Mon & Fri)
- Wed-Thu (with Grecia on Tue & Fri)

We’ve seen:

- In Mon-Tue: Grecia on Wed/Fri → not on Tue
- In Tue-Wed: Grecia on Mon/Fri → not on Tue
- In Wed-Thu: Grecia on Tue/Fri → **on Tue**

So only in the Wed-Thu case does Grecia work Tuesday.

But is that case **fully valid**? Let's double-check all constraints.

In Wed-Thu case (Louise = Wed/Thu, Grecia = Tue/Fri):

- Grecia: Tue (1st), Fri (1st)
- Louise: Wed (2nd), Thu (2nd)
- Katya: Tue (2nd), Fri (2nd)
- Hakeem/Joe: Mon (both shifts), Wed (1st), Thu (1st)

Wait, hold on: On Tuesday, Grecia is 1st, Katya is 2nd → OK

On Friday, Grecia 1st, Katya 2nd → OK

On Wednesday: Louise 2nd, so 1st must be Hakeem or Joe

On Thursday: Louise 2nd, so 1st must be Hakeem or Joe

On Monday: both shifts open → assign to Hakeem and Joe

Now count shifts for Hakeem and Joe:

- Monday: 2 shifts → assign one to each → each has 1 shift
- Wednesday: 1st → assign to, say, Hakeem → Hakeem now has 2 shifts
- Thursday: 1st → assign to Joe → Joe now has 2 shifts

Now, do Hakeem and Joe share a day? Yes: **Monday** (both work Monday) → OK

All constraints satisfied.

So this is a **valid schedule** where **Grecia works Tuesday**.

Therefore, (A) “Grecia does not work on Tuesday” is **not always true**.

Now, what about (C): “Joe does not work on Tuesday”

In this valid schedule, Tuesday shifts are taken by Grecia and Katya → Joe does **not** work Tuesday.

Is there **any** valid schedule where Joe **does** work Tuesday?

To have Joe work Tuesday, he must take one of the two shifts.

But Tuesday must include Katya.

So Joe would take the other shift.

That means **Louise cannot be on Tuesday** (since Louise only does second shift, and if she’s on Tuesday, she takes second shift; then Katya must be first; then no room for Joe).

So for Joe to work Tuesday, **Louise must not be on Tuesday**, and **Grecia must not be on Tuesday** (since Grecia only does first shift; if Grecia is on Tuesday, she takes first shift; then Katya must be second; again no room for Joe).

So for Joe to work Tuesday, **both Grecia and Louise must be off Tuesday**, and Katya takes one shift, Joe the other.

Is that possible?

Let’s try to construct such a schedule.

We need:

- Louise not on Tuesday → her consecutive second-shift days must be Mon-Tue (no, includes Tue), Tue-Wed (includes Tue), so only possibilities **excluding Tuesday** are Wed-Thu or Thu-Fri.

But we saw Thu-Fri leads to invalid (Hakeem/Joe can't share day).

Wed-Thu: we just did that, and in that case, Grecia was on Tue (to make schedule valid). But maybe there's another way?

In Wed-Thu case, Grecia must pick two nonconsecutive days from {Mon, Tue, Fri}.

We tried Mon & Fri → invalid (Hakeem/Joe can't share)

We tried Tue & Fri → valid

Any other? No.

So in Wed-Thu case, **Grecia must be on Tuesday** to make schedule valid.

Thus, if Louise is on Wed-Thu, Grecia must be on Tue → Joe can't work Tue.

What if Louise is on Mon-Tue? Then Louise is on Tue → Joe can't work Tue.

Louise on Tue-Wed → Louise on Tue → Joe can't work Tue.

Louise on Thu-Fri → we saw it's invalid.

So **in all valid schedules, Tuesday is occupied by Katya and either Louise or Grecia**.

Thus, **Joe never works on Tuesday**.

Therefore, (C) **must be true**.

Now check other options:

(B) Hakeem does not work on Wednesday.

In the Wed-Thu Louise case, Hakeem could work Wednesday (1st shift). So (B) not necessarily true.

(D) Joe does not work on Thursday.

In Mon-Tue Louise case, Thursday shifts are filled by Hakeem and Joe → Joe could work Thursday. So (D) not necessarily true.

(E) Louise does not work on Tuesday.

In Mon-Tue and Tue-Wed cases, Louise **does** work Tuesday → so (E) is false in those valid schedules.

Thus, the only statement that **must be true** is:

**(C) Joe does not work at the gallery on Tuesday.**

---

### Final Answer:

{"answer": "C"}

### TOKEN USAGE

  Input tokens:  332
  Output tokens: 5,407
  Total tokens:  5,739

COMPLETE

## System 1 Final Answer

```json
We are given a logic puzzle with 5 students (Grecia, Hakeem, Joe, Katya, Louise) and 5 days (Monday–Friday). Each day has two shifts: first and second. Each student works exactly **two shifts total**, and **no student works both shifts on the same day**.

Additional constraints:

1. **Louise works the second shift on two consecutive days.**
2. **Grecia works the first shift on two nonconsecutive days.**
3. **Katya works on Tuesday and Friday.**
4. **Hakeem and Joe work on the same day at least once.**
5. **Grecia and Louise never work on the same day.**

We are to determine which of the answer choices **must be true**.

---

### Step 1: Understand the structure

- 5 days × 2 shifts = 10 total shifts.
- 5 students × 2 shifts each = 10 shifts → all shifts are filled.
- Each day has exactly 2 different students (since no one works both shifts on a day).
- So each day is assigned to **two distinct students**, one for first shift, one for second.

We can think of each day as a pair: (First, Second)

We’ll denote the schedule as:

- Monday: (F1, S1)
- Tuesday: (F2, S2)
- Wednesday: (F3, S3)
- Thursday: (F4, S4)
- Friday: (F5, S5)

Each student appears in exactly two of these 10 positions (as either F or S), never twice in the same day.

---

### Step 2: Apply Katya’s constraint

> Katya works on Tuesday and Friday.

So Katya appears **once on Tuesday** (either first or second shift), and **once on Friday** (either first or second shift). That accounts for her two shifts.

So Katya is **not available** on Monday, Wednesday, or Thursday.

---

### Step 3: Apply Louise’s constraint

> Louise works the second shift on two **consecutive** days.

So Louise is in the **second shift** on two days that are consecutive, e.g., Mon-Tue, Tue-Wed, Wed-Thu, or Thu-Fri.

She has exactly two shifts total, so **both of her shifts are second shifts**, on consecutive days.

So Louise appears **only** on two consecutive days, both in the second shift.

Thus, Louise is **not available** on the other three days.

Also, since she only works second shift, she never works first shift.

---

### Step 4: Apply Grecia’s constraint

> Grecia works the first shift on two **nonconsecutive** days.

So Grecia’s two shifts are both **first shifts**, on nonconsecutive days.

So Grecia appears on two days (not adjacent), both in first shift.

She is not available on the other three days.

Also, Grecia and Louise **never work on the same day**.

Since Louise works on two consecutive days (second shift), Grecia **cannot** be scheduled on either of those days.

So Grecia’s two days must be among the **other three days**, and must be nonconsecutive.

But there are only 5 days total. Louise occupies 2 consecutive days. So only 3 days remain for Grecia.

From those 3 days, Grecia must pick **two nonconsecutive** days.

Let’s consider possible placements for Louise.

---

### Step 5: Consider possible placements for Louise

Louise works second shift on two consecutive days. Possible pairs:

- Mon-Tue
- Tue-Wed
- Wed-Thu
- Thu-Fri

We’ll analyze each possibility and see what constraints it imposes.

But first, recall that **Katya works on Tuesday and Friday**.

So Tuesday and Friday are **occupied by Katya** (one shift each). That means **Louise cannot work on Tuesday or Friday**, **if** that would conflict with Katya? Wait — actually, **multiple students can work on the same day**, just not the same shift. Since each day has two shifts, and Katya takes one of them (either first or second), the other shift can be someone else.

So **Louise can work on Tuesday or Friday**, as long as she takes the other shift from Katya.

But remember: **Louise only works second shift**.

So if Louise works on Tuesday, she must be **second shift**, and Katya must be **first shift** on Tuesday.

Similarly, if Louise works on Friday, she must be **second shift**, and Katya must be **first shift** on Friday.

Alternatively, if Katya is second shift on Tuesday, then Louise **cannot** work Tuesday (since Louise only does second shift, and only one person per shift).

So **Louise and Katya can share a day only if Katya is first shift and Louise is second shift**.

Same for Friday.

Now, Grecia and Louise **never share a day**, so Grecia cannot be on any day Louise works.

So Grecia’s two days must be among the days **Louise does not work**.

Also, Grecia works **first shift** on her two days.

Now, let’s consider each possible Louise pair and see what’s possible.

---

### Case 1: Louise works Mon (2nd) and Tue (2nd)

Then Louise is on Mon and Tue.

So Grecia cannot be on Mon or Tue.

Grecia must work two **nonconsecutive** days among Wed, Thu, Fri.

Possible nonconsecutive pairs from {Wed, Thu, Fri}:

- Wed and Fri → OK (nonconsecutive)
- Wed and Thu → consecutive → not allowed
- Thu and Fri → consecutive → not allowed

So only possible: **Wed and Fri**

So Grecia works first shift on Wed and Fri.

Now, Katya works on Tue and Fri.

On Friday: Grecia is first shift, Katya must be second shift (since only one per shift). OK.

On Tuesday: Louise is second shift, so Katya must be first shift on Tuesday. OK.

Now check total shifts per student:

- Louise: Mon (2nd), Tue (2nd) → done
- Grecia: Wed (1st), Fri (1st) → done
- Katya: Tue (1st), Fri (2nd) → done

Now we have used:

- Mon: 2nd = Louise → need 1st = someone (not Grecia, not Louise, not Katya) → must be Hakeem or Joe
- Tue: 1st = Katya, 2nd = Louise → done
- Wed: 1st = Grecia → need 2nd = someone (not Grecia, not Louise, not Katya) → Hakeem or Joe
- Thu: both shifts unassigned → need two students (not Grecia, not Louise, not Katya) → again only Hakeem and Joe available
- Fri: 1st = Grecia, 2nd = Katya → done

So Monday, Wednesday, Thursday need to be filled by Hakeem and Joe only.

But each of Hakeem and Joe must work **exactly two shifts**.

Let’s count available shifts for them:

- Monday: 1 shift
- Wednesday: 1 shift
- Thursday: 2 shifts

Total = 4 shifts → perfect for two students × 2 shifts.

Now, constraint: Hakeem and Joe must work **on the same day at least once**.

So among Mon, Wed, Thu, they must share at least one day.

Possible.

Now, check if any of the answer choices are **forced** in this case.

Answer choices:

(A) Grecia does not work on Tuesday → In this case, Grecia works Wed/Fri → so **true** in this case.

(B) Hakeem does not work on Wednesday → Not necessarily; could work Wed.

(C) Joe does not work on Tuesday → True, since Tuesday is full (Katya/Louise). So Joe doesn’t work Tuesday.

(D) Joe does not work on Thursday → Not necessarily; could work Thu.

(E) Louise does not work on Tuesday → **False** in this case; she **does** work Tuesday.

So in this case, (E) is false, (A) and (C) are true.

But we need what **must be true** in **all** valid schedules.

So we need to test other Louise placements to see if (A) or (C) always hold.

---

### Case 2: Louise works Tue (2nd) and Wed (2nd)

Then Louise is on Tue and Wed.

Grecia cannot be on Tue or Wed.

Grecia must pick two nonconsecutive days from {Mon, Thu, Fri}

Possible nonconsecutive pairs:

- Mon & Thu → OK (not adjacent)
- Mon & Fri → OK
- Thu & Fri → **consecutive** → not allowed

So Grecia can be on (Mon, Thu) or (Mon, Fri)

Now, Katya is on Tue and Fri.

On Tuesday: Louise is 2nd → Katya must be 1st → OK

On Friday: Katya is either 1st or 2nd.

Now consider Grecia options.

#### Subcase 2a: Grecia on Mon and Thu (both 1st)

Then:

- Mon: 1st = Grecia → 2nd = ?
- Tue: 1st = Katya, 2nd = Louise
- Wed: 1st = ?, 2nd = Louise
- Thu: 1st = Grecia → 2nd = ?
- Fri: Katya = ? shift

Now, who’s available for remaining shifts?

Used so far:

- Grecia: Mon, Thu
- Louise: Tue, Wed
- Katya: Tue, Fri

Remaining students: Hakeem, Joe

Remaining shifts:

- Mon: 2nd
- Wed: 1st
- Thu: 2nd
- Fri: 1st or 2nd (whichever Katya doesn’t take)

Total shifts left: 4 → again Hakeem and Joe must fill them.

Now, can we assign so that Hakeem and Joe share a day?

Possible shared days: Mon (only 2nd open), Wed (only 1st open), Thu (only 2nd open), Fri (1 shift open)

They can share a day only if both shifts of a day are assigned to them — but each day only has one open shift in this setup.

Wait: On Friday, Katya takes one shift, so only one shift left → can't share Friday.

On Mon: only 2nd open → only one of them can work.

Same for Wed (only 1st open), Thu (only 2nd open).

So **no day has two open shifts** for Hakeem and Joe to share.

Thus, **they cannot work on the same day** → violates constraint #4.

Therefore, **Subcase 2a is invalid**.

#### Subcase 2b: Grecia on Mon and Fri (both 1st)

Then:

- Mon: 1st = Grecia
- Fri: 1st = Grecia

Katya is on Tue and Fri → on Fri, Grecia is 1st, so Katya must be 2nd.

Tue: Louise is 2nd → Katya must be 1st.

So Katya: Tue (1st), Fri (2nd) → OK

Louise: Tue (2nd), Wed (2nd)

Grecia: Mon (1st), Fri (1st)

Now used shifts:

- Mon: 1st = Grecia → 2nd = ?
- Tue: 1st = Katya, 2nd = Louise
- Wed: 2nd = Louise → 1st = ?
- Thu: both shifts open
- Fri: 1st = Grecia, 2nd = Katya

Remaining shifts: Mon (2nd), Wed (1st), Thu (1st), Thu (2nd) → 4 shifts

Again, only Hakeem and Joe available.

Now, can they share a day?

- Mon: only 2nd open → only one can work
- Wed: only 1st open → only one
- Thu: both shifts open → **both can work Thu**

So they can share Thursday → satisfies constraint #4.

So this subcase is **valid**.

Now check answer choices in this valid schedule:

- (A) Grecia does not work on Tuesday → Grecia works Mon/Fri → **true**
- (C) Joe does not work on Tuesday → Tuesday is Katya/Louise → **true**
- (E) Louise does not work on Tuesday → **false** (she does)

So again, (A) and (C) hold.

Now check if (C) could ever be false.

Is there any valid schedule where **Joe works on Tuesday**?

Tuesday has two shifts: first and second.

We know **Katya works on Tuesday** (constraint). So Katya takes one shift.

Louise may or may not work Tuesday.

But if Louise **does not** work Tuesday, then second shift is open.

Could Joe take that?

But wait: if Louise does **not** work Tuesday, then her two consecutive second-shift days must be elsewhere.

Let’s test a case where Louise **does not** work Tuesday.

That would be Louise on Wed-Thu or Thu-Fri.

Let’s try **Louise on Thu-Fri** (Case 4). We’ll come back to whether Joe can work Tuesday.

But first, continue with current case analysis.

---

### Case 3: Louise works Wed (2nd) and Thu (2nd)

Then Louise is on Wed, Thu.

Grecia cannot be on Wed or Thu.

Grecia must pick two nonconsecutive days from {Mon, Tue, Fri}

Possible pairs:

- Mon & Tue → consecutive → not allowed
- Mon & Fri → OK
- Tue & Fri → OK

So Grecia can be (Mon, Fri) or (Tue, Fri)

Now, Katya is on Tue and Fri.

Consider each.

#### Subcase 3a: Grecia on Mon and Fri

Then:

- Mon: 1st = Grecia
- Fri: 1st = Grecia

Katya on Tue and Fri → on Fri, Grecia is 1st, so Katya must be 2nd.

On Tue: Katya can be 1st or 2nd.

Louise: Wed (2nd), Thu (2nd)

Now used shifts:

- Mon: 1st = Grecia → 2nd = ?
- Tue: Katya = ? shift
- Wed: 2nd = Louise → 1st = ?
- Thu: 2nd = Louise → 1st = ?
- Fri: 1st = Grecia, 2nd = Katya

Remaining shifts:

- Mon: 2nd
- Tue: 1st or 2nd (whichever Katya doesn’t take)
- Wed: 1st
- Thu: 1st

Total = 4 shifts → Hakeem and Joe

Now, can they share a day?

Each of these days has only **one** open shift:

- Mon: 2nd
- Tue: one shift
- Wed: 1st
- Thu: 1st

So **no day has two open shifts** → Hakeem and Joe cannot share a day → **invalid**

#### Subcase 3b: Grecia on Tue and Fri

Then Grecia works first shift on Tue and Fri.

But Katya also works on Tue and Fri.

So on Tuesday: Grecia = 1st, so Katya must be 2nd.

On Friday: Grecia = 1st, so Katya = 2nd.

So Katya: Tue (2nd), Fri (2nd)

Louise: Wed (2nd), Thu (2nd)

Now used shifts:

- Tue: 1st = Grecia, 2nd = Katya
- Fri: 1st = Grecia, 2nd = Katya
- Wed: 2nd = Louise → 1st = ?
- Thu: 2nd = Louise → 1st = ?
- Mon: both shifts open

Remaining shifts: Mon (2 shifts), Wed (1st), Thu (1st) → total 4 shifts

Again, only Hakeem and Joe.

Now, can they share a day?

- Mon: both shifts open → they can share Monday → OK

So this is **valid**.

Now check answer choices:

- Grecia works Tue and Fri → so (A) “Grecia does not work on Tuesday” is **false** in this case!

So (A) is **not always true**.

Now check (C): Joe does not work on Tuesday.

In this schedule, Tuesday shifts are:

- 1st = Grecia
- 2nd = Katya

So Joe **cannot** work Tuesday → (C) is **true** here.

So (A) is **not must-be-true**, but (C) still holds.

Now check if (C) can ever be false.

Is there any valid schedule where **Joe works on Tuesday**?

That would require Joe to take one of Tuesday’s shifts.

But Tuesday must have Katya (constraint). So only one other shift available.

So Joe could take the other shift **if** Louise is not working Tuesday.

So let's try to construct a valid schedule where **Louise does not work Tuesday**, and Joe takes the other shift.

That would be Louise on **Wed-Thu** or **Thu-Fri**.

We just did Wed-Thu → in that case, Tuesday had Grecia and Katya (in subcase 3b), so no room for Joe.

But what if Grecia is **not** on Tuesday?

In Case 3 (Louise = Wed-Thu), Grecia could be on Mon & Fri (subcase 3a), but that was invalid due to Hakeem/Joe not sharing a day.

But maybe another Louise placement.

### Case 4: Louise works Thu (2nd) and Fri (2nd)

Then Louise is on Thu, Fri.

Grecia cannot be on Thu or Fri.

Grecia must pick two nonconsecutive days from {Mon, Tue, Wed}

Possible pairs:

- Mon & Wed → OK (nonconsecutive)
- Mon & Tue → consecutive → not allowed
- Tue & Wed → consecutive → not allowed

So only possibility: **Mon and Wed**

So Grecia = Mon (1st), Wed (1st)

Katya = Tue, Fri

Now, on Friday: Louise is 2nd, so Katya must be 1st (since only one per shift)

On Tuesday: Katya can be 1st or 2nd.

Now used shifts:

- Mon: 1st = Grecia → 2nd = ?
- Tue: Katya = ? shift
- Wed: 1st = Grecia → 2nd = ?
- Thu: 2nd = Louise → 1st = ?
- Fri: 1st = Katya, 2nd = Louise

Remaining shifts:

- Mon: 2nd
- Tue: 1 shift (whichever Katya doesn’t take)
- Wed: 2nd
- Thu: 1st

Total = 4 shifts → Hakeem and Joe

Now, can they share a day?

Each day has only one open shift:

- Mon: 2nd
- Tue: one shift
- Wed: 2nd
- Thu: 1st

No day has two open shifts → **cannot share a day** → **invalid**

So Louise on Thu-Fri leads to **no valid schedule**.

Thus, **only valid Louise placements are**:

- Mon-Tue
- Tue-Wed (with Grecia on Mon & Fri)
- Wed-Thu (with Grecia on Tue & Fri)

We’ve seen:

- In Mon-Tue: Grecia on Wed/Fri → not on Tue
- In Tue-Wed: Grecia on Mon/Fri → not on Tue
- In Wed-Thu: Grecia on Tue/Fri → **on Tue**

So only in the Wed-Thu case does Grecia work Tuesday.

But is that case **fully valid**? Let's double-check all constraints.

In Wed-Thu case (Louise = Wed/Thu, Grecia = Tue/Fri):

- Grecia: Tue (1st), Fri (1st)
- Louise: Wed (2nd), Thu (2nd)
- Katya: Tue (2nd), Fri (2nd)
- Hakeem/Joe: Mon (both shifts), Wed (1st), Thu (1st)

Wait, hold on: On Tuesday, Grecia is 1st, Katya is 2nd → OK

On Friday, Grecia 1st, Katya 2nd → OK

On Wednesday: Louise 2nd, so 1st must be Hakeem or Joe

On Thursday: Louise 2nd, so 1st must be Hakeem or Joe

On Monday: both shifts open → assign to Hakeem and Joe

Now count shifts for Hakeem and Joe:

- Monday: 2 shifts → assign one to each → each has 1 shift
- Wednesday: 1st → assign to, say, Hakeem → Hakeem now has 2 shifts
- Thursday: 1st → assign to Joe → Joe now has 2 shifts

Now, do Hakeem and Joe share a day? Yes: **Monday** (both work Monday) → OK

All constraints satisfied.

So this is a **valid schedule** where **Grecia works Tuesday**.

Therefore, (A) “Grecia does not work on Tuesday” is **not always true**.

Now, what about (C): “Joe does not work on Tuesday”

In this valid schedule, Tuesday shifts are taken by Grecia and Katya → Joe does **not** work Tuesday.

Is there **any** valid schedule where Joe **does** work Tuesday?

To have Joe work Tuesday, he must take one of the two shifts.

But Tuesday must include Katya.

So Joe would take the other shift.

That means **Louise cannot be on Tuesday** (since Louise only does second shift, and if she’s on Tuesday, she takes second shift; then Katya must be first; then no room for Joe).

So for Joe to work Tuesday, **Louise must not be on Tuesday**, and **Grecia must not be on Tuesday** (since Grecia only does first shift; if Grecia is on Tuesday, she takes first shift; then Katya must be second; again no room for Joe).

So for Joe to work Tuesday, **both Grecia and Louise must be off Tuesday**, and Katya takes one shift, Joe the other.

Is that possible?

Let’s try to construct such a schedule.

We need:

- Louise not on Tuesday → her consecutive second-shift days must be Mon-Tue (no, includes Tue), Tue-Wed (includes Tue), so only possibilities **excluding Tuesday** are Wed-Thu or Thu-Fri.

But we saw Thu-Fri leads to invalid (Hakeem/Joe can't share day).

Wed-Thu: we just did that, and in that case, Grecia was on Tue (to make schedule valid). But maybe there's another way?

In Wed-Thu case, Grecia must pick two nonconsecutive days from {Mon, Tue, Fri}.

We tried Mon & Fri → invalid (Hakeem/Joe can't share)

We tried Tue & Fri → valid

Any other? No.

So in Wed-Thu case, **Grecia must be on Tuesday** to make schedule valid.

Thus, if Louise is on Wed-Thu, Grecia must be on Tue → Joe can't work Tue.

What if Louise is on Mon-Tue? Then Louise is on Tue → Joe can't work Tue.

Louise on Tue-Wed → Louise on Tue → Joe can't work Tue.

Louise on Thu-Fri → we saw it's invalid.

So **in all valid schedules, Tuesday is occupied by Katya and either Louise or Grecia**.

Thus, **Joe never works on Tuesday**.

Therefore, (C) **must be true**.

Now check other options:

(B) Hakeem does not work on Wednesday.

In the Wed-Thu Louise case, Hakeem could work Wednesday (1st shift). So (B) not necessarily true.

(D) Joe does not work on Thursday.

In Mon-Tue Louise case, Thursday shifts are filled by Hakeem and Joe → Joe could work Thursday. So (D) not necessarily true.

(E) Louise does not work on Tuesday.

In Mon-Tue and Tue-Wed cases, Louise **does** work Tuesday → so (E) is false in those valid schedules.

Thus, the only statement that **must be true** is:

**(C) Joe does not work at the gallery on Tuesday.**

---

### Final Answer:

{"answer": "C"}
```
