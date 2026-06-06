% Scheduling 20 meetings across 4 rooms and 5 days with 4 time slots per day

% Domains
room(r1; r2; r3; r4).
day(1..5).
slot(1..4).
meeting(m1..m20).
person(p1..p20).

% Equipment per room
equipment_room(r1, projector).
equipment_room(r1, whiteboard).
equipment_room(r1, video).
equipment_room(r1, confcall).

equipment_room(r2, projector).
equipment_room(r2, whiteboard).
equipment_room(r2, confcall).

equipment_room(r3, whiteboard).
equipment_room(r3, confcall).

equipment_room(r4, projector).
equipment_room(r4, video).

% Equipment required per meeting
equipment_required(m1, projector).
equipment_required(m11, projector).

equipment_required(m2, whiteboard).
equipment_required(m12, whiteboard).

equipment_required(m3, confcall).
equipment_required(m13, confcall).

equipment_required(m4, video).
equipment_required(m4, projector).
equipment_required(m14, video).
equipment_required(m14, projector).

equipment_required(m5, projector).
equipment_required(m5, confcall).
equipment_required(m15, projector).
equipment_required(m15, confcall).

equipment_required(m6, whiteboard).
equipment_required(m6, confcall).
equipment_required(m16, whiteboard).
equipment_required(m16, confcall).

equipment_required(m7, projector).
equipment_required(m7, whiteboard).
equipment_required(m7, confcall).
equipment_required(m17, projector).
equipment_required(m17, whiteboard).
equipment_required(m17, confcall).

equipment_required(m8, video).
equipment_required(m8, confcall).
equipment_required(m18, video).
equipment_required(m18, confcall).

equipment_required(m9, projector).
equipment_required(m9, video).
equipment_required(m19, projector).
equipment_required(m19, video).

equipment_required(m10, projector).
equipment_required(m10, whiteboard).
equipment_required(m20, projector).
equipment_required(m20, whiteboard).

% Attendees per meeting
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

% Attending relation (person attends meeting)
attending(P, M) :- attendee(M, P).

% Schedule assignment: each meeting assigned to exactly one (day, slot, room)
1 { schedule(M, D, S, R) : day(D), slot(S), room(R) } 1 :- meeting(M).

% Room occupancy: at most one meeting per (day, slot, room)
:- schedule(M1, D, S, R), schedule(M2, D, S, R), M1 != M2.

% Person availability: no person can attend two meetings at same (day, slot)
:- attending(P, M1), attending(P, M2), schedule(M1, D, S, _), schedule(M2, D, S, _), M1 != M2.

% Equipment requirement: each meeting must be in a room that has all required equipment
:- schedule(M, D, S, R), equipment_required(M, E), not equipment_room(R, E).

% Show schedule
#show schedule/4.