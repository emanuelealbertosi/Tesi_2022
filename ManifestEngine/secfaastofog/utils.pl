%find highest type in a list
highestType([T], T).
highestType([T1,T2|Ts], MaxT) :-
	highestType([T2|Ts], MaxTofRest),
	maxType(T1, MaxTofRest, MaxT).

maxType(T1,T2,TMax):- once(innerMaxType(T1,T2,TMax)).
innerMaxType(X, X, X).
innerMaxType(X, Y, X) :- dif(X,Y), lattice_higherThan(X,Y).
innerMaxType(X, Y, Y) :- dif(X,Y), lattice_higherThan(Y,X).
innerMaxType(X, Y, Top) :-											%labels not reachable with path (on different branch) 
	dif(X,Y), \+ lattice_higherThan(X,Y), \+ lattice_higherThan(Y,X),
	lattice_higherThan(Top, X), lattice_higherThan(Top, Y),
	\+ (lattice_higherThan(Top, LowerTop), lattice_higherThan(LowerTop, X), lattice_higherThan(LowerTop, Y)).
lattice_higherThan(X, Y) :- g_lattice_higherThan(X,Y).
lattice_higherThan(X, Y) :- g_lattice_higherThan(X,W), lattice_higherThan(W,Y).

%highestListType(List1, List2, ListHigher) %given two lists pick the highest type in the same position
highestListType([],[],[]).
highestListType(L,[],L).
highestListType([],L,L).
highestListType(L,L,L).
highestListType([T1|L1],[T2|L2],[Tmax|LRes]):-
	maxType(T1,T2,Tmax),
	highestListType(L1,L2,LRes).

lowestType(LowestType):-
	g_lattice_higherThan(_,LowestType), \+ (g_lattice_higherThan(LowestType,_)).
%condTypes(Positions, TypeList, PosList) extract types of Position from TypeList  into PosList
condTypes([],_,[]).
condTypes([Pos|CondList],InTypes, [TypePos|CondTypes]):-
	nth0(Pos,InTypes,TypePos),
	condTypes(CondList, InTypes, CondTypes).

swReqsOK(SWReqs, SWCaps):- subset(SWReqs, SWCaps).
%hwReqsOK(HWReqs, HWCaps, N, Placement)
%given a placement with on(Function, Node, FunctionHWReqs), check if node has hw caps for new function
hwReqsOK((RAMReq,VCPUsReq,CPUReq),(RAMCap,VCPUsCap,CPUCap),N,P):-
    findall(HW, (member(on(_,N,HW),P)), OkHWs),
	sum_reqs(OkHWs, (AllocRAM,AllocVCPUs)),
    NewAllocRAM is AllocRAM + RAMReq, RAMCap >= NewAllocRAM,
	NewAllocVCPUs is AllocVCPUs + VCPUsReq, VCPUsCap >= NewAllocVCPUs,
	CPUCap >= CPUReq.
sum_reqs([],(0,0)).
sum_reqs([(RAM, VCPUs, _)|HWs],(NewSumRAM,NewSumVCPUs)):-
	sum_reqs(HWs, (SumRAM,SumVCPUs)),
	NewSumRAM is SumRAM + RAM,
	NewSumVCPUs is SumVCPUs + VCPUs.

/*	
hwReqsOK((RAMReq,VCPUsReq,CPUReq), (RAMCap,VCPUsCap,CPUCap), N, [], [(N,(RAMReq,VCPUsReq,CPUCap))]) :-
	RAMCap >= RAMReq, CPUCap >= CPUReq, VCPUsCap >= VCPUsReq.
hwReqsOK((RAMReq,VCPUsReq,CPUReq), (RAMCap,VCPUsCap,CPUCap), N, [(N,(AllocRAM,AllocVCPUs,CPUCap))|L], [(N,(NewAllocRAM,NewAllocVCPUs,CPUCap))|L]) :-
	NewAllocRAM is AllocRAM + RAMReq, RAMCap >= NewAllocRAM,
	NewAllocVCPUs is AllocVCPUs + VCPUsReq, VCPUsCap >= NewAllocVCPUs,
	CPUCap >= CPUReq.
hwReqsOK(HWReqs, HWCaps, N, [(N1,AllocHW)|L], [(N1,AllocHW)|NewL]) :-
	N \== N1, 
	hwReqsOK(HWReqs, HWCaps, N, L, NewL).
*/
%set_dif -> check the difference of two sets implemented by lists
set_dif(A,B) :- once(check_set_dif(A,B)).
check_set_dif(A,B) :- (member(X,A), \+ member(X,B)); (member(Y,B), \+ member(Y,A)).

%union_sort, append of list and sorting
union_sort(L1,L2,Lres):-
	append(L1,L2,Ltemp),
	sort(Ltemp, Lres).
union_sort(L1,L2,L3,Lres):-
	append(L1,L2,Ltemp),
	append(L3,Ltemp,Ltemp2),
	sort(Ltemp2, Lres).