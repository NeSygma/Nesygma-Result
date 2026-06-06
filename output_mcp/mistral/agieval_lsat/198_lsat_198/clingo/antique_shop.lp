% Domain: Days and Antiques
 day(1..6).
 antique(harominca; lamp; mirror; sundial; table; vase).

% Assignment: Each antique is auctioned on exactly one day
 1 { assigned(A, D) : day(D) } 1 :- antique(A).

% Helper predicate: earlier(A, B) means antique A is auctioned before antique B
 earlier(A, B) :- assigned(A, DA), assigned(B, DB), DA < DB.

% Base constraints from the problem

% 1. The sundial is not auctioned on June 1st
 :- assigned(sundial, 1).

% 2. If the harmonica is auctioned on an earlier date than the lamp, then the mirror is also auctioned on an earlier date than the lamp
 % Rephrased: It cannot be the case that harmonica < lamp and mirror >= lamp
 :- assigned(harominca, DH), assigned(lamp, DL), assigned(mirror, DM),
    earlier(harominca, lamp), not earlier(mirror, lamp).

% 3. The sundial is auctioned on an earlier date than the mirror and also on an earlier date than the vase
 :- assigned(sundial, DS), assigned(mirror, DM), not earlier(sundial, mirror).
 :- assigned(sundial, DS), assigned(vase, DV), not earlier(sundial, vase).

% 4. The table is auctioned on an earlier date than the harmonica or on an earlier date than the vase, but not both
 % This means exactly one of (table < harmonica) or (table < vase) is true
 :- assigned(table, DT), assigned(harominca, DH), assigned(vase, DV),
    (earlier(table, harominca) + earlier(table, vase)) != 1.

% Additional constraint from the question:
% The table is auctioned on a date that is later than both the date on which the mirror is auctioned and the date on which the vase is auctioned
 :- assigned(table, DT), assigned(mirror, DM), not earlier(mirror, table).
 :- assigned(table, DT), assigned(vase, DV), not earlier(vase, table).

% Map the correct answer to option/1
% (A) The harmonica is auctioned on an earlier date than the table
 option(a) :- earlier(harominca, table).

% (B) The table is auctioned on an earlier date than the lamp
 option(b) :- earlier(table, lamp).

% (C) The table is auctioned on an earlier date than the sundial
 option(c) :- earlier(table, sundial).

% (D) The mirror is auctioned on an earlier date than the vase
 option(d) :- earlier(mirror, vase).

% (E) The sundial is auctioned on an earlier date than the lamp
 option(e) :- earlier(sundial, lamp).

#show option/1.