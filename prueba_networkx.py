#  C:\Users\ggalv\Google Drive\Respaldo\TESIS\Trabajo con networkx       python prueba_networkx.py

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import heapq as hq
import math as mt
import operator
import time


resultados=open("resultados.txt","w")
for w in range(23):
	start=time.time()
	dataset='C:/Users/Administrador/Google Drive/Respaldo/TESIS/Trabajo con Networkx/instancias/p'+str(w+1)
	resultados.write('INSTANCIA p'+str(w+1)+'-----------------------------------------'+'\n')
	# print("dataset= ",dataset)
	print(" ")
	print("------------------------------------------------------------------------------------")
	print("------------------------------------------------------------------------------------")
	print("ECECUTARE INSTANCIA P"+str(w+1))

	def lectura_datos(dataset):
		archivo = pd.read_csv(dataset,delim_whitespace=True,header=None)
		# print(archivo)
		print(" ")
		tamaño_del_data=archivo.shape
		c=archivo.iloc[tamaño_del_data[0]-1:tamaño_del_data[0]]
		c=c.as_matrix()
		N=int(c[0][2]+c[0][3])
		C=int(c[0][2])
		K=int(c[0][1])
		D=int(c[0][3])
		P=2
		#creo las demandas-----------------------------------
		dem1=(archivo.iloc[0:int(c[0][2]):,4].as_matrix())
		dem2=dem1*2
		dem=[]
		for i in range(int(c[0][2])):
			dem.append(dem1[i])
			dem.append(dem2[i])
		dem=np.array(dem)
		dem=dem.reshape(int(c[0][2]),P)
		# print(dem)

		#creo las distancias----------------------------------
		dist1=(archivo.iloc[0:int(c[0][2]+c[0][3]):,1]).as_matrix()                 #coordenada X
		dist2=(archivo.iloc[0:int(c[0][2]+c[0][3]):,2]).as_matrix().astype('int')	#coordenada Y
		dist=[]
		# print("dist1=",len(dist1))
		# print("dist2=",len(dist2))	
		# print("c[0][2]=",range(1,int(c[0][2]+c[0][3])))	
		for i in range(int(c[0][2]+c[0][3])):
			for j in range(int(c[0][2]+c[0][3])):
				if i==j:
					dist.append(99999)
				elif i!=j:
					dist.append(mt.sqrt(pow(dist1[i]-dist2[i],2) + pow(dist1[j]-dist2[i],2)))
		distancias=np.array(dist)
		distancias=distancias.reshape(int(c[0][2]+c[0][3]),int(c[0][2]+c[0][3]))
		# print(dist)

		#creo camion asignado--------------------------------
		camion_asignado=[]
		for i in range(int(D)):
			camion_asignado.append(int(K))	

		#creo inventarios-------------------------------------
		inv1=sum(dem1)
		inv2=sum(dem2)
		# print(inv1)
		# print(inv2)
		inv=[]
		for i in range(int(D)):
			inv.append((inv1/int(D))+100)
			inv.append((inv2/int(D))+100)
		inventario=np.array(inv)
		inventario=inventario.reshape(int(D),int(P))
		# print(inventario)

		#obtengo capacidad de los vehiculos-------------------
		V=int((int(sum(sum(dem)))/(K*D))+0.3*(int(sum(sum(dem)))/(K*D)))
		# print("Capacidad de los vehiculos=",V)
		
		return(N,K,D,P,V,dem,distancias,camion_asignado,inventario)


	N,K,D,P,V,dem,distancias,camion_asignado,inventario=lectura_datos(dataset)
	print("N=",N)
	print("K=",K)
	print("D=",D)
	print("P=",P)
	print("V=",V)



	#Diccionario de Demandas--------------------------------
	demanda_nodos={}
	i=0
	for i in range(N-D):
		demanda_nodos[i]=list(dem[i])
	# print("demanda_nodos",demanda_nodos)

	#Diccionario de Inventarios-----------------------------
	inventario_depositos={}
	i=0
	for i in range(D):
		inventario_depositos[(N-D)+i]=list(inventario[i])
	print("inventario_depositos=",inventario_depositos)

	#Diccionario de Distancias-----------------------------
	distancias_nodos={}
	i=0
	for i in range(N):
		for j in range(N):
			distancias_nodos[(i,j)]=int(distancias[i][j])
		j=0	


	#Diccionario de Camiones asignados---------------------
	camiones_asignados={}
	i=0
	for i in range(D):
		# print("Camion_asignado=",camion_asignado)
		# print("camiones_asignados=",camiones_asignados)
		camiones_asignados[(N-D)+i]=camion_asignado[i]
	print("camiones_asignados=",camiones_asignados)

	#clase camion-----------------------------------------
	class Camion(object):
		"""docstring for camion"""
		def __init__(self, id,deposito):
			self.nombre="camion"+str(id)
			self.carga=0
			self.deposito=deposito
			self.posicion_actual=deposito
			self.nodo_visitado=[]
	#Creo diccionario con la clase camion---------------		
	m=0
	n=int(N-D)
	d={}
	for i in range(int(D)):
		# print(i)
		# print(n)
		# print(int(camiones_asignados[n]))
		for j in range(int(camiones_asignados[n])):
			d["camion"+str(m)]=Camion(m,n)
			m+=1
		n+=1
	print("Nombre camiones=",d.keys())
	print("Diccionario de camiones=",d["camion0"].posicion_actual)



	#inicializo vectores con nodos por cubrir--------------
	i=0
	C=N-D
	nodos_por_visitar=[]
	for i in range(0,C):
		nodos_por_visitar.append(i)
	print("nodos_por_visitar=",nodos_por_visitar)


	#Creo grafo con clases nodos y edge--------------------
	G=nx.complete_graph(N)
	nx.set_node_attributes(G, demanda_nodos,'Demanda')
	nx.set_node_attributes(G, inventario_depositos,'Inventario')
	nx.set_node_attributes(G,camiones_asignados,'Camion_asignado')
	nx.set_edge_attributes(G,distancias_nodos,'Distancia')
	# print("diccionario en nx",len(nx.get_edge_attributes(G,'Distancia')))

	# print("Distancia grafo")
	# sorted_x = sorted(nx.get_edge_attributes(G,'Distancia').items(), key=operator.itemgetter(0))
	# print("sorted_x",sorted_x)

	# print("Valor distancia minima=",nx.get_edge_attributes(G,'Distancia'))
	# print(len(nx.get_edge_attributes(G,'Distancia')))
	# sorted_x = sorted(nx.get_edge_attributes(G,'Distancia').items(), key=operator.itemgetter(0))
	# print("sorted_x",sorted_x)

	#funcion camion en uso----------------------------------
	def camion(c):
		camion_en_uso1=d['camion'+str(c)].nombre
		print(type(camion_en_uso1))
		return(camion_en_uso1)

	#funcion llenado camion---------------------------------
	def llenar_camion(k,carga_actual,inventario,demanda,V,cambiar_camion):
		if carga_actual<V:
			if demanda<=inventario and demanda<(V-carga_actual): #la demanda del producto puede ser satisfecha por completo, hay inventario para hacerlo y espacio para hacerlo
				print("EJECUTE CASO 0")
				carga_actual+=demanda				
				inventario-=demanda
				demanda=0

			elif demanda>inventario and demanda<(V-carga_actual): #se puede satisfacer solo una parte de la demanda del producto, por falta de inventario
				print("EJECUTE CASO 1")
				carga_actual+=inventario
				demanda-=inventario
				inventario=0

			elif  demanda<=inventario and demanda>(V-carga_actual):	#Se puede satisfacer solo parte de la demanda, ya que no hay espacio para llevar más		
				print("EJECUTE CASO 2")
				demanda-=(V-carga_actual)				
				inventario-=(V-carga_actual)
				carga_actual+=(V-carga_actual)			
							
			elif demanda>inventario and demanda>(V-carga_actual): #Se puede satisfacer una parte de la demana ya que no hay ni inventario ni espacio suficienta para satisfacer más
				if (V-carga_actual)<=inventario:	#Mi limitante es el inventario 
					print("EJECUTE CASO 3.1")
					demanda-=(V-carga_actual)
					inventario-=(V-carga_actual)
					carga_actual=V					
				elif(V-carga_actual)>inventario:	#mi limitante es la capacidad de carga
					print("EJECUTE CASO 3.2")
					carga_actual+=inventario
					demanda-+inventario
					inventario=0	

		print("carga actual dentro del for= ",int(carga_actual)) #cumplio el limite de carga del camion			
		if int(carga_actual)>=V:
			print("HOLA")
			cambiar_camion=1 	
			print("cambiar_camion= ",cambiar_camion)
		return(carga_actual,inventario,demanda,cambiar_camion)	 





	#Inicio Iteracion---------------------------------------
	iteracion=1
	c=0
	cambiar_camion=0
	camion_en_uso=camion(c)
	posicion_actual=d[camion_en_uso].posicion_actual
	f=1
	distancia_total=0
	lista_tabu=[]
	total_recorrido=0
	while  len(nodos_por_visitar)!=0:

		print(" ")
		print("INICIO ITERACION "+str(iteracion))

		#selecciono camion a usar-------------------------------
		print("nodos_por_visitar",nodos_por_visitar)
		print("c=",c)
		camion_en_uso=camion(c)
		print(camion_en_uso)
		z=[(posicion_actual,x) for x in nodos_por_visitar]

		#Busco distancia minima a siguiente nodo----------------
		dictfilt=lambda x,y:dict([(i,x[i])for i in x if i in set(y)])
		distancias_filtradas=dictfilt(distancias_nodos,z)
		distancia_minima=min(distancias_filtradas, key=distancias_filtradas.get)
		print("Valor distancia minima= ",distancias_filtradas[distancia_minima])
		total_recorrido+=distancias_filtradas[distancia_minima]
		print("distancia_minima=",distancia_minima)
		nodo_siguiente=distancia_minima[1]
		print("nodo_siguiente=",nodo_siguiente)

		# print("Demanda del nodo=",(nx.get_node_attributes(G,'Demanda')))

		#lleno camion
		for k in range(len(nx.get_node_attributes(G,'Demanda')[nodo_siguiente])):
			carga_actual=d[camion_en_uso].carga
			inventario=int(nx.get_node_attributes(G,'Inventario')[d[camion_en_uso].deposito][k])
			demanda=nx.get_node_attributes(G,'Demanda')[nodo_siguiente][k]
			print("carga_actual,inventario,demanda",carga_actual,inventario,demanda)
			carga_actual,inventario,demanda,cambiar_camion=llenar_camion(k,carga_actual,inventario,demanda,V,cambiar_camion)       #uso la funcion llenar camion
			print("Valores fuera de la funcion carga_actual,inventario,demanda",carga_actual,inventario,demanda)
			d[camion_en_uso].carga=carga_actual
			nx.get_node_attributes(G,'Inventario')[d[camion_en_uso].deposito][k]=inventario
			nx.get_node_attributes(G,'Demanda')[nodo_siguiente][k]=demanda
			if cambiar_camion==1: #El camion cumplio con su carga maxima
				print("EJECUTO BREAK")
				break
		print("Demanda afuera del for",nx.get_node_attributes(G,'Demanda')[nodo_siguiente])
		
		#Paso a la ciudad a la lista de nodos visitados
		true5=all(nx.get_node_attributes(G,'Demanda')[nodo_siguiente][i]==0 for i in range(len(nx.get_node_attributes(G,'Demanda')[nodo_siguiente])))
		print("true5= ",true5)
		if true5==True: #Toda la demanda del nodo fue satisfecha
			nodos_por_visitar.remove(nodo_siguiente)
			posicion_actual=nodo_siguiente
			d[camion_en_uso].nodo_visitado.append(nodo_siguiente)
		elif true5==False: #La demanda del nodo no pudo ser satisfecha pero el nodo se agrega a una lsita tabu para que no sea visitado de nuevo por el mismo camion
			lista_tabu.append(nodo_siguiente)		
			nodos_por_visitar.remove(nodo_siguiente)
			posicion_actual=nodo_siguiente
			d[camion_en_uso].nodo_visitado.append(nodo_siguiente)

		#Reviso el inventario que hay en el deposito
		print("Inventario del deposito=",nx.get_node_attributes(G,'Inventario')[d[camion_en_uso].deposito])
		true6=all(nx.get_node_attributes(G,'Inventario')[d[camion_en_uso].deposito][i]==0 for i in range(len(nx.get_node_attributes(G,'Inventario')[d[camion_en_uso].deposito])))	
		print("true6=",true6)
		if true6==True: #No queda inventario en el deposito
			print("CAMBIO CAMION POR FALTA DE INVENTARIO")
			c+=1		#cambio de camion	
			cambiar_camion=0
			for i in range(len(lista_tabu)):
				nodos_por_visitar.append(lista_tabu[i]) 
			lista_tabu=[]	

		#Reviso la carga del camion para ver si es necesario cambiarlo
		print("Lista tabu= ",lista_tabu)
		if cambiar_camion==1:
			print("CAMBIO CAMION POR CARGA MAXIMA")
			c+=1
			cambiar_camion=0
			if len(lista_tabu)!=0:
				for i in range(len(lista_tabu)):
					nodos_por_visitar.append(lista_tabu[i]) 
				lista_tabu=[]		 
							 

		# if iteracion>=2:
		# 	break	

		print(" ")		
		print("POST LLENADO DE CAMION")		
		print("Demanda del nodo=",nx.get_node_attributes(G,'Demanda')[nodo_siguiente])		
		print("Inventario del deposito=",nx.get_node_attributes(G,'Inventario')[d[camion_en_uso].deposito])
		print("Carga del camion=", d[camion_en_uso].carga)
		print("nodo visitado=",d[camion_en_uso].nodo_visitado)

		iteracion+=1
		del camion_en_uso		


	# print(G.nodes.data())
	# print(G.number_of_nodes())
	# print(G.number_of_edges())	
	# print(list(G.nodes))

	end=time.time()
	print("Tiempo de ejeución= ",end-start)
	resultados.write("Tiempo de ejeución= "+str(end-start)+'\n')
	print("Total recorrido",total_recorrido)
	resultados.write("Total recorrido= "+str(total_recorrido)+'\n')
	for i in range(int(K*D)):
		print("nodos visitados por camion"+str(i),d["camion"+str(i)].nodo_visitado)
		resultados.write("nodos visitados por camion"+str(i)+'='+str(d["camion"+str(i)].nodo_visitado)+'\n')
	


