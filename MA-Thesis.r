#install mixed effects models
install.packages("lme4")
library(lme4)
library(ggplot2)
----------------------------SET UP DATA FRAMES---------------------------------------

#read in data
full_data=read.csv('/Users/akshayasuresh/Documents/UChicago--MA/Lab/score_plus_demos.csv')
#check for missing data (demographic info for several rows ~42)
which(!complete.cases(full_data))
#inspect data
View(full_data)

#create binary race variable due to small sample sizes for some races
full_data$race_binary <- ifelse(full_data$Race == "Af Am", c("Af Am"), c("Other"))
#create threeway race variable
full_data$race_triad <- 0
full_data$race_triad[full_data$Race == "Af Am"] <- "Af Am"
full_data$race_triad[full_data$Race == "White"] <- "White"
full_data$race_triad[full_data$Race == "white"] <- "White"
full_data$race_triad[full_data$race_triad == 0] <- "Other"
#clean up Prior Schooling variable
full_data$Prior.Schooling[full_data$Prior.Schooling == "N "] <- "N"
full_data$Prior.Schooling <- droplevels(full_data)$Prior.Schooling

#calculate date at test column
full_data$Birthdate <- as.Date(full_data$Birthdate, format = "%m/%d/%y")
full_data$date_at_test <- full_data$Birthdate + (full_data$Age*365.25)

#check for common support 
table(full_data$race_triad, full_data$X.Free.Reduced.lunch)

#add in variable for log of age
full_data$log_age <- log(full_data$Age)
full_data$square_age <- full_data$Age**2


#create subset of data for only the Operations skill scores (Will need to repeat for all other skills as well)
operations_data <- full_data[ which(full_data$SkillOrd == 1), ]
comparing_sets_data <- full_data[ which(full_data$SkillOrd == 2), ]
counting_data <- full_data[ which(full_data$SkillOrd == 3), ]
number_id_data <- full_data[ which(full_data$SkillOrd == 4), ]
cardinality_data <- full_data[ which(full_data$SkillOrd == 5), ]
math_vocab_data <- full_data[ which(full_data$SkillOrd == 6), ]
shape_comp_data <- full_data[ which(full_data$SkillOrd == 7), ]
mental_rotation_data <- full_data[ which(full_data$SkillOrd == 8), ]
pattern_data <- full_data[ which(full_data$SkillOrd == 9), ]
spatial_data <- full_data[ which(full_data$SkillOrd == 10), ]
shape_feat_data <- full_data[ which(full_data$SkillOrd == 11), ]
shape_know_data <- full_data[ which(full_data$SkillOrd == 12), ]

View(operations_data)
table(operations_data$race_triad)

-------------------------------VISUALIZE DATA---------------------------------------
#try to visualize differences in data
#differences by race, not so much by gender
boxplot(Proficiency ~ race_binary, col=c("white","lightgray"),full_data)
boxplot(Proficiency ~ race_triad, col=c("white","lightgray"),full_data)
boxplot(Proficiency ~ Gender, col=c("white","lightgray"),full_data)

#differences by gender by Skill
boxplot(Proficiency ~ Gender, col=c("white","lightgray"),operations_data)
t.test(operations_data$Proficiency[operations_data$Gender == 'F'],operations_data$Proficiency[operations_data$Gender == 'M'])
   #repeat for all skills

#differences by race by Skill
boxplot(Proficiency ~ race_triad, col=c("white","lightgray"),operations_data)
t.test(operations_data$Proficiency[operations_data$race_triad == 'Af Am'],operations_data$Proficiency[operations_data$race_triad == 'White']) 

#loop over all skills
skillsList <- list(operations_data, cardinality_data, comparing_sets_data, counting_data,
					math_vocab_data, mental_rotation_data, number_id_data, pattern_data,
					shape_comp_data, shape_feat_data, shape_know_data, spatial_data)
output <- vector()
lapply(skillsList, function(x) {
	ttest <- t.test(x$Proficiency[x$race_triad == 'Af Am' & x$Prior.Schooling== "Y"],x$Proficiency[x$race_triad == 'White' & x$Prior.Schooling== "Y"])
	output <- c(output, ttest$statistic, ttest$p.value, ttest$estimate)
})
print(output)

#interaction of race and gender, bigger differences in race, still not so much by gender
boxplot(Proficiency ~ race_binary*Gender, col=c("white","lightgray"),operations_data)
boxplot(Proficiency ~ race_triad*Gender, col=c("white","lightgray"),operations_data)

