import os
from numpy import empty
from sqlalchemy import null
import yaml
import yaml.representer
import re
import collections
import sys
#Infrastructure

def main():
    yaml.add_representer(str, literalPresenter)
    with open(sys.argv[2], "r") as stream:
        try:
            infrastructure=yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    #"application.yaml_prove"
    with open(sys.argv[1], "r") as stream:
        try:
            application=yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)        

    placement,application,infrastructure=createPlacement(application,infrastructure)
    #print(placement)
    
    placement=outPutPlace(placement,application,infrastructure)
    depserv_dict=createDeployment(placement,application)
    print(yaml.dump(depserv_dict))
    file = open("/Users/macintosh/Documents/tesi/funzioni/deployment_nopad.yaml", "w")
    yaml.dump(depserv_dict,file)
    file.close()
    print(placement)
    

def literalPresenter(dumper, data):
  if isinstance(data, str) and ("TCP" in data or "Mi" in data or "0m" in data):
      return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
  else:
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='')


def createDeployment(placement,application):
    deployment={}
    deployment['apiVersion']='v1'
    deployment['kind']='List'
    deployment['items']=[]

    
    for fun_name,node in placement.items():
        pad_dep= null
        pad_serv = null
        if 'ServicePad' not in fun_name:
            fun_dep={}
            fun_dep['apiVersion']='apps/v1'
            fun_dep['kind']='Deployment'
            fun_dep['metadata']={}
            fun_dep['metadata']['name']=fun_name
            fun_dep['spec']={}
            fun_dep['spec']['selector']={}
            fun_dep['spec']['selector']['matchLabels']={}
            fun_dep['spec']['selector']['matchLabels']['app']= fun_name
            fun_dep['spec']['template']={}
            fun_dep['spec']['template']['metadata']={}
            fun_dep['spec']['template']['metadata']['labels']= {}
            fun_dep['spec']['template']['metadata']['labels']['app']=fun_name
            fun_dep['spec']['template']['spec']={}
            fun_dep['spec']['template']['spec']['nodeName']=node
            fun_dep['spec']['template']['spec']['containers']=[]
            cont_details={}
            cont_details['name']=fun_name
            cont_details['ports']=[]
            cont_details['env']=[]
            worked_pad=[]
            worked_pad.append('dummy')
            for function in application['Deployments']:
                if function['Function']['id']==fun_name:
                    cont_details['image']=function['Function']['image']
                    cont_details['ports'].append({'containerPort':function['Function']['port']})
                    truedone=0
                    falsedone=0
                    for links in function['Function']['links']:
                        if function['Function']['type']=='branch' and 'btype' in links:
                                if links['btype']=='TRUE':
                                    for pname,nodename in placement.items():
                                        print(pname)
                                        if ('ServicePad' in pname and nodename==placement[links['fun']] and not(pname in worked_pad) and truedone==0):
                                                cont_details['env'].append({'name':str(links['name']),'value':'http://'+pname.lower()+':5000'})
                                                pad_dep,pad_serv=creaPad(placement[links['fun']],pname.lower(),links['fun'])
                                                deployment['items'].append(pad_dep)
                                                deployment['items'].append(pad_serv)
                                                worked_pad.append(pname)
                                                truedone=1
                                else:
                                    for pname,nodename in placement.items():
                                        print(pname)
                                        if ('ServicePad' in pname and nodename==placement[links['fun']] and not(pname in worked_pad) and falsedone==0):
                                                cont_details['env'].append({'name':str(links['name']),'value':'http://'+pname.lower()+':5000'})
                                                pad_dep,pad_serv=creaPad(placement[links['fun']],pname.lower(),links['fun'])
                                                deployment['items'].append(pad_dep)
                                                deployment['items'].append(pad_serv)
                                                worked_pad.append(pname)
                                                falsedone=1

                                        
        

                        else:
                            cont_details['env'].append({'name':links['name'],'value':links['value']})

            cont_details['imagePullPolicy']= 'Always'  
            cont_details['resources']={}
            cont_details['resources']['limits']={'memory':"200Mi",'cpu':"300m"}    
            fun_dep['spec']['template']['spec']['containers'].append(cont_details)
            fun_dep['spec']['template']['spec']['imagePullSecrets']=[]
            fun_dep['spec']['template']['spec']['imagePullSecrets'].append({'name':'regcred'})
            
            
            fun_serv={}
            fun_serv['apiVersion']='v1'
            fun_serv['kind']='Service'
            fun_serv['metadata']={}
            fun_serv['metadata']['name']=fun_name
            fun_serv['spec']={}
            fun_serv['spec']['selector']={}
            fun_serv['spec']['selector']['app']=fun_name
            fun_serv['spec']['ports']=[]
            for function in application['Deployments']:
                if function['Function']['id']==fun_name:
                    if function['Function']['exposed']:
                        fun_serv['spec']['type']='NodePort'
                        fun_serv['spec']['ports'].append({'protocol':"TCP",'port': function['Function']['port'],'targetPort': function['Function']['port'], 'nodePort': function['Function']['exposed_port']})
                    else:
                        fun_serv['spec']['type']='ClusterIP'
                        fun_serv['spec']['ports'].append({'protocol':"TCP",'port': function['Function']['port'],'targetPort': function['Function']['port']})
                

            deployment['items'].append(fun_dep)
            deployment['items'].append(fun_serv)
            
    return deployment
