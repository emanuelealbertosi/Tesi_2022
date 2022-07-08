functionReqs(flogin,[docker],(512,1,500),[(userDB,13)]).
functionReqs(fcrop,[docker],(512,1,1200),[(ai,5)]).
functionReqs(fgeo,[docker],(256,2,400),[(maps,5)]).
functionReqs(fdcc,[docker],(128,2,500),[(checkGp,50)]).
functionReqs(fcheckdcc,[docker],(512,2,500),[(dccchk,50)]).
functionReqs(frules,[docker],(512,1,400),[(checkRules,20)]).
functionReqs(far,[],(512,2,1200),[(sendMail,5)]).
functionBehaviour(flogin,[U,Sc,G],[U],[U,Sc,G]):- maxType(U, Draw, ScAr).
functionBehaviour(fcrop,[_,Sc,G],[],[Sc,G]):- maxType(U, Draw, ScAr).
functionBehaviour(fgeo,[Sc,G],[G],[Sc]):- maxType(U, Draw, ScAr).
functionBehaviour(fdcc,[U,_,_],[],[low]):- maxType(U, Draw, ScAr).
functionBehaviour(fcheckdcc,[_],[_],[low]):- maxType(U, Draw, ScAr).
functionBehaviour(frules,[_],[_],[low]):- maxType(U, Draw, ScAr).
functionBehaviour(far,[U,Sc,G],[U],[U,Sc,G]):- maxType(U, Draw, ScAr).
%versione automatica
functionOrch(arOrch,(userDevice, [top,low,medium]),seq(fun(flogin,[myusers],25),seq(fun(far,[sendmail],12),par([seq(fun(fcrop,[mycrop],18),fun(fgeo,[],12)),if(fun(fdcc,[greenpassapi],15),fun(fcheckdcc,[dccchk],15),fun(frules,[],18))])))).
%versione automatica
g_lattice_higherThan(top,medium).
g_lattice_higherThan(medium,low).
latticeColor(top,green).
latticeColor(medium,orange).
latticeColor(low,red).
nodeLabel(NodeId,top)    :- node(NodeId,_,SecCaps,_,_),member(antiTamp,SecCaps),member(pubKeyE,SecCaps).
nodeLabel(NodeId,medium)    :- node(NodeId,_,SecCaps,_,_),member(pubKeyE,SecCaps),\+(member(antiTamp,SecCaps)).
nodeLabel(NodeId,low)    :- node(NodeId,_,SecCaps,_,_),\+(member(pubKeyE,SecCaps)).
serviceLabel(SId,_,top):- service(SId,appOp,_,_).
serviceLabel(SId,_,top):- service(SId,appOp,_,_).
serviceLabel(SId,_,top):- service(SId,appOp,_,_).
serviceLabel(SId,_,top):- service(SId,pa,_,_).
serviceLabel(SId,_,top):- service(SId,appOp,_,_).
serviceLabel(SId,_,top):- service(SId,appOp,_,_).
serviceLabel(SId,_,top):- service(SId,appOp,_,_).
serviceLabel(SId, Type,low):- service(SId, Provider, Type, _),\+(Provider==appOp),\+((Provider==cloudProvider, Type ==maps)),\+((Provider==cloudProvider, Type ==sendMail)).
