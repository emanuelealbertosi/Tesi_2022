node(private1, privateCitizen1,[],[js,docker],(2048,2,2500)).
node(private2, privateCitizen2,[pubKeyE],[py3,docker],(2048,2,1500)).
node(isprouter, telco,[pubKeyE,antiTamp],[js,py3,docker],(3500,5,2000)).
node(antenna1, telco,[pubKeyE,antiTamp],[js,py3,docker],(2048,4,1500)).
node(antenna2, telco,[pubKeyE],[py3,numPy,docker],(2048,4,1500)).
node(labserver, university,[pubKeyE,antiTamp],[py3,numPy,docker],(2048,4,2000)).
node(officeserver, university,[],[py3,docker],(2048,2,1000)).
node(switch, university,[pubKeyE],[py3,js,docker],(2048,2,2000)).
node(cloudnode, cloudProvider,[pubKeyE,antiTamp],[py3,js,numPy],(inf,inf,inf)).
eventGenerator(userDevice,isprouter).
service(myusers, appOp, userDB, isprouter).
service(mymaps, appOp, maps, switch).
service(mycrop, appOp, ai, antenna1).
service(greenpassapi, pa, checkGp, isprouter).
service(rules, appOp, checkRules, isprouter).
service(sendmail, appOp, sendMail, antenna1).
service(dccchk, appOp, dccchk, antenna1).
link(X,X,0).
link(X,Y,L) :- dif(X,Y), (latency(X,Y,L);latency(Y,X,L)).
latency(cloudnode, isprouter, 1).
latency(cloudnode, antenna1, 1).
latency(cloudnode, private1, 1).
latency(cloudnode, private2, 1).
latency(cloudnode, switch, 1).
latency(cloudnode, officeserver, 1).
latency(cloudnode, labserver, 1).
latency(cloudnode, antenna2, 1).
latency(isprouter, antenna1, 1).
latency(isprouter, antenna2, 1).
latency(isprouter, private1, 1).
latency(isprouter, private2, 1).
latency(isprouter, switch, 1).
latency(isprouter, officeserver, 1).
latency(isprouter, labserver, 1).
latency(antenna1, antenna2, 12).
latency(antenna1, private1, 14).
latency(antenna1, private2, 7).
latency(antenna1, switch, 13).
latency(antenna1, officeserver, 20).
latency(antenna1, labserver, 18).
latency(antenna2, private1, 5).
latency(antenna2, private2, 19).
latency(antenna2, switch, 12).
latency(antenna2, officeserver, 19).
latency(antenna2, labserver, 20).
latency(private1, private2, 21).
latency(private1, switch, 11).
latency(private1, officeserver, 18).
latency(private1, labserver, 16).
latency(private2, switch, 20).
latency(private2, officeserver, 27).
latency(private2, labserver, 25).
latency(switch, officeserver, 7).
latency(switch, labserver, 5).
latency(officeserver, labserver, 7).
