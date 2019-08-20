setwd("/Users/swkim728/Desktop/wesleyan/spring_2019/QAC305")
## PACKAGES
library(readr)
library(dplyr)
library(factorAnalysis)
library(factoextra)
library(tidyr)
library(ggplot2)
library(plotly)
library(ggridges)
library(Hmisc)
## Reading in data
fifa = read_csv("fifa19.csv")

## Summary statistics
summary(fifa)

## Condensing positions and subsetting data
positions = as.factor(fifa$Position)
PlayArea = list(GK = c("GK"),
                DF = c("LWB", "LB", "LCB", "CB", "RCB", "RB", "RWB"),
                MF = c("LM", "LAM", "LDM", "LCM", "CDM", "CM","CAM", "RCM", "RDM", "RAM", "RM"),
                FW = c("LW", "LF", "LS", "CF", "ST", "RS", "RF", "RW"))
GenPosition = list(GK = c("GK"),
                   FB = c("LWB", "LB", "RB", "RWB"),
                   CB = c("LCB", "CB", "RCB"),
                   DM = c("LDM", "CDM", "RDM"),
                   CM = c("LCM", "CM","RCM"),
                   AM = c("LAM", "CAM", "RAM"),
                   WI = c("LM", "LW", "LF", "RF", "RW", "RM"),
                   FW = c("LS", "CF", "ST", "RS"))

levels(positions) = GenPosition

fifa = fifa %>% mutate(Position = positions) %>% filter(!is.na(Position) & !is.na(Wage) & !is.na(Value))

fifa_analysis = fifa %>% filter(Overall >= 75) %>% filter(Position != "GK")
fifa_analysis = fifa_analysis %>% select(ID:Age, Nationality, Position, Overall:Club, 
                                         Value, Wage, `Weak Foot`, `Skill Moves`, Height:Weight, 
                                         Crossing:SlidingTackle)
fifa_abilities = fifa_analysis %>% select(Crossing:SlidingTackle)

## Univariate Exploration and Visualization
ggplot(fifa_analysis) + 
  geom_histogram(aes(x = Overall), fill = "cornflowerblue", color = "white", binwidth = 1) +
  ggtitle("Distribution of Overall Scores") +
  theme_minimal() +
  theme(legend.position = "none")

ggplot(fifa_analysis) +
  geom_bar(aes(x=Position, fill = Position),
           color = "white", alpha = 0.7) +
  labs(title = "Distribution of Positions (Condensed)", x = "Position") +
  theme_minimal() +
  theme(legend.position = "none")

## CLUSTER ANALYSIS
# Scree plot - how many clusters?
fifa_st = scale(fifa_abilities)
fviz_nbclust(fifa_st, FUN = kmeans, method = "wss")

# Fitting data
set.seed(1234)
fit.km = kmeans(fifa_st, 5, nstart = 25)
fit.km$size
fit.km$center

# Adding clusters to dataset
fifa_analysis$Cluster = fit.km$cluster


## FACTOR ANALYSIS
# How many factors?
screePlot(fifa_abilities, method = "pa")

# Fitting the data using factor analysis
set.seed(1234)
fit.fa <- FA(fifa_abilities, fm="pa", rotate = "varimax", nfactors = 5)

# Adding factors to datset
fifa_analysis = score(fifa_analysis, fit.fa)


## CLUSTERING AFTER FACTOR ANALYSIS
fviz_nbclust(fifa_analysis[45:49], FUN = kmeans, method = "wss")

set.seed(1234)
fit.kmFA = kmeans(fifa_analysis[45:49], 5, nstart = 25)
fit.kmFA$size
fit.kmFA$center


## CLUSTER ANALYSIS RESULTS
# Plot cluster profiles
means = as.data.frame(fit.km$centers)
means$cluster = row.names(means)
dfm = gather(means, key = "variable", value = "value", Crossing:SlidingTackle)
ggplot(data = dfm, 
       aes(x = variable, y = value, group = cluster, color = cluster, shape = cluster)) +
  geom_point(size = 3) +
  geom_line(size = 1) +
  labs(title = "FIFA Profiles for Clusters")+
  theme(axis.text.x = element_text(angle = 35, hjust = 1))

# Cluster Graph
ggplot(data = dfm %>% filter(cluster == 1), 
       aes(x = variable, y = value, group = cluster, color = cluster, shape = cluster)) +
  geom_point(size = 3) +
  geom_line(size = 1) +
  labs(title = "Cluster 1 Profile") +
  theme(axis.text.x = element_text(angle = 35, hjust = 1))

# Who are top 5 players in this cluster?
fifa_analysis %>% filter(Cluster == 1) %>% 
  select(Name, Position, Club, 
         Marking, SlidingTackle, StandingTackle, Strength,
         Positioning, Dribbling, LongShots, Vision) %>% 
  head() # No-nonsense defenders

ggplot(data = fifa_analysis %>% filter(Cluster == 1)) +
  geom_bar(aes(x=Position, fill = Position),
           color = "white", alpha = 0.7) +
  labs(title = "Distribution of Positions (Limited Defenders)", x = "Position") +
  theme_minimal() +
  theme(legend.position = "none")

# Cluster Graph
ggplot(data = dfm %>% filter(cluster == 2), 
       aes(x = variable, y = value, group = cluster, color = cluster, shape = cluster)) +
  geom_point(size = 3) +
  geom_line(size = 1) +
  labs(title = "Cluster 2 Profile") +
  theme(axis.text.x = element_text(angle = 35, hjust = 1))

