hasarrow :-
    nb_current(shoot, A),
    not(A="true").

reborn.

confounded(on) :-
    nb_setval(confounded, on).
confounded(off) :-
    nb_setval(confounded, off).

stench(on) :-
    nb_setval(stench, on).
stench(off) :-
    nb_setval(stench, off).

tingle(on) :-
    nb_setval(tingle, on).
tingle(off) :-
    nb_setval(tingle, off).

glitter(on) :-
    nb_setval(glitter, on).
glitter(off) :-
    nb_setval(glitter, off).

bump(on) :-
    nb_setval(bump, on).
bump(off) :-
    nb_setval(bump, off).

scream(on) :-
    nb_setval(scream, on).
scream(off) :-
    nb_setval(scream, off).

move(shoot) :-
    nb_setval(shoot, "true"),
    write("shoot").
move(moveforward).
move(turnleft).
move(turnright).
move(pickup).

move(A, [LA, LB, LC, LD, LE, LF]) :-
    move(A),
    confounded(LA),
    stench(LB),
    tingle(LC),
    glitter(LD),
    bump(LE),
    scream(LF).

reposition([LA, LB, LC, LD, LE, LF]) :-
    confounded(LA),
    stench(LB),
    tingle(LC),
    glitter(LD),
    bump(LE),
    scream(LF).

explore([]).