def creaPad(node,fun_name,link_fun):
            print("creo servicepad")
            print(fun_name)
            fun_dep={}
            fun_dep['apiVersion']='apps/v1'
            fun_dep['kind']='Deployment'
            fun_dep['metadata']={}
            fun_dep['metadata']['name']=fun_name
            fun_dep['spec']={}
            fun_dep['spec']['selector']={}
            fun_dep['spec']['selector']['matchLabels']={}
            fun_dep['spec']['selector']['matchLabels']['app']= fun_name
            fun_dep['spec']['template']={}
            fun_dep['spec']['template']['metadata']={}
            fun_dep['spec']['template']['metadata']['labels']= {}
            fun_dep['spec']['template']['metadata']['labels']['app']=fun_name
            fun_dep['spec']['template']['spec']={}
            fun_dep['spec']['template']['spec']['nodeName']=node
            fun_dep['spec']['template']['spec']['containers']=[]
            cont_details={}
            cont_details['name']=fun_name
            cont_details['ports']=[]
            cont_details['env']=[]
            cont_details['image']="albertosiemanuele/tesitestv1:fpaddef"
            cont_details['ports'].append({'containerPort':5000})
            cont_details['imagePullPolicy']= 'Always'  
            cont_details['resources']={}
            cont_details['resources']['limits']={'memory':"100Mi",'cpu':"100m"}   
            cont_details['env'].append({'name':'LINK','value':'http://'+link_fun+':5000'}) #toDo mettere dinamicamente il link alla funzione
            fun_dep['spec']['template']['spec']['containers'].append(cont_details)
            fun_dep['spec']['template']['spec']['imagePullSecrets']=[]
            fun_dep['spec']['template']['spec']['imagePullSecrets'].append({'name':'regcred'})
            
            
            fun_serv={}
            fun_serv['apiVersion']='v1'
            fun_serv['kind']='Service'
            fun_serv['metadata']={}
            fun_serv['metadata']['name']=fun_name
            fun_serv['spec']={}
            fun_serv['spec']['selector']={}
            fun_serv['spec']['selector']['app']=fun_name
            fun_serv['spec']['ports']=[]
            fun_serv['spec']['type']='ClusterIP'
            fun_serv['spec']['ports'].append({'protocol':"TCP",'port':5000,'targetPort': 5000})

            return (fun_dep,fun_serv)       
    
