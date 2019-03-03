#
# 1
#

# Importing the tidyverse library
library(readr)
library(tidyverse)
library(stringr)
library(purrr)

# Loading in datasets/users.csv
data_dir <- "../datasets/"
users <- read_csv(paste0(data_dir, "users.csv"))

# Counting how many users we've got
nrow(users)

# Taking a look at the 12 first users
head(users, 12)

#
# 2
#

# Calculating the lengths of users' passwords
users$length <- nchar(users$password)

# Flagging the users with too short passwords
users$too_short <- users$length < 8

# Counting the number of users with too short passwords
sum(users$too_short)

# Taking a look at the 12 first rows
head(users, 12)

#
# 3
#

# Reading in the top 10000 passwords
common_passwords <- read_csv(
  paste0(data_dir,
         "10_million_password_list_top_10000.txt"),
  col_names = FALSE,
)$X1

# Taking a look at the top 100
head(common_passwords, 100)

#
# 4
#

# Flagging the users with passwords that are common passwords
users$common_password <- users$password %in% common_passwords

# Counting the number of users using common passwords
sum(users$common_password)

# Taking a look at the 12 first rows
head(users, 12)

#
# 5
#

# Reading in a list of the 10000 most common words
words <- read_csv(
  paste0(data_dir, "google-10000-english.txt"),
         col_names = FALSE
)$X1

# Flagging the users with passwords that are common words
users$common_word <- users$password %in% words

# Counting the number of users using common words as passwords
sum(users$common_word)

# Taking a look at the 12 first rows
head(users, 12)

#
# 6
#

# Extracting first and last names into their own columns
names <- as.data.frame(do.call(rbind, str_split(users$user_name, "\\.")))
colnames(names) <- c("first_name", "last_name")

users <- cbind(users, names)

# Flagging the users with passwords that matches their names
users$uses_name <- (
  (users$password == users$first_name) |
  (users$password == users$last_name)
)

# Counting the number of users using names as passwords
sum(users$uses_name)

# Taking a look at the 12 first rows
head(users, 12)

#
# 7
#

# Splitting the passwords into vectors of single characters
split_passwords <- strsplit(users$password, "")

# Picking out the max number of repeat characters for each password
users$max_repeats <- map(split_passwords, function(split_password) {
  max(rle(split_password)$lengths)
})


# Flagging the passwords with >= 4 repeats
users$too_many_repeats <- users$max_repeats >= 4

# Taking a look at the users with too many repeats
sum(users$too_many_repeats)

#
# 8
#

users$bad_password <- (
  users$too_short |
  users$common_password |
  users$common_word |
  users$uses_name |
  users$too_many_repeats
)

sum(users$bad_password)

bad_passwords <- subset(users, bad_password, select = "password")

head(bad_passwords, 100)
