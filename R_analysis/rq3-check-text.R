all_hacks <- read.csv("../dataset/all_hackathons_cleaned.csv", 
                         encoding = "UTF-8" ,
                         stringsAsFactors = FALSE,
                         na.strings=c("","NA"))

summary(all_hacks$num_participants)

plot(density(log(all_hacks$num_participants + 1)))

all_hacks$total_prize_value <- ifelse(isna(all_hacks$total_prize_value), 0)
all_hacks$total_prize_value[is.na(all_hacks$total_prize_value)] <- 0

prize_usd <- all_hacks[all_hacks$total_prize_currency == "$"]


plot(density(log(all_hacks$total_prize_value + 1)))


summary(as.factor(all_hacks$total_prize_currency))


num_submissions_df <- read.csv("../dataset/all_hackathons_numsub.csv", 
                                encoding = "UTF-8" ,
                                stringsAsFactors = FALSE,
                                na.strings=c("","NA"))
plot(density(log(num_submissions_df$num_submission + 1)))

plot(density(num_submissions_df$num_submission))

summary(num_submissions_df$num_submission)