def createFunction(application):
    elem=""
    orchname={'name':"arOrch"}
    trigger={}
    trigger['name']=application['EventGenerator']['generatorId']
    trigger['sectypes']=[]
    for t in application['EventGenerator']['sectypes']:
        trigger['sectypes'].append(t)

    functions=[]
    for function in application['Deployments']:
        fun={}
        fun['op']='fun'
        fun['worked']=False
        fun['type']=function['Function']['type']
        fun['id']= function['Function']['id']
        if fun['type'] == 'par' and ('sync' in function['Function']) :
            fun['sync']=function['Function']['sync']
        fun['is_ingress']=function['Function']['is_ingress']
        fun['bindings']=[]
        if function['Function']['bindings']:
            for bind in function['Function']['bindings']:
                fun['bindings']=bind
        if function['Function']['latfromprev']:
            fun['lat']=function['Function']['latfromprev']
        else:
            fun['lat'] = 200
        fun['nexts']=[]    
        for var in function['Function']['links']:
            if var['next']:
                  fun['nexts'].append(var['fun'])
        functions.append(fun)
    head=[]
    head.append(orchname)
    head.append(trigger)
    chain=[]
    ingress_set=False
    for fun in functions:
        if fun["is_ingress"]:
          if not ingress_set:
            chain.append(fun)
            ingress_set=True
          else:
            raise("ERROR ONLY ONE INGRESS")
    print(functions)
    for fun in functions:
        
        if fun['type']=='par' and ('sync' in fun.keys()):
            for elem in functions:
                elem['id']==fun["sync"]
                fun["sync"]=elem
                
        fun['next_funs']=[]
        for next in fun['nexts']:
            for elem in functions:
                if elem['id']==next:
                    fun['next_funs'].append(elem)




    def createchain(fun):
        if fun['next_funs'] == []:
            return ""
        else:    
            for next in fun['next_funs']:
                next=createchain(next)
            return fun   

    for fun in chain:
        print(fun)
        if fun['is_ingress']:
            print('fun_next')
            print(fun['next_funs'])
            for next in fun['next_funs']:
                next=createchain(next)

        else:    
            pass
    
    def createchain_formatted(fun):
        print(fun)
        if fun['next_funs'] == []:
             elem= fun['op']+"("+fun['id']+",["
             if fun['bindings']!=[]:    
                elem+=str(fun['bindings'])    
             elem+="],"+str(fun['lat'])+")"
             return elem
        elif fun['type']=='node':
             elem='seq('
             elem+= fun['op']+"("+fun['id']+",["
             if fun['bindings']!=[]:    
                elem+=str(fun['bindings'])
             
             elem+="],"+str(fun['lat'])+"),"
             for next in fun['next_funs']:
                elem+=createchain_formatted(next)
                elem+=")"
             return elem 
        elif fun['type']=='par':
                elem='seq('    
                elem+= fun['op']+"("+fun['id']+",["
                if fun['bindings']!=[]:    
                    elem+=str(fun['bindings'])
                elem+="],"+str(fun['lat'])
                if 'sync' in fun.keys():
                    elem+="),seq("
                    print(fun['type'])
                    print(fun['sync'])
                else:
                    elem+=")," #il problema e' qui, se togli la parentesi funziona, ma poi non funziona piu' quello vecchio
                elem+="par(["
                for next in fun['next_funs']:
                    elem+=createchain_formatted(next)
                    elem+=","
                elem=elem[:-1]
                
                if 'sync' in fun.keys():
                        elem+="]),"+createchain_formatted(fun['sync'])+"))"
                else:
                    elem+="]))" # e aggiunta una qui...c'e' da capire per bene
                        
                return  elem
        elif fun['type']=='branch':
                elem='if('
                elem+= fun['op']+"("+fun['id']+",["
                if fun['bindings']!=[]:    
                    elem+=str(fun['bindings'])
                elem+="],"+str(fun['lat'])+"),"
                for next in fun['next_funs']:
                    elem+=createchain_formatted(next)
                    elem+=","
                elem=elem[:-1]   

                return elem+")"       
        else:
            raise("tipo non riconosciuto")                     
    print('chain')
    print(chain)
    for fun in chain:
        if fun['is_ingress']:
                elem=createchain_formatted(fun)
        else:    
            raise("Devi scegliere un ingress") 

    output="functionOrch("+head[0]['name']+",("+head[1]['name']+", ["
    for sec in head[1]['sectypes']:
        output+=sec+","
    output=output[:-1]
    output+="]),"
    print(elem)
    chain_ok=output+elem+")."       
    print(chain_ok)            
    return chain_ok
