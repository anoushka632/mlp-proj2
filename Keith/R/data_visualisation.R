pacman::p_load(tidyverse, data.table, GGally, lubridate)

dat <- fread("../../hotel.csv", na.strings = c("NULL", "NaN", "NA"))

s1 <- sample(nrow(dat), size = 1000)
p1 <- dat[s1] %>% 
  select_if(is.numeric) %>% 
  select(1:15)

pairs(p1, col= dat[s1]$is_canceled)
ggpairs(p1, aes(colour = factor(p1$is_canceled)))

dat %>% 
  mutate(date = ymd(paste(dat$arrival_date_year, dat$arrival_date_month, dat$arrival_date_day_of_month, sep = "/"))) %>% 
  group_by(arrival_date_month, is_canceled) %>% 
  summarise(n_booking = n(), date = first(date)) %>% 
  ggplot() +
  aes(x = date, y = n_booking, colour = as.factor(is_canceled)) +
  geom_line()

dat %>% 
  mutate(date = ymd(paste(dat$arrival_date_year, dat$arrival_date_month, dat$arrival_date_day_of_month, sep = "/"))) %>% 
  group_by(date, is_canceled) %>% 
  summarise(n_booking = n()) %>% 
  ggplot() +
  aes(x = date, y = n_booking, colour = as.factor(is_canceled)) +
  geom_line() +
  facet_wrap(~year(date),ncol = 1, scales = "free_x")

dat %>% 
  mutate(date = ymd(paste(dat$arrival_date_year, dat$arrival_date_month, dat$arrival_date_day_of_month, sep = "/"))) %>% 
  group_by(date) %>% 
  summarise(.groups = "keep",
            n_booking     = n(), 
            canceled      = sum(is_canceled),
            not_canceled  = n_booking - canceled,
            canceled_diff = not_canceled - canceled,
            weekend       = ifelse(weekdays(date) %in% c("Sunday", "Saturday"), T,F)) %>% 
  ggplot() +
  aes(x = date, y = canceled_diff, colour = weekend) +
  geom_line()


library(mice)

md.pattern(dat,rotate.names = T)
