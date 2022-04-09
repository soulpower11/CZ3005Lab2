:- (dynamic[visited/2, wumpus/2, confundus/2, tingle/2, glitter/2, stench/2, safe/2, wall/2]).
:- (dynamic[confounded/0, stench/0, tingle/0, glitter/0, bump/0, scream/0]).
:- (dynamic[hasarrow/0]).
:- (dynamic[current/3]).
:- retractall(current(_, _, _)).
:- retractall(hasarrow).
:- asserta(current(0, 0, rnorth)).
:- asserta(hasarrow).

test :-
    current(X, Y, D),
    X1 is X+1,
    write(X1),
    write(Y),
    write(D).

move(A) :-
    (   A=shoot
    ->  retract(hasarrow),
        write(shoot)
    ;   A=moveforward
    ->  forward
    ;   A=turnleft
    ->  turnleft
    ;   A=turnright
    ->  turnright
    ).

forward :-
    current(X, Y, D),
    (   D=rnorth
    ->  Y1 is Y+1,
        retractall(current(_, _, _)),
        asserta(current(X, Y1, D))
    ;   D=rwest
    ->  X1 is X-1,
        retractall(current(_, _, _)),
        asserta(current(X1, Y, D))
    ;   D=reast
    ->  X1 is X+1,
        retractall(current(_, _, _)),
        asserta(current(X1, Y, D))
    ;   D=rsouth
    ->  Y1 is Y-1,
        retractall(current(_, _, _)),
        asserta(current(X, Y1, D))
    ).

turnleft :-
    current(X, Y, D),
    (   D=rnorth
    ->  asserta(current(X, Y, rwest))
    ;   D=rwest
    ->  asserta(current(X, Y, rsouth))
    ;   D=reast
    ->  asserta(current(X, Y, rnorth))
    ;   D=rsouth
    ->  asserta(current(X, Y, reast))
    ).

turnright :-
    current(X, Y, D),
    (   D=rnorth
    ->  asserta(current(X, Y, reast))
    ;   D=rwest
    ->  asserta(current(X, Y, rnorth))
    ;   D=reast
    ->  asserta(current(X, Y, rsouth))
    ;   D=rsouth
    ->  asserta(current(X, Y, rwest))
    ).

confounded(A) :-
    (   A=on
    ->  (   not(confounded)
        ->  asserta(confounded)
        ;    !
        )
    ;   A=off
    ->  (   confounded
        ->  retract(confounded)
        ;    !
        )
    ).

stench(A) :-
    (   A=on
    ->  (   not(stench)
        ->  asserta(stench)
        ;    !
        )
    ;   A=off
    ->  (   stench
        ->  retract(stench)
        ;    !
        )
    ).

tingle(A) :-
    (   A=on
    ->  (   not(tingle)
        ->  asserta(tingle)
        ;    !
        )
    ;   A=off
    ->  (   tingle
        ->  retract(tingle)
        ;    !
        )
    ).

glitter(A) :-
    (   A=on
    ->  (   not(glitter)
        ->  asserta(glitter)
        ;    !
        )
    ;   A=off
    ->  (   glitter
        ->  retract(glitter)
        ;    !
        )
    ).

bump(A) :-
    (   A=on
    ->  (   not(bump)
        ->  asserta(bump)
        ;    !
        )
    ;   A=off
    ->  (   bump
        ->  retract(bump)
        ;    !
        )
    ).

scream(A) :-
    (   A=on
    ->  (   not(scream)
        ->  asserta(scream)
        ;    !
        )
    ;   A=off
    ->  (   scream
        ->  retract(scream)
        ;    !
        )
    ).

reposition([LA, LB, LC, LD, LE, LF]) :-
    retractall(visited(_, _)),
    retractall(wumpus(_, _)),
    retractall(confundus(_, _)),
    retractall(tingle(_, _)),
    retractall(glitter(_, _)),
    retractall(stench(_, _)),
    retractall(safe(_, _)),
    retractall(wall(_, _)),
    confounded(LA),
    stench(LB),
    tingle(LC),
    glitter(LD),
    bump(LE),
    scream(LF).

move(A, [LA, LB, LC, LD, LE, LF]) :-
    move(A),
    confounded(LA),
    stench(LB),
    tingle(LC),
    glitter(LD),
    bump(LE),
    scream(LF).