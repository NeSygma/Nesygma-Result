% Schedule 20 meetings across 4 rooms and 5 days

% Domain declarations
room(r1). room(r2). room(r3). room(r4).
meeting(m1). meeting(m2). meeting(m3). meeting(m4). meeting(m5).
meeting(m6). meeting(m7). meeting(m8). meeting(m9). meeting(m10).
meeting(m11). meeting(m12). meeting(m13). meeting(m14). meeting(m15).
meeting(m16). meeting(m17). meeting(m18). meeting(m19). meeting(m20).
person(p1). person(p2). person(p3). person(p4). person(p5).
person(p6). person(p7). person(p8). person(p9). person(p10).
person(p11). person(p12). person(p13). person(p14). person(p15).
person(p16). person(p17). person(p18). person(p19). person(p20).
day(1..5).
slot(1..4).

% Room equipment
room_equipment(r1, "projector"). room_equipment(r1, "whiteboard"). room_equipment(r1, "video"). room_equipment(r1, "confcall").
room_equipment(r2, "projector"). room_equipment(r2, "whiteboard"). room_equipment(r2, "confcall").
room_equipment(r3, "whiteboard"). room_equipment(r3, "confcall").
room_equipment(r4, "projector"). room_equipment(r4, "video").

% Meeting equipment requirements
meeting_requirement(m1, "projector"). meeting_requirement(m11, "projector").
meeting_requirement(m2, "whiteboard"). meeting_requirement(m12, "whiteboard").
meeting_requirement(m3, "confcall"). meeting_requirement(m13, "confcall").
meeting_requirement(m4, "video"). meeting_requirement(m4, "projector"). meeting_requirement(m14, "video"). meeting_requirement(m14, "projector").
meeting_requirement(m5, "projector"). meeting_requirement(m5, "confcall"). meeting_requirement(m15, "projector"). meeting_requirement(m15, "confcall").
meeting_requirement(m6, "whiteboard"). meeting_requirement(m6, "confcall"). meeting_requirement(m16, "whiteboard"). meeting_requirement(m16, "confcall").
meeting_requirement(m7, "projector"). meeting_requirement(m7, "whiteboard"). meeting_requirement(m7, "confcall"). meeting_requirement(m17, "projector"). meeting_requirement(m17, "whiteboard"). meeting_requirement(m17, "confcall").
meeting_requirement(m8, "video"). meeting_requirement(m8, "confcall"). meeting_requirement(m18, "video"). meeting_requirement(m18, "confcall").
meeting_requirement(m9, "projector"). meeting_requirement(m9, "video"). meeting_requirement(m19, "projector"). meeting_requirement(m19, "video").
meeting_requirement(m10, "projector"). meeting_requirement(m10, "whiteboard"). meeting_requirement(m20, "projector"). meeting_requirement(m20, "whiteboard").

% Meeting attendees
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

% Schedule assignment: each meeting assigned to exactly one (day, slot, room)
1 { schedule(M, D, S, R) : day(D), slot(S), room(R) } 1 :- meeting(M).

% Room occupancy: at most one meeting per (day, slot, room)
:- schedule(M1, D, S, R), schedule(M2, D, S, R), M1 != M2.

% Person availability: no person can attend two meetings at same (day, slot)
:- attendee(M1, P), attendee(M2, P), schedule(M1, D, S, _), schedule(M2, D, S, _), M1 != M2.

% Equipment requirements: room must have all required equipment for the meeting
has_equipment(R, E) :- room_equipment(R, E).
:- schedule(M, _, _, R), meeting_requirement(M, E), not has_equipment(R, E).

% Show the schedule
#show schedule/4.
#show feasible/0.
feasible :- schedule(_, _, _, _).