#scatter plot by race
color <- as.factor(operations_data$race_triad)
plot(operations_data$Age, operations_data$Proficiency, pch=19, col=color)
points(operations_data$Age, fitted(model_op), col='Blue')

#exploring Prior Schooling variable
#good variation by race, income, gender, and age by prior schooling

##Include this data as a balance table in the paper

table(full_data$Prior.Schooling, full_data$race_triad)
table(full_data$Prior.Schooling, full_data$X.Free.Reduced.lunch)
table(full_data$Prior.Schooling, round(full_data$Age,0))
table(full_data$Prior.Schooling, full_data$Gender)
table(full_data$School.ID, full_data$Prior.Schooling)

---------------------------------CREATE MODELS---------------------------------------

#initial model with full Race variable and three levels (skill, teacher, school)
#no variance explained by Skill Level-- I think I did this incorrectly
model = lmer(Proficiency ~ Age + Gender + Race + Prior.Schooling + (1|SkillOrd) + (1|Teacher.ID) + (1|School.ID), data=full_data)
summary(model)

#model with binary race variable and three levels
model = lmer(Proficiency ~ Age + Gender + race_binary + Prior.Schooling + (1|SkillOrd) + (1|Teacher.ID) + (1|School.ID), data=full_data)
summary(model)

#model with binary race variable and four levels (individual, skill, teacher, school)
model2 = lmer(Proficiency ~ Age + Gender + race_binary + Prior.Schooling + (1|ID) + (1|SkillOrd) + (1|Teacher.ID) + (1|School.ID), data=full_data)
summary(model2)


#now only need 2 levels (teacher, school), keep the binary race variable
model3 = lmer(Proficiency ~ Age + Gender + race_binary + Prior.Schooling + (1|Teacher.ID) + (1|School.ID), data=operations_data)
summary(model3)

#check residuals to see if assumption of linearity/homoskedasticity holds
plot(fitted(model),residuals(model))
plot(fitted(model2),residuals(model2))
#maybe doesn't hold here? try log of age?
plot(fitted(model3),residuals(model3))

#add in variable for log of age
operations_data$log_age <- log(operations_data$Age)
model4 = lmer(Proficiency ~ Age + log_age + Gender + race_binary + Prior.Schooling + (1|Teacher.ID) + (1|School.ID), data=operations_data)
#log_age seems to be a stronger predictor
summary(model4)
#doesn't seem to be much difference in plot. Still looks like heteroskedasticity.
plot(fitted(model4),residuals(model4))

#use income proxy as a predictor
model_op = lmer(Proficiency ~ Age + square_age + log_age + Gender + race_triad + Prior.Schooling + X.Free.Reduced.lunch + (1|Teacher.ID) + (1|School.ID), data=operations_data)
#school ID becomes unimportant, income is very predictive
summary(model_op)
operations_data$fit <- predict(model_op)

---------------------------------PLOT MODEL RESULTS---------------------------------------

#plot model predictions and trends
ggplot(data = operations_data, mapping = aes(x = Age, y = fit)) + geom_point(mapping = aes(color = race_binary)) + geom_smooth(mapping = aes(color = race_binary), se = FALSE)
operations_data$fit <- predict(model_op)

model_car = lmer(Proficiency ~ Age + square_age + log_age + Gender + race_triad + Prior.Schooling + X.Free.Reduced.lunch + (1|Teacher.ID) + (1|School.ID), data=cardinality_data)
cardinality_data$fit <- predict(model_car)
ggplot(data = cardinality_data, mapping = aes(x = Age, y = fit)) + geom_point(mapping = aes(color = race_triad)) + geom_smooth(mapping = aes(color = race_triad), se = FALSE)

model_cs = lmer(Proficiency ~ Age + square_age + log_age + Gender + race_triad + Prior.Schooling + X.Free.Reduced.lunch + (1|Teacher.ID) + (1|School.ID), data=comparing_sets_data)
comparing_sets_data$fit <- predict(model_cs)
ggplot(data = comparing_sets_data, mapping = aes(x = Age, y = fit)) + geom_point(mapping = aes(color = race_triad)) + geom_smooth(mapping = aes(color = race_triad), se = FALSE)

#P-values
coefs <- data.frame(coef(summary(model_cs)))
coefs$p.z <- 2 * (1 - pnorm(abs(coefs$t.value)))
coefs

savehistory("~/Documents/UChicago--MA/Lab/Analysis.Rhistory")
