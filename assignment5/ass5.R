rm(list = ls())
library(ggplot2) 
library(rpart)

setwd("~/git/IntroductionToDataScience/assignment5")

D = read.csv(file="seaflow_21min.csv")
#Step 1
#Q1 18146
summary(D$pop)
#Q2 39180
summary(D$fsc_small)

#Step 2
#Create training and testing data samples
index <- 1:nrow(D)
trainindex <- sample(index, trunc(length(index)/2))
trainset <- D[trainindex, ]
testset <- D[-trainindex, ]
#Q3 342
summary(trainset$time)

#Step 3
#Q4 nano pico
qplot(D$pe,D$chl_small,color = D$pop, xlab = "fluerescense", ylab = "small wavelength")

#Step 4Constructing a binary tree.

fol <- formula(pop ~ fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small)
model <- rpart(fol, method = "class", data = trainset)
print(model)
#Q5 crypto
#Q6 5004
#Q7. pe and chl_small

#Step 5 Evaluate decision forest
prediction <- predict(model, testset, type = "class")
correct <- testset$pop == prediction
score = sum(correct)/length(correct)
#Q8 0.856


#Step 6 Build and evaluate random forest
library(randomForest)
forestmodel <- randomForest(fol, data=trainset)
print(forestmodel)

forestprediction <- predict(forestmodel, testset, type = "class")
forestcorrect <- testset$pop == forestprediction
forestscore = sum(forestcorrect)/length(forestcorrect)

#Q9 0.92

importance(forestmodel)
#Q10 pe, chl_small, chl_big

#Step 7: Train a support vector machine model and compare results.
library(e1071)
svmmodel <- svm(fol, data=trainset)

svmprediction <- predict(svmmodel, testset, type = "class")
svmcorrect <- testset$pop == svmprediction
svmscore = sum(svmcorrect)/length(svmcorrect)

#Q11 0.92
#Step 8: Construct confusion matrices
binarytable = table(testset$pop,prediction)
foresttable = table(testset$pop,forestprediction)
svmtable = table(testset$pop,svmprediction)
#Q12 ultra > pico

#Step 8: Sanity check the data

qplot(fsc_big, data=D, geom="histogram",binwidth = 200)
#Q13 fsc_perp?

newD <- subset(D, ! file_id == 208)
newindex <- 1:nrow(newD)
newtrainindex <- sample(newindex, trunc(length(newindex)/2))
newtrain <- newD[newtrainindex, ]
newtest <- newD[-newtrainindex, ]


newsvmmodel <- svm(fol, data=newtrain)
newsvmprediction <- predict(newsvmmodel, newtest, type = "class")
newsvmcorrect <- newtest$pop == newsvmprediction
newsvmscore = sum(newsvmcorrect)/length(newsvmcorrect)
preddiff = newsvmscore - svmscore

#Q14 0.0509