# Who are top 5 players in this cluster?
fifa_analysis %>% filter(Cluster == 2) %>% 
  select(Name, Position, Club,
         Marking, SlidingTackle, StandingTackle, Interceptions,
         Finishing, Penalties, Volleys) %>% 
  head() # No-nonsense defenders

ggplot(data = fifa_analysis %>% filter(Cluster == 2)) +
  geom_bar(aes(x=Position, fill = Position),
           color = "white", alpha = 0.7) +
  labs(title = "Distribution of Positions (Ball Playing Defenders)", x = "Position") +
  theme_minimal() +
  theme(legend.position = "none")

# Cluster Graph
ggplot(data = dfm %>% filter(cluster == 3), 
       aes(x = variable, y = value, group = cluster, color = cluster, shape = cluster)) +
  geom_point(size = 3) +
  geom_line(size = 1) +
  labs(title = "Cluster 3 Profile") +
  theme(axis.text.x = element_text(angle = 35, hjust = 1))

# Who are top 5 players in this cluster?
fifa_analysis %>% filter(Cluster == 3) %>% 
  select(Name, Position, Club,
         LongPassing, ShortPassing, Vision,
         HeadingAccuracy, Jumping, SprintSpeed, Strength) %>% 
  head() # No-nonsense defenders

ggplot(data = fifa_analysis %>% filter(Cluster == 3)) +
  geom_bar(aes(x=Position, fill = Position),
           color = "white", alpha = 0.7) +
  labs(title = "Distribution of Positions (Passerss)", x = "Position") +
  theme_minimal() +
  theme(legend.position = "none")

# Cluster Graph
ggplot(data = dfm %>% filter(cluster == 4), 
       aes(x = variable, y = value, group = cluster, color = cluster, shape = cluster)) +
  geom_point(size = 3) +
  geom_line(size = 1) +
  labs(title = "Cluster 4 Profile") +
  theme(axis.text.x = element_text(angle = 35, hjust = 1))

# Who are top 5 players in this cluster?
fifa_analysis %>% filter(Cluster == 4) %>% 
  select(Name, Position, Club,
         Acceleration, Agility, Dribbling, SprintSpeed,
         Aggression, Strength, StandingTackle, Interceptions) %>% 
  head() # No-nonsense defenders

ggplot(data = fifa_analysis %>% filter(Cluster == 4)) +
  geom_bar(aes(x=Position, fill = Position),
           color = "white", alpha = 0.7) +
  labs(title = "Distribution of Positions (Dribblers)", x = "Position") +
  theme_minimal() +
  theme(legend.position = "none")

# Cluster Graph
ggplot(data = dfm %>% filter(cluster == 5), 
       aes(x = variable, y = value, group = cluster, color = cluster, shape = cluster)) +
  geom_point(size = 3) +
  geom_line(size = 1) +
  labs(title = "Cluster 5 Profile") +
  theme(axis.text.x = element_text(angle = 35, hjust = 1))

# Who are top 5 players in this cluster?
fifa_analysis %>% filter(Cluster == 5) %>% 
  select(Name, Position, Club,
         Positioning, Finishing, Penalties, Volleys,
         Interceptions, LongPassing, StandingTackle, SlidingTackle) %>% 
  head() # No-nonsense defenders

ggplot(data = fifa_analysis %>% filter(Cluster == 5)) +
  geom_bar(aes(x=Position, fill = Position),
           color = "white", alpha = 0.7) +
  labs(title = "Distribution of Positions (Finishers)", x = "Position") +
  theme_minimal() +
  theme(legend.position = "none")


## FACTOR ANALYSIS RESULTS
# Plotting the data
plot(fit.fa, type = "bar")

# Naming factors in dataset
names(fifa_analysis)[45:49] = c("KICKING", "DEFENSE", "SPEED", "STRENGTH", "COMPOSURE")


# Which clusters are strong in which factors?
clusters_by_factors = fifa_analysis %>%
  group_by(Cluster) %>%
  summarise(avgKICKING = mean(KICKING),
            avgDEFENSE = mean(DEFENSE),
            avgSPEED = mean(SPEED),
            avgSTRENGTH = mean(STRENGTH) * -1,
            avgCOMPOSURE = mean(COMPOSURE))
clusters_by_factors


## CLUSTER ANALYSIS AFTER FACTOR ANALYSIS RESULTS
set.seed(1234)
fit.kmFA = kmeans(fifa_analysis[45:49], 5, nstart = 25)
fit.kmFA$size
fit.kmFA$center

# Plot cluster profiles
meansFA = as.data.frame(fit.kmFA$centers)
meansFA$cluster = row.names(meansFA)
dfmFA = gather(meansFA, key = "variable", value = "value", KICKING:COMPOSURE)
pFA = ggplot(data = dfmFA, 
             aes(x = variable, y = value, group = cluster, color = cluster, shape = cluster)) +
  geom_point(size = 3) +
  geom_line(size = 1) +
  labs(title = "FIFA Profiles for Clusters after Factor Analysis")
ggplotly(pFA)


# Adding cluster profiles to dataset
fifa_analysis$FACluster = fit.kmFA$cluster
# Two way table of cluster and FAcluster
with(fifa_analysis, table(Cluster, FACluster))

save(fifa_analysis, file = "fifa_finalclean.Rdata")
