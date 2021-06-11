def get_channel_stats(selectedChannel, theDB):

    if selectedChannel[0] == "H":
        theCollection = theDB.Homework
    elif selectedChannel[0] == "P":
        theCollection = theDB.Project
    elif selectedChannel[0] == "O":
        theCollection = theDB.OffTopic
    else:
        theCollection = theDB.Quiz

    if not bool(theCollection.find_one({})):   # if the collection is empty
        nConvTopics = 0
        theDocuments = []
        nComments = []
        allCurrentConvTopics = []
    else:
        theDocuments = list(theCollection.find())    # obtaining all the documents in the collection (returning as dict)
        #nConvTopics = len(theDocuments)
        #nComments = 0
        #print(selectedChannel)
        #theCollection = theDB.collection(selectedChannel)

        #nConvTopics = theCollection["convTopics"]
        #nConvTopics = 0

        theDocuments = sorted(theDocuments, key=lambda k: k['convID'])
        allCurrentConvTopics = list(theCollection.distinct("convID"))
        ###allCurrentConvTopics = list(theDocuments.distinct("convTopic"))
        allCurrentConvTopics.sort()
        ###currentConvTopic = ""
        ###nEntries = len(theDocuments)
        nConvTopics = len(allCurrentConvTopics)
        nComments = []
        for myCounter in range(0, nConvTopics):
            mySum = sum([1 for d in theDocuments if allCurrentConvTopics[myCounter] == d.get("convID") ])
            mySum = mySum - 1
            #mySum = len([k for d in theDocuments for k in d.keys() if k == allCurrentConvTopics[myCounter]])
            #print(mySum)
            nComments.append(mySum)

        ###print(nConvTopics)
        #print(allCurrentConvTopics)
        #nConvTopics = 0
        #nComments = 0
        #print(nComments)
        #print(nConvTopics)
        #nComments = [0, 0, 1, 0, 0, 0, 0]
        #print(nComments)
        #print(theDocuments[0]["convTopic"])

    return [theDocuments, allCurrentConvTopics, nConvTopics, nComments]
    

