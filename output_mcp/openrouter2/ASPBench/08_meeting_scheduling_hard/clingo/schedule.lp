room(r1). room(r2). room(r3). room(r4).

has_equipment(r1, projector). has_equipment(r1, whiteboard). has_equipment(r1, video). has_equipment(r1, confcall).
has_equipment(r2, projector). has_equipment(r2, whiteboard). has_equipment(r2, confcall).
has_equipment(r3, whiteboard). has_equipment(r3, confcall).
has_equipment(r4, projector). has_equipment(r4, video).

meeting(m1). meeting(m2). meeting(m3). meeting(m4). meeting(m5). meeting(m6). meeting(m7). meeting(m8). meeting(m9). meeting(m10). meeting(m11). meeting(m12). meeting(m13). meeting(m14). meeting(m15). meeting(m16). meeting(m17). meeting(m18). meeting(m19). meeting(m20).

attendee(m1, p1). attendee(m1, p3). attendee(m1, p6). attendee(m1, p8).
attendee(m2, p2). attendee(m2, p4). attendee(m2, p7). attendee(m2, p9).
attendee(m3, p3). attendee(m3, p5). attendee(m3, p8). attendee(m3, p10).
attendee(m4, p4). attendee(m4, p6). attendee(m4, p9). attendee(m4, p11).
attendee(m5, p5). attendee(m5, p7). attendee(m5, p10). attendee(m5, p12).
attendee(m6, p6). attendee(m6, p8). attendee(m6, p11). attendee(m6, p13).
attendee(m7, p7). attendee(m7, p9). attendee(m7, p12). attendee(m7, p14).
attendee(m8, p8). attendee(m8, p10). attendee(m8, p13). attendee(m8, p15).
attendee(m9, p9). attendee(m9, p11). attendee(m9, p14). attendee(m9, p16).
attendee(m10, p10). attendee(m10, p12). attendee(m10, p15). attendee(m10, p17).
attendee(m11, p11). attendee(m11, p13). attendee(m11, p16). attendee(m11, p18).
attendee(m12, p12). attendee(m12, p14). attendee(m12, p17). attendee(m12, p19).
attendee(m13, p13). attendee(m13, p15). attendee(m13, p18). attendee(m13, p20).
attendee(m14, p14). attendee(m14, p16). attendee(m14, p19). attendee(m14, p1).
attendee(m15, p15). attendee(m15, p17). attendee(m15, p20). attendee(m15, p2).
attendee(m16, p16). attendee(m16, p18). attendee(m16, p1). attendee(m16, p3).
attendee(m17, p17). attendee(m17, p19). attendee(m17, p2). attendee(m17, p4).
attendee(m18, p18). attendee(m18, p20). attendee(m18, p3). attendee(m18, p5).
attendee(m19, p19). attendee(m19, p1). attendee(m19, p4). attendee(m19, p6).
attendee(m20, p20). attendee(m20, p2). attendee(m20, p5). attendee(m20, p7).

required(m1, projector). required(m2, whiteboard). required(m3, confcall). required(m4, video). required(m4, projector). required(m5, projector). required(m5, confcall). required(m6, whiteboard). required(m6, confcall). required(m7, projector). required(m7, whiteboard). required(m7, confcall). required(m8, video). required(m8, confcall). required(m9, projector). required(m9, video). required(m10, projector). required(m10, whiteboard). required(m11, projector). required(m12, whiteboard). required(m13, confcall). required(m14, video). required(m14, projector). required(m15, projector). required(m15, confcall). required(m16, whiteboard). required(m16, confcall). required(m17, projector). required(m17, whiteboard). required(m17, confcall). required(m18, video). required(m18, confcall). required(m19, projector). required(m19, video). required(m20, projector). required(m20, whiteboard).

person(p1). person(p2). person(p3). person(p4). person(p5). person(p6). person(p7). person(p8). person(p9). person(p10). person(p11). person(p12). person(p13). person(p14). person(p15). person(p16). person(p17). person(p18). person(p19). person(p20).

day(1). day(2). day(3). day(4). day(5).

slot(1). slot(2). slot(3). slot(4).

% Assignment: each meeting assigned to exactly one day, slot, room
1 { assign(M,D,S,R) : day(D), slot(S), room(R) } 1 :- meeting(M).

% Person availability: no person attends two meetings at same day and slot
:- person(P), meeting(M1), meeting(M2), attendee(M1,P), attendee(M2,P), M1 != M2, assign(M1,D,S,R1), assign(M2,D,S,R2).

% Room occupancy: each room hosts at most one meeting per day and slot
:- room(R), day(D), slot(S), assign(M1,D,S,R), assign(M2,D,S,R), M1 != M2.

% Equipment requirement: assigned room must have all required equipment
:- meeting(M), assign(M,D,S,R), required(M,E), not has_equipment(R,E).

% Visible atoms
schedule(M,D,S,R) :- assign(M,D,S,R).
feasible :- assign(M,D,S,R).

#show schedule/4.
#show feasible.