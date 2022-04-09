/* Make the following predicates dynamic */
:- (dynamic[visited/2, wumpus/2, confundus/2, tingle/2, glitter/2, stench/2, safe/2, current/3, hasarrow/0]).
  
  /****** Initial current position and possession of the agent. Note that the agent position is 0,0 which is relative. 
  This may not be the actual position of the agent in the real wumpus world map as displayed by driver ******/
current(0, 0, rnorth).
  
  /* Arrow checker will return true all the way until shoot has been used then return false. Once shoot has been used retract all 'hasarrow' */
hasarrow.
  
  /****** Localisation and mapping ******/
  
  /*** Each of these rules should just return a true or false. Based on the input from the driver, the agent KB will update these as facts ***/
  /* Add the current position as being visited - visited(X,Y) */
add_visited :-
    current(X, Y, _),
    asserta(visited(X, Y)).
  
  /* Add the current position as having wumpus - wumpus(X,Y) */
add_wumpus :-
    current(X, Y, _),
    asserta(wumpus(X, Y)).
  
  /* Add the current position as having confundus portal - confundus(X,Y) */
add_confundus :-
    current(X, Y, _),
    asserta(confundus(X, Y)).
  
  /* Add the current position as having tingle - tingle(X,Y) */
add_tingle :-
    current(X, Y, _),
    asserta(tingle(X, Y)).
  
  /* Add the current position as having glitter - glitter(X,Y) */
add_glitter :-
    current(X, Y, _),
    asserta(glitter(X, Y)).
  
  /* Add the current position as having stench - stench(X,Y) */
add_stench :-
    current(X, Y, _),
    asserta(stench(X, Y)).
  
  /* Add the current position as a safe square - safe(X,Y) */
add_safe :-
    current(X, Y, _),
    asserta(safe(X, Y)).
  
  /****** Current position(axis value and direction) of agent - current(X,Y,D) ******/
  
  
  /****** Movement(action, sensory input) of agent - move(A,L) ******/
  /* A will be determined using logic, L is passed in from driver and taken from KB facts */
  /* This will change the hunter's current position - current(X,Y,D) if valid */
  /* L is a list in this order: Confounded, Stench, Tingle, Glitter, Bump, Scream. Each of this element will be either on/off */
  
  % move(A,[C,St,T,G,B,Sc]):- (
  %    
  % )
  
  /* arrow remover */
  
  /****** If step into wumpus, reborn:  ******/
  /*  1. Retract all facts
      2. Initialize new random player position and update current(X,Y,D) to origin north */
initialize_new_pos(X, Y, D) :-
    retractall(current(_, _, _)),
    asserta(current(X, Y, D)).
  reborn :-
    retractall(visited(X, Y)),
    retractall(wumpus(X, Y)),
    retractall(confundus(X, Y)),
    retractall(tingle(X, Y)),
    retractall(glitter(X, Y)),
    retractall(stench(X, Y)),
    retractall(safe(X, Y)),
    initialize_new_pos(0, 0, rnorth),
    asserta(hasarrow).
  
  /****** If step into confundus portal, reposition:  ******/
  /*  1. Retract all visited squares and sensory readings (tingle, stench, glitter)
      2. Relocate new random player position and update current(X,Y,D) to origin north */
reposition :-
    retractall(visited(X, Y)),
    retractall(wumpus(X, Y)),
    retractall(confundus(X, Y)),
    retractall(tingle(X, Y)),
    retractall(glitter(X, Y)),
    retractall(stench(X, Y)),
    retractall(safe(X, Y)),
    initialize_new_pos(0, 0, rnorth).