def createSecLevels(application,infrastructure):
        rows=[]



        #Questa parte la lascerei statica, si tratta delle regole per la definizione del lattice di sicurezza
        #% lattice of security types

        #LABELS
        
        if len(application['Lattice']['intermediate']) >0: #Se esistono livelli intermedi allora...
            if len(application['Lattice']['intermediate']) >1:
                pass #ToDo: Gestire piu' intermedi

            else: #gestiamo un solo livello intermediate
                row="g_lattice_higherThan("+application['Lattice']['top']['value']+","+application['Lattice']['intermediate'][0]['value']
                row+=")."
                rows.append(row)
                row="g_lattice_higherThan("+application['Lattice']['intermediate'][0]['value']+","+application['Lattice']['bottom']['value']
                row+=")."
                rows.append(row)
        else: #non ci sono livelli intermedi4
            row="g_lattice_higherThan("+application['Lattice']['top']['value']+","+application['Lattice']['bottom']['value']
            row+=")."  
            rows.append(row)       
       
        
        #COLORS
        #% lattice security types color for print, if do not needed use 'latticeColor(_,default).'

        if len(application['Lattice']['intermediate']) >0: #Se esistono livelli intermedi allora...
            if len(application['Lattice']['intermediate']) >1:
                pass #ToDo: Gestire piu' intermedi

            else: #gestiamo un solo livello intermediate
                row="latticeColor(top,"+application['Lattice']['top']['color']
                row+=")."
                rows.append(row)
                row="latticeColor(medium,"+application['Lattice']['intermediate'][0]['color']
                row+=")."
                rows.append(row)
                row="latticeColor(low,"+application['Lattice']['bottom']['color']
                row+=")."
                rows.append(row)
        else:
            #non ci sono livelli intermedi
            row="g_lattice_higherThan("+application['Lattice']['top']['value']+","+application['Lattice']['bottom']['value']
            row+=")."  
            rows.append(row)       
        #raw="g_lattice_higherThan(medium, low)."
    


        #
        #% node labeling
        raw="nodeLabel(NodeId, top)    :- node(NodeId,_,SecCaps,_,_), member(antiTamp, SecCaps), member(pubKeyE, SecCaps)."
        
        for secaps in application['NodeSecTypeCaps']:
            
            if secaps['label'] == application['Lattice']['top']['value']:
                row="nodeLabel(NodeId,"+ application['Lattice']['top']['value']+")    :- node(NodeId,_,SecCaps,_,_),"
                if secaps['present']:
                    for presentcap in secaps['present']:
                        row+="member("+presentcap+",SecCaps),"
                    row=row[:-1]    
                if secaps['absent']:        
                    for absentcaps in secaps['absent']:
                        row+="\+member("+absentcaps+",SecCaps),"    
                    row=row[:-1]
                row+="."
                
                rows.append(row) 
        for secaps in application['NodeSecTypeCaps']:        
            for intermediate in application['Lattice']['intermediate']:
                if secaps['label'] == intermediate['value']:
                    row="nodeLabel(NodeId,"+ intermediate['value']+")    :- node(NodeId,_,SecCaps,_,_),"
                    if secaps['present']:
                        for presentcap in secaps['present']:
                            row+="member("+presentcap+",SecCaps),"    
                    if secaps['absent']:        
                        for absentcaps in secaps['absent']:
                            row+="\+(member("+absentcaps+",SecCaps)),"    
                    row=row[:-1]
                    row+="."    
                    rows.append(row)

        for secaps in application['NodeSecTypeCaps']:        
            if secaps['label'] == application['Lattice']['bottom']['value']:
                row="nodeLabel(NodeId,"+ application['Lattice']['bottom']['value']+")    :- node(NodeId,_,SecCaps,_,_),"
                if secaps['present']:
                    for presentcap in secaps['present']:
                        row+="member("+presentcap+",SecCaps),"
                    row=row[:-1]    
                if secaps['absent']:        
                    for absentcaps in secaps['absent']:
                        row+="\+(member("+absentcaps+",SecCaps)),"    
                    row=row[:-1]
                row+="."
                rows.append(row)         
       
        #
        #%service labeling

        #definizioni
        for service in infrastructure['Services']:
            for servsectype in application['ServSecTypes']:
                if 'providers' in servsectype.keys():
                    for provider in servsectype['providers']:
                        if service['Service']['serviceProvider'] == provider['name']:
                            row="serviceLabel(SId,"
                            if 'serviceType' in provider.keys():
                                row+=provider['serviceType']+","
                            else:
                                row+='_,'    
                            row+=servsectype['label']+"):- service(SId,"+provider['name']+","
                            if 'serviceType' in provider.keys():
                                row+=provider['serviceType']+",_)."
                            else:
                                row+="_,_)." 
                            rows.append(row)
        #esclusioni
        for servsectype in application['ServSecTypes']:
            if 'exclude' in servsectype.keys():
                row="serviceLabel(SId, Type,"+servsectype['label']+"):- service(SId, Provider, Type, _),"
                for provider in servsectype['exclude']['providers']:
                    if 'serviceType' in provider.keys():
                        row+="\+((Provider=="+provider['name']+", Type =="+provider['serviceType']+")),"
                    else:
                        row+="\+(Provider=="+provider['name']+"),"
                row=row[:-1]
                row+="."    
                rows.append(row)        
                    

        for row in rows:
            print(row)

        return rows               
                               

