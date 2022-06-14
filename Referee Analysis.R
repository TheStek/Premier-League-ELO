library(tidyverse)

data <- read.csv("Data/Match Data.csv")


liverpool_games = data %>%
  filter(Home == 'Liverpool' | Away == 'Liverpool')


result_mapping <- tibble(
  Result = c(1, 0, -1),
  Result2 = c('W', 'D', 'L')
)



liverpool_results <- 
  union(
  liverpool_games %>%
    filter(Home == 'Liverpool') %>%
    select(Date, Season, Referee, Result),
  
  liverpool_games %>%
    filter(Away == 'Liverpool') %>%
    select(Date, Season, Referee, Result) %>%
    mutate(Result = -1*Result)
  ) %>%
  inner_join(result_mapping, by = "Result")


ggplot(data = liverpool_results)+
  geom_bar(aes(x = Referee, fill = Result2), position = "fill")+
  coord_flip()


ref_stats <- liverpool_results %>% group_by(Referee) %>% summarise(count = n(), overall_decision = sum(Result), average_decision = mean(Result))



data %>% filter(Referee == "Graham Scott", Home == 'Liverpool' | Away == "Liverpool")
