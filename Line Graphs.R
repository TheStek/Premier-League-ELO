library(tidyverse)

data <- read.csv("Data/Team Histories.csv")


ggplot(data = data %>% filter(Team == 'Manchester Utd'))+
  geom_line(aes(x = Date, y = New.Elo, group = Team, colour = Team))


ggplot(data = data %>% filter(Date == '2022-05-22'))+
  geom_bar(aes(x = reorder(Team, New.Elo), y = New.Elo, fill = Team), stat = 'identity')+
  coord_flip()