def createPlacement(application,infrastructure):
    #scrive infrastructure.pl da usare con placer.pl
    with open("infrastructure.pl", "w") as infile:    
        for node in infrastructure['Nodes']:

            raw= "node("+node['Node']['id']+", "+node['Node']['providerId']+",["

            if node['Node']['securitySpecs']:
                for secspec in node['Node']['securitySpecs']:
                    raw+=secspec
                    if secspec != node['Node']['securitySpecs'][-1]:
                        raw+=','           
            raw+="],["
            if node['Node']['swCapabilities']:
                for swcap in node['Node']['swCapabilities']:
                    raw+=swcap
                    if swcap != node['Node']['swCapabilities'][-1]:
                        raw+=','

            raw+="],("+str(node['Node']['hwCapabilities']['memory'])+","+str(node['Node']['hwCapabilities']['cpu'])+","+str(node['Node']['hwCapabilities']['mhz'])+"))." 

            print(raw)
            infile.write(raw)
            infile.write('\n')

        raw="eventGenerator("+infrastructure['EventGenerator']['generatorId']+","+infrastructure['EventGenerator']['sourceNodes']+")."
        print (raw) 
        infile.write(raw)
        infile.write('\n')   

        for service in infrastructure['Services']:
            raw="service("+service['Service']['serviceId']+", "+service['Service']['serviceProvider']+", "+service['Service']['serviceType']+", "+service['Service']['deployedNode']+")."
            print(raw)
            infile.write(raw)
            infile.write('\n')
    
        raw="link(X,X,0)."
        print(raw)
        infile.write(raw)
        infile.write('\n')
        raw="link(X,Y,L) :- dif(X,Y), (latency(X,Y,L);latency(Y,X,L))."
        print(raw)
        infile.write(raw)
        infile.write('\n')
        for latency in infrastructure['Latencies']:
            raw="latency("+latency['Latency']['Node1']+", "+latency['Latency']['Node2']+", "+str(+latency['Latency']['value'])+")."
            print(raw)
            infile.write(raw)
            infile.write('\n')

        infile.close()



     #scrive application.pl da usare con placer.pl

    with open("application.pl", "w") as infile:        
        for funcReq in application['Requirements']:
            raw="functionReqs("+funcReq['Function']['id']+",["
            if funcReq['Function']['sw']:
                    for swreq in funcReq['Function']['sw']:
                        raw+=swreq
                        raw+=','
                    raw=raw[:-1]     
            raw+="],("+str(funcReq['Function']['hw']['mem'])+","+str(funcReq['Function']['hw']['cpu'])+","+str(funcReq['Function']['hw']['mhz'])+"),["
            if funcReq['Function']['services']:
                    for serv in funcReq['Function']['services']:
                        raw+="("+serv['service']['id']+","+str(serv['service']['latency'])+")"
                        raw+=','
                    raw=raw[:-1]     
            raw+="])."        
            infile.write(raw)
            infile.write('\n')
        for funBeh in application['Behaviours']:
            raw="functionBehaviour("+funBeh['Function']['id']+",["
            if funBeh['Function']['inputs']:
                for input in funBeh['Function']['inputs']:
                    raw+=input
                    raw+=','
                raw=raw[:-1]   
            raw+="],["
            if funBeh['Function']['fun']:
                for fun in funBeh['Function']['fun']:
                    raw+=fun
                    raw+=','
                raw=raw[:-1]   
            raw+="],["
            if funBeh['Function']['outputs']:
                for output in funBeh['Function']['outputs']:
                    raw+=output
                    raw+=','  
                raw=raw[:-1]          
            raw+="])"
            if funBeh['Function']['rule'] != []:
                raw+=":- maxType(U, Draw, ScAr)" #ToDO: comporlo leggendo dal file
            raw+="."
            infile.write(raw)
            infile.write('\n') 

       
        #raw="functionOrch(arOrch,(userDevice, [top,low,medium]),seq(seq(fun(flogin,[myUserDb],25),fun(far,[],30)),par([if(fun(fdcc,[],30), fun(fcheckdcc,[],30), fun(frules,[],30)),seq(fun(fcrop,[],30),fun(fgeo,[],30))])))." 
        
        infile.write('%versione automatica')
        infile.write('\n')
        raw=createFunction(application)
        infile.write(raw)
        infile.write('\n')
        infile.write('%versione automatica')
        infile.write('\n')
        rows=createSecLevels(application,infrastructure) 

        for row in rows:
            infile.write(row)
            infile.write('\n')
        

    infile.close()

    placement=os.popen('swipl -s placer.pl --on-warning=halt --on-error=halt').read()

    return placement,application,infrastructure

