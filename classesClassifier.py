#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	classesHMMClassifier.py


	Training gesture 1 Hand (finger only extension is considered)
	This module is used for training the 2 level classifier (Random Forest)
	and save the parameter of the model in folder modelClassifier.


"""

__author__ = "Giuseppe Francesco Rigano"
__email__ = "giusepperig48@gmail.com"

import os, sys, glob
import numpy as np
import random
import math
from sklearn.externals import joblib
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier

from pybrain.datasets            import ClassificationDataSet
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer

import settings
import dataset
import math


np.set_printoptions(threshold=np.nan)

clf = [0] * settings.K
listGesture=[]

#return a list of all gesture in a path
def getGestureName(datasetPath):

	instanceList=[]

	for gestureName in os.listdir(datasetPath):

		# ignoring .DS_Store for Mac machines
		if (gestureName == '.DS_Store'):
			continue
		if (gestureName == '._.DS_Store'):
			continue
		if ('._' in gestureName):
			continue
		instanceList.append(gestureName)


	return instanceList

def average(num1,num2):
	av=num1 + num2 /2
	return av

def dotproduct (x,y,z,a,b,c):

	val=x*a + y*b +z*c
	return val

def norma(x,y,z):

	val=math.sqrt(x**x +y**y +z**z)
	return val

def medianFilter(instance):

	count=[]

	for l in range(0,5):
		count.append(0)

	for i in range(0,len(instance)):

		for u in range(0,len(count)):
			count[u]=0
		s=0
		if i>5:
			s=i-5


		for k in range(s,i):
			#print "aaa" + str(i-s)
			if instance[k][10]==True:
				count[0]=count[0]+1
			if instance[k][17]==True:
				count[1]=count[1]+1
			if instance[k][24]==True:
				count[2]=count[2]+1
			if instance[k][31]==True:
				count[3]=count[3]+1
			if instance[k][38]==True:
				count[4]=count[4]+1

		e=len(instance)
		if i+5<len(instance):
			e=i+5

		for k in range(i,e):
			#print "bbb"+str(e-i)
			if instance[k][10]==True:
				count[0]=count[0]+1
			if instance[k][17]==True:
				count[1]=count[1]+1
			if instance[k][24]==True:
				count[2]=count[2]+1
			if instance[k][31]==True:
				count[3]=count[3]+1
			if instance[k][38]==True:
				count[4]=count[4]+1

		#print count

		global mx,my,mz,dx,dy,dz
		mx=0
		my=0
		mx=0
		dx=0
		dy=0
		dz=0



		if instance[i][10]==False and count[0]>5:
			if i>0:
				mx=average(instance[i-1][11],instance[i+1][11])
				my=average(instance[i-1][12],instance[i+1][12])
				mz=average(instance[i-1][13],instance[i+1][13])
				dx=average(instance[i-1][14],instance[i+1][14])
				dy=average(instance[i-1][15],instance[i+1][15])
				dz=average(instance[i-1][16],instance[i+1][16])

		if instance[i][10]== False and count[0]>5:
			instance[i][10]=True
			instance[i][11]=mx
			instance[i][12]=my
			instance[i][13]=mz
			instance[i][14]=dx
			instance[i][15]=dy
			instance[i][16]=dz




		if instance[i][17]==False and count[1]>5:
			if i>0:
				mx=average(instance[i-1][18],instance[i+1][18])
				my=average(instance[i-1][19],instance[i+1][19])
				mz=average(instance[i-1][20],instance[i+1][20])
				dx=average(instance[i-1][21],instance[i+1][21])
				dy=average(instance[i-1][22],instance[i+1][22])
				dz=average(instance[i-1][23],instance[i+1][23])

		if instance[i][17]== False and count[1]>5:
			instance[i][17]=True
			instance[i][18]=mx
			instance[i][19]=my
			instance[i][20]=mz
			instance[i][21]=dx
			instance[i][22]=dy
			instance[i][23]=dz




		if instance[i][24]==False and count[2]>5:
			if i>0:
				mx=average(instance[i-1][25],instance[i+1][25])
				my=average(instance[i-1][26],instance[i+1][26])
				mz=average(instance[i-1][27],instance[i+1][27])
				dx=average(instance[i-1][28],instance[i+1][28])
				dy=average(instance[i-1][29],instance[i+1][29])
				dz=average(instance[i-1][30],instance[i+1][30])

		if instance[i][24]== False and count[2]>5:
			instance[i][24]=True
			instance[i][25]=mx
			instance[i][26]=my
			instance[i][27]=mz
			instance[i][28]=dx
			instance[i][29]=dy
			instance[i][30]=dz




		if instance[i][31]==False and count[3]>5:
			if i>0:
				mx=average(instance[i-1][32],instance[i+1][32])
				my=average(instance[i-1][33],instance[i+1][33])
				mz=average(instance[i-1][34],instance[i+1][34])
				dx=average(instance[i-1][35],instance[i+1][35])
				dy=average(instance[i-1][36],instance[i+1][36])
				dz=average(instance[i-1][37],instance[i+1][37])

		if instance[i][31]== False and count[3]>5:
			instance[i][31]=True
			instance[i][31]=mx
			instance[i][33]=my
			instance[i][34]=mz
			instance[i][35]=dx
			instance[i][36]=dy
			instance[i][37]=dz




		if instance[i][38]==False and count[4]>5:
			if i>0:
				mx=average(instance[i-1][39],instance[i+1][39])
				my=average(instance[i-1][40],instance[i+1][40])
				mz=average(instance[i-1][41],instance[i+1][41])
				dx=average(instance[i-1][42],instance[i+1][42])
				dy=average(instance[i-1][43],instance[i+1][43])
				dz=average(instance[i-1][44],instance[i+1][44])

		if instance[i][38]== False and count[4]>5:
			instance[i][38]=True
			instance[i][39]=mx
			instance[i][40]=my
			instance[i][41]=mz
			instance[i][42]=dx
			instance[i][43]=dy
			instance[i][44]=dz


	return instance


# return a list of cluster
def readCluster(clusterPath):
	clusters = [0] * settings.K
	c = 0

	for clust in os.listdir(clusterPath):

		# ignoring .DS_Store for Mac machines
		if (clust == '.DS_Store'):
			continue
		if ('._' in clust):
			continue

		if c>=settings.K:
			break
		# reading data from file file
		infile = open(clusterPath + "cluster" + str(c) + ".txt")
		tmpLine = infile.read()

		# saving clusters
		clusters[c] = tmpLine.split('\n')

		infile.close()
		c += 1

	return clusters

#return a list that contains the longest instance for each class considering the key frame extraction first
def getMaxKeyFrameLengthCluster(datasetPath,clustersPath):
	clusters = []
	maxLengthInstance = [0] * settings.K  # contains the number of frame of longest instance for each cluster

	clusters = readCluster(clustersPath)

	# for each cluster
	for i in range(0, settings.K):

		maxcluster = 0

		# for each gesture in a cluster
		for gestureName in clusters[i]:

			# get list instance of a gesture, there are several (different people,same person)
			instanceList = os.listdir(datasetPath + gestureName + "/")

			#instanceList.remove('.DS_Store')
			#instanceList.remove('._.DS_Store')
			for inst in instanceList:
				if ('._' in inst):
					instanceList.remove(inst)

			# get instance in list
			# maxlocal=0
			for tmpinstance in instanceList:
				if ('._' in tmpinstance):
					continue

				instance = dataset.getInstanceDataList(datasetPath + gestureName + "/" + tmpinstance)
				# if(len(instance)>maxlocal):
				# maxlocal=len(instance)

				keyframeinstance=extractKeyFrame(instance)
				if (len(keyframeinstance) > maxcluster):
					maxcluster = len(keyframeinstance)

				# print "lenlocale"+ str(maxlocal)

		# print "lenglobal"+ str(maxcluster)

		maxLengthInstance[i] = maxcluster
		maxcluster = 0

	return maxLengthInstance

#return a list that contains the longest instance for each class
def getMaxLengthCluster(datasetPath,clustersPath):
	clusters = []
	maxLengthInstance = [0] * settings.K  # contains the number of frame of longest instance for each cluster

	clusters = readCluster(clustersPath)

	# for each cluster
	for i in range(0, settings.K):

		maxcluster = 0

		# for each gesture in a cluster
		for gestureName in clusters[i]:

			# get list instance of a gesture, there are several (different people,same person)
			instanceList = os.listdir(datasetPath + gestureName + "/")

			#instanceList.remove('.DS_Store')
			#instanceList.remove('._.DS_Store')
			for inst in instanceList:
				if ('._' in inst):
					instanceList.remove(inst)

			# get instance in list
			# maxlocal=0
			for tmpinstance in instanceList:
				if ('._' in tmpinstance):
					continue

				instance = dataset.getInstanceDataList(datasetPath + gestureName + "/" + tmpinstance)
				# if(len(instance)>maxlocal):
				# maxlocal=len(instance)
				if (len(instance) > maxcluster):
					maxcluster = len(instance)

				# print "lenlocale"+ str(maxlocal)

		# print "lenglobal"+ str(maxcluster)

		maxLengthInstance[i] = maxcluster
		maxcluster = 0

	return maxLengthInstance

# add repeat value until reach n
#ex [[2,3],[4,5]] -> [[2,3][4,5],[2,3].[4,5]]
def repeatPadding(instance, n):

	original_len=len(instance)

	for i in range(0,n):
		k=i
		if(k==original_len):
			k=0
		instance.append(instance[k])

	return instance

def repeatPaddingReverseHMM(instance, n):

	instance=np.array(instance).tolist()
	k=-1
	a=1
	conta=0
	while a == 1:
		old=len(instance)-1
		for i in range(len(instance)-1,k,-1):
			conta=conta+1
			if (conta > n):
				a=0
				break
			instance.append(instance[i])
		k=old

	return instance

# add repeat value until reach n in reverse order
#ex [[2,3],[4,5]] -> [[2,3][4,5],[4,5].[2,3]]
def repeatPaddingReverse(instance, n):


	k=-1
	a=1
	conta=0
	while a == 1:
		old=len(instance)-1
		for i in range(len(instance)-1,k,-1):
			conta=conta+1
			if (conta > n):
				a=0
				break
			instance.append(instance[i])
		k=old

	return instance

# add padding n times at the end
def addPaddingEndInstance(instance, n):
	for i in range(0, n):
		instance.append(instance[len(instance) - 1])

	return instance

#not used
def trainSingleGesture(datasetPath, maxLengthInstance):
	clusters = []

	clusters = readCluster(clustersPath)

	# for each cluster
	#for i in range(0, settings.K):
	for i in range(1,2):

		num_gesture=0
		# for each gesture in a cluster
		for gestureName in clusters[i]:
			label = []
			listInstances = []  # contains istance of a specific cluster

			clf[num_gesture] = RandomForestClassifier(n_estimators=100)

			# get list instance of a gesture, there are several (different people,same person)
			instanceList = os.listdir(datasetPath + gestureName + "/")
			# instanceList.remove('.DS_Store')
			instanceList.remove('._.DS_Store')
			for inst in instanceList:
				if ('._' in inst):
					instanceList.remove(inst)

			for tmpinstance in instanceList:
				if ('._' in tmpinstance):
					continue
				instance = dataset.getInstanceDataList(datasetPath + gestureName + "/" + tmpinstance)
				print"lenistanza prima"
				print len(instance)
				rate=float(maxLengthInstance[i]/len(instance))

				instancepadded = addPaddingEndInstance(instance, maxLengthInstance[i] - len(instance))
				#instancepadded = repeatPadding(instance, maxLengthInstance[i] - len(instance))
				print"lenistanza dopo"
				print len(instancepadded)
				# convert from 2D in 1D
				normalizedInstance = np.reshape(instancepadded, len(instancepadded) * settings.F)
				listInstances.append(normalizedInstance)
				label.append(listGesture.index(gestureName))

			print label

			clf[num_gesture] = clf[num_gesture].fit(listInstances, label)


			# saving parameters of the trained model

			joblib.dump(clf[num_gesture], "modelSingleClassifier//"+gestureName + ".pkl")
			print"Save MODEL "+ gestureName
			num_gesture= num_gesture+1
			print "label"
			print label
	print clf
	return 1

#Train the classifier
def trainClassifier(datasetPath, maxLengthInstance):
	clusters = []

	clusters = readCluster(clustersPath)

	# for each cluster
	for i in range(0, settings.K):

		listInstances = []  # contains istance of a specific cluster
		label = []

		#clf[i]=tree.DecisionTreeClassifier()
		#clf[i] = RandomForestClassifier(n_estimators=100)
		clf[i]=ExtraTreesClassifier(n_estimators=100)


		# for each gesture in a cluster
		for gestureName in clusters[i]:

			# get list instance of a gesture, there are several (different people,same person)
			instanceList = os.listdir(datasetPath + gestureName + "/")
			# instanceList.remove('.DS_Store')
			#instanceList.remove('._.DS_Store')
			for inst in instanceList:
				if ('._' in inst):
					instanceList.remove(inst)

			for tmpinstance in instanceList:
				if ('._' in tmpinstance):
					continue
				instance = dataset.getInstanceDataList(datasetPath + gestureName + "/" + tmpinstance)

				#extract key frame
				keyframeinstance=extractKeyFrame(instance)

				#add padding
				if(maxLengthInstance[i]>len(keyframeinstance)):
					keyframeinstance = repeatPaddingReverse(keyframeinstance, maxLengthInstance[i] - len(keyframeinstance))


				# convert from 2D in 1D
				normalizedInstance = np.reshape(keyframeinstance, len(keyframeinstance) * settings.F)
				listInstances.append(normalizedInstance)
				label.append(listGesture.index(gestureName))


		clf[i] = clf[i].fit(listInstances, label)

		# saving parameters of the trained model
		joblib.dump(clf[i], "modelClassifier//classifier" + str(i) + ".pkl")
		print"Save MODEL"

	return 1

#load parameter classifier from file
def loadModelLive():

	# Load model from file
	for i in range(0, settings.K):
		clf[i] = joblib.load("modelClassifier//classifier" + str(i) + ".pkl")
		print "LOAD MODEL CLASSIFIER " + str(i)

	# load maxLengthInstance
	maxLengthInstance = [0] * settings.K

	for i in range(0, len(maxLengthInstance)):
		outFile = open("modelClassifier//maxcluster" + str(i) + ".txt", "r")
		maxLengthInstance[i] = int(outFile.readline().split('\n')[0])
		outFile.close()

	return clf,maxLengthInstance

#not used anymore (only used for inital test)
def loadModel(clustersPath, testpath):
	# Load model from file
	for i in range(0, settings.K):
		clf[i] = joblib.load("modelClassifier//classifier" + str(i) + ".pkl")
		print "LOAD MODEL CLASSIFIER " + str(i)

	# load maxLengthInstance
	maxLengthInstance = [0] * settings.K

	for i in range(0, len(maxLengthInstance)):
		outFile = open("modelClassifier//maxcluster" + str(i) + ".txt", "r")
		maxLengthInstance[i] = int(outFile.readline().split('\n')[0])
		outFile.close()

	print "maxcluster"
	print maxLengthInstance

	print "******************************TEST*****************************"


	numcluster = 1
	clusters = readCluster(clustersPath)

	# open file to save result
	outFile = open("result//clusternTRAINING0" + str(numcluster) + ".txt", "a")

	for iter in range(0, 10):

		specificy=0
		tot_istance=0

		# creating confusion matrix
		confusionMtrx = [[0 for x in range(0, 10)] for x in range(0, 10)]

		predictedVal = [0] * settings.K
		for n in range(0, settings.K):
			predictedVal[n] = []

		for gest in clusters[numcluster]:
			num_instance = 0
			countRec = 0
			print "TRY RECOGNIZE GESTURE " + gest
			instanceList = os.listdir(testpath + "/" + gest + "/")
			# instanceList.remove('.DS_Store')
			#instanceList.remove('._.DS_Store')

			# get row for confusion matrix
			rowCM = listGesture.index(gest)

			"""print "" +str(len(instanceList))

			for inst in instanceList:
				if('._' in inst):
					print "---->>>"+inst
					instanceList.remove(inst)

			print "" +str(len(instanceList))"""

			for tmpinstance in instanceList:
				if ('._' in tmpinstance):
					# instanceList.remove(tmpinstance)
					continue

				tot_istance=tot_istance+1
				num_instance = num_instance + 1
				testinstance = dataset.getInstanceDataList(testpath + "/" + gest + "/" + tmpinstance)
				print "len" + str(len(testinstance))

				rate=float(maxLengthInstance[numcluster]/len(testinstance))
				"""if(rate<1,50):
					instancepadded = addPaddingEndInstance(testinstance, maxLengthInstance[numcluster] - len(testinstance))
				else:
					instancepadded = repeatPadding(testinstance, maxLengthInstance[numcluster] - len(testinstance))"""
				#instancepadded = repeatPaddingReverse(testinstance, maxLengthInstance[numcluster] - len(testinstance))
				#print "len" + str(len(testinstance))
				#normalizedInstance = np.reshape(instancepadded, len(instancepadded) * settings.F)

				#keyframe
				keyframeinstance=extractKeyFrame(testinstance)
				print "len" + str(len(keyframeinstance))

				#nel caso training con keyframe
				if(maxLengthInstance[i]>len(keyframeinstance)):
					instancepadded = repeatPaddingReverse(keyframeinstance, maxLengthInstance[numcluster] - len(keyframeinstance))


					normalizedInstance = np.reshape(instancepadded, len(instancepadded) * settings.F)
				#<<<<

					index = clf[numcluster].predict(normalizedInstance)
					#calcolate probability for each gesture
					#array=clf[numcluster].predict_proba(normalizedInstance)
					#print array
					print "INDEX " + str(index) + "--> " + listGesture[index]
					confusionMtrx[rowCM][index] += 1
					if (listGesture[index] == gest):
						countRec += 1
						#calcolo specificy
						specificy=specificy+1





			nrec = num_instance - countRec
			print "rec " + str(countRec)
			print "nonrec " + str(nrec)

			percent = (float(float(countRec) / float(num_instance))) * 100
			print "percent " + str(percent)
			predictedVal[numcluster].append(percent)

		print "predicted value"
		print predictedVal

		outFile.write(str(predictedVal[numcluster]) + "\n")

		specificy = (float(float(specificy) / float(tot_istance)))
		print "SPECIFICY " + str(specificy)
		outFile.write("\nSPECIFICY =" +str(specificy) + "\n")

		# printing confusion matrix
		print "Confusion Matrix"
		for row in confusionMtrx:
			print row
			outFile.write("\n"+str(row))
		print "\n"
		outFile.write("\n\n")

	outFile.close()

	""" test per riconoscimento singolo gesto
	gesture=testpath.split('/')[-2]
	print "TRY RECOGNIZE GESTURE "+gesture
	countRec=0
	instanceList = os.listdir(testpath+ "/")
	instanceList.remove('.DS_Store')
	instanceList.remove('._.DS_Store')
	for inst in instanceList:
		if('._' in inst):
			instanceList.remove(inst)
			
	for tmpinstance in instanceList:
		testinstance = dataset.getInstanceDataList(testpath +"/" +tmpinstance)
		print "len" +str(len(testinstance))
		instancepadded=addPaddingEndInstance(testinstance,maxLengthInstance[numcluster]-len(testinstance))
		print "len" +str(len(testinstance))
		normalizedInstance=np.reshape(instancepadded,len(instancepadded)*settings.F)
	
		index=clf[numcluster].predict(normalizedInstance)
		print "INDEX "+ str(index) +"--> "+ listGesture[index]
		if(listGesture[index]==gesture):
			countRec+=1
	
	
	
	
	
	nrec=len(instanceList)-countRec
	print "rec " + str(countRec)
	print "nonrec "+ str(nrec)
	
	percent=(float(float(countRec)/float(len(instanceList))))*100
	print "percent " +str(percent)
	"""

	return

#not used
def loadModelSingleGesture(clustersPath, testpath):
	# Load model from file

	numcluster = 1
	clusters = readCluster(clustersPath)

	num_gesture=0

	for gest in clusters[numcluster]:
		clf[num_gesture] = joblib.load("modelSingleClassifier//" +gest + ".pkl")
		num_gesture=num_gesture+1
		print "LOAD MODEL CLASSIFIER " + gest


	print clf
	# load maxLengthInstance
	maxLengthInstance = [0] * settings.K

	for i in range(0, len(maxLengthInstance)):
		outFile = open("modelClassifier//maxcluster" + str(i) + ".txt", "r")
		maxLengthInstance[i] = int(outFile.readline().split('\n')[0])
		outFile.close()

	print "maxcluster"
	print maxLengthInstance

	print "******************************TEST*****************************"
	"""nelle prove cambiare il clf[i] maxlenth[] list gesture[]"""


	# open file to save result
	outFile = open("result//gesture" + str(numcluster) + ".txt", "a")

	for iter in range(0, 1):

		predictedVal = [0] * 10
		for n in range(0, 10):
			predictedVal[n] = []

		num_gesture=0

		for gest in clusters[numcluster]:
			num_instance = 0
			countRec = 0
			print "TRY RECOGNIZE GESTURE " + gest
			instanceList = os.listdir(testpath + "/" + gest + "/")
			# instanceList.remove('.DS_Store')
			instanceList.remove('._.DS_Store')


			for tmpinstance in instanceList:
				if ('._' in tmpinstance):
					# instanceList.remove(tmpinstance)
					continue
				num_instance = num_instance + 1
				testinstance = dataset.getInstanceDataList(testpath + "/" + gest + "/" + tmpinstance)
				print "len" + str(len(testinstance))

				instancepadded = addPaddingEndInstance(testinstance, maxLengthInstance[numcluster] - len(testinstance))

				#instancepadded = repeatPadding(testinstance, maxLengthInstance[numcluster] - len(testinstance))
				print "len" + str(len(testinstance))
				normalizedInstance = np.reshape(instancepadded, len(instancepadded) * settings.F)

				for pred in range(0,len(clf)):
					#array=clf[pred].predict_proba(normalizedInstance)
					array=clf[pred].predict_log_proba(normalizedInstance)
					print array[0][0]
					print "%.2f" % (array[0][0])

				#print "INDEX " + str(index) + "--> " + listGesture[index]
				#if (listGesture[index] == gest):
				 #   countRec += 1

			nrec = num_instance - countRec
			print "rec " + str(countRec)
			print "nonrec " + str(nrec)

			percent = (float(float(countRec) / float(num_instance))) * 100
			print "percent " + str(percent)
			predictedVal[numcluster].append(percent)

			num_gesture= num_gesture+1

		print "predicted value"
		print predictedVal

		outFile.write(str(predictedVal[numcluster]) + "\n")

	outFile.close()

	return

#return an instance with key frame extracted
def extractKeyFrame(instance):

	keyFeatureInstances =[]

	conta=0
	index=0
	for k in range(1,len(instance)):
		sad=0
		#print "index >> "+ str(index)
		for i in range(0,len(instance[k])):
			#SAD= sad + | |x1| - |x2| |
			sad=sad+abs( abs(float(instance[index][i]))-abs(float(instance[k][i])))
		#print "SADFINE"+ str(sad)
		#default value 4
		if(sad>=4):
			index=k
			conta=conta+1
			keyFeatureInstances.append(instance[k])

	#print "conta"+ str(conta)

	#print "len >>"+str(len(keyFeatureInstances))

	return keyFeatureInstances


def training(datasetPath, trainingPath):
	datasetG = []

	#maxLengthInstance = getMaxLengthCluster(datasetPath)

	maxLengthInstance=getMaxKeyFrameLengthCluster(datasetPath,clustersPath)

	print "maxcluster"
	print maxLengthInstance

	# saving length instance on files for each cluster
	for i in range(0, len(maxLengthInstance)):
		outFile = open("modelClassifier//maxcluster" + str(i) + ".txt", "w")
		outFile.write(str(maxLengthInstance[i]) + "\n")
		outFile.close()

	trainClassifier(trainingPath, maxLengthInstance)


	return datasetG


if __name__ == "__main__":

	# Usage: python classesClassifier <datasetPath> <trainingdatasetPath> <clustersPath>

	if len(sys.argv) != 4:
		print "Missing parameters. Usage: python classeslassifier <datasetPath> <trainingdatasetPath> <clustersPath> "
		exit()

	datasetPath = sys.argv[1]
	trainingPath = sys.argv[2]
	clustersPath = sys.argv[3]

	listGesture=getGestureName(datasetPath)
	# getting the dataset
	datasetG = training(datasetPath, trainingPath)