#restituisce la coppia funzione:nodo
def outPutPlace(placement,application,infrastructure):

    pos_fun={}
    pos_node={}
    for fun in application['Requirements']:
        matches=(re.finditer(fun['Function']['id'], placement))
        if matches:
            pos_fun[fun['Function']['id']]=[match.end() for match in matches]
    for fun in ['fServicePad1','fServicePad2','fServicePad3','fServicePad4','fServicePad5','fServicePad6','fServicePad7','fServicePad8']:
        matches=(re.finditer(fun, placement))
        if matches:
            pos_fun[fun]=[match.end() for match in matches]

    for node in infrastructure['Nodes']:
        matches=(re.finditer("],"+node['Node']['id'], placement))
        if matches:
            pos_node[node['Node']['id']]=[match.end() for match in matches]

  

    mapping={}
    for fkey,fvalue in pos_fun.items():
        mapping[fkey]={}
        if fvalue:
           for nkey,nvalue in pos_node.items():
               for nvalue_sing in nvalue:
                   
                   if (nvalue_sing-fvalue[0])>0:
                       
                       dict={nkey:nvalue_sing}
                       
                       mapping[fkey][nkey]=nvalue_sing
                       
                       break

    finalmap={}
    for fvalue,pot_place in mapping.items():

        if fvalue:
            for key,value in sorted(pot_place.items(), key=lambda x: x[1]):
              
                finalmap[fvalue]=key
                break
            

    
    return finalmap    

if __name__ == "__main__":
    main()


