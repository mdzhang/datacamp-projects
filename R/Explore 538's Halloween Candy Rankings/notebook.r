
# Load all the packages we need
library(tidyverse)
library(broom)
library(corrplot)
library(fivethirtyeight)

# Load the candy_rankings dataset from the fivethirtyeight package
data(candy_rankings)

# Take a glimpse() at the dataset
glimpse(candy_rankings)

glimpse_result <- .Last.value


# These packages need to be loaded in the first @tests cell. 
library(testthat) 
library(IRkernel.testthat)

# Then follows one or more tests of the student's code. 
# The @solution should pass the tests.
# The purpose of the tests is to try to catch common errors and to 
# give the student a hint on how to resolve these errors.


run_tests({
    test_that("Packages are loaded.", {
        expect_true("tidyverse" %in% .packages(),
                   info = "Make sure you loaded `tidyverse`.")
        expect_true("broom"  %in% .packages(),
                   info = "Make sure you loaded `broom`.")
        expect_true("corrplot" %in% .packages(),
                   info = "Make sure you loaded `corrplot`.")
        expect_true("fivethirtyeight" %in% .packages(),
                   info = "Make sure you loaded `fivethirtyeight`.")
    })
    test_that("Data is loaded.", {
        expect_equal(.GlobalEnv$candy_rankings, fivethirtyeight::candy_rankings,
                        info = "Did you call `data(candy_rankings)`?")
    })
    test_that("`glimpse()` was called", {
        expect_equal(candy_rankings, glimpse_result,
                    info = "Make sure you took a look at `candy_rankings` with `glimpse()`.")
    })
})


# gather() the categorical variables to make them easier to plot
candy_rankings_long <- candy_rankings %>%
    gather("feature", "value", chocolate:pluribus)

# Make a bar plot showing the distribution of each variable
ggplot(candy_rankings_long, aes(x = competitorname)) +
    geom_bar(aes(fill = sugarpercent)) +
    facet_wrap(~feature)

# One or more tests of the student's code. 
# The @solution should pass the tests.
# The purpose of the tests is to try to catch common errors and to 
# give the student a hint on how to resolve these errors.
p <- last_plot()

run_tests({
    test_that("`candy_rankings_long` is correct", {
        expect_equal(candy_rankings_long, gather(candy_rankings, "feature", "value", chocolate:pluribus),
                        info = "Make sure you created `candy_features_long` by `gathering` the correct columns.")
    })
    test_that("The plot was created correctly", {
        expect_equal(p$data, candy_rankings_long,
                        info = "Make sure you passed `candy_rankings` as the `data` argument to `ggplot()`.")
        expect_equal(p$mapping, aes(value),
                    info = "Did you map the `value` column to the `x` aesthetic?")
        expect_equal(p$layers, list(geom_bar()),
                    info = "Did you call `geom_bar()` to create a bar chart?")
        expect_equal(p$facet, facet_wrap(~feature),
                    info = "Did you create facet for each `feature`?")
    })
})

# Make a lollipop chart of pricepercent
# .... YOUR CODE FOR TASK 3 ....

# One or more tests of the student's code. 
# The @solution should pass the tests.
# The purpose of the tests is to try to catch common errors and to 
# give the student a hint on how to resolve these errors.
p <- last_plot()

run_tests({
    test_that("The plot is correct", {
        expect_equal(p$data, candy_rankings,
                    info = "Make sure you passed `candy_rankings` as the `data` argument to `ggplot()`.")
        expect_equal(p$mapping, aes(reorder(competitorname, pricepercent), pricepercent),
                    info = "Did you pass the right aesthetics to `aes()`? Make sure to reorder `competitorname`.")
        expect_equal(p$layers, list(geom_segment(aes(xend = reorder(competitorname, pricepercent), yend = 0)), geom_point()),
                    info = "The aesthetics in `geom_segment()` are not correct. You only need `xend=` and `yend=` Was `xend=` reordered correctly?")
        expect_equal(p$coordinates, coord_flip(),
                    info = "Did you flip the plot with `coord_flip()`?")
    })
    # You can have more than one test
})

# Plot a histogram of winpercent
# .... YOUR CODE FOR TASK 4 ....


p <- last_plot()

run_tests({
    test_that("The histogram is plotted correctly.",{
        expect_equal(p$data, candy_rankings,
                    info = "Make sure you used `candy_rankings` as the `data` argument in your `ggplot()`.")
        expect_equal(p$mapping, aes(winpercent),
                    info = "Make sure you assigned `winpercent` to the `x` aesthetic.")
        expect_equal(p$layers, list(geom_histogram()),
                    info = "Make sure you used `geom_histogram()` to make your plot.")
    })
})

# Make a lollipop chart of winpercent
# .... YOUR CODE FOR TASK 5 ....

p <- last_plot()

run_tests({
    test_that("The plot is correct", {
        expect_equal(p$data, candy_rankings,
                    info = "Make sure you passed `candy_rankings` as the `data` argument to `ggplot()`.")
        expect_equal(p$mapping, aes(reorder(competitorname, winpercent), winpercent),
                    info = "Did you pass the right aesthetics to `aes()`? Make sure to reorder `competitorname`.")
        expect_equal(p$layers, list(geom_segment(aes(xend = reorder(competitorname, winpercent), yend = 0)), geom_point()),
                    info = "The aesthetics in `geom_segment()` are not correct. You only need `xend=` and `yend=` Was `xend=` reordered correctly?")
        expect_equal(p$coordinates, coord_flip(),
                    info = "Did you flip the plot with `coord_flip()`?")
    })
    # You can have more than one test
})

# Plot the correlation matrix using corrplot()
# .... YOUR CODE FOR TASK 6 ....

# One or more tests of the student's code.  
# The @solution should pass the tests.
# The purpose of the tests is to try to catch common errors and to 
# give the student a hint on how to resolve these errors.

student_cor <- .Last.value
good_cor <- candy_rankings %>%
  select(-competitorname) %>% 
  cor()
run_tests({
    test_that("The correlation matrix is created correctly", {
        expect_equal(student_cor, good_cor,
                    info = "Make sure you calculated the correlation matrix correctly.")
    })
    # You can have more than one test
})

# Fit a linear model of winpercent explained by all variables 
# except competitorname
win_mod <- ....

# One or more tests of the student's code. 
# The @solution should pass the tests.
# The purpose of the tests is to try to catch common errors and to 
# give the student a hint on how to resolve these errors.
good_mod <- lm(winpercent ~ . -competitorname, data = candy_rankings)

run_tests({
    test_that("The model is correct.", {
        expect_equal(good_mod$fitted.values, win_mod$fitted.values,
                        info = "Make sure you created the model correctly.")
    })
    # You can have more than one test
})

# Take a look at the summary
# .... YOUR CODE FOR TASK 8 ....

# Plot the residuals vs the fitted values
# .... YOUR CODE FOR TASK 8 ....

# One or more tests of the student's code.
# The @solution should pass the tests.
# The purpose of the tests is to try to catch common errors and to 
# give the student a hint on how to resolve these errors.
p <- last_plot()

run_tests({
    test_that("The plot is correct.", {
        expect_equal(p$data, augment(win_mod),
                    info = "Make sure you called `ggplot()` on the `augment()`-ed `win_mod`.")
        expect_equal(p$mapping, aes(.fitted, .resid),
                    info = "Make sure you mapped `.fitted` to the `x` aesthetic and `.resid` to the `y` aesthetic.")
        expect_equal(p$layers, list(geom_point(), geom_hline(yintercept = 0)),
                    info = "Make sure you used `geom_point()` and `geom_hline()` to make your plot.")
    })
    # You can have more than one test
})

# Fit a glm() of chocolate
choc_mod <- ....

# One or more tests of the student's code. 
# The @solution should pass the tests.
# The purpose of the tests is to try to catch common errors and to 
# give the student a hint on how to resolve these errors.
good_mod <- glm(chocolate ~ . - competitorname, family = "binomial", data = candy_rankings)

run_tests({
    test_that("the model is correct.", {
        expect_equal(good_mod$fitted.values, choc_mod$fitted.values,
                        info = "Make sure you fit your logistic regression correctly.")
    })
    # You can have more than one test
})

# Print the summary
# .... YOUR CODE FOR TASK 10 ....

# Make a dataframe of predictions
preds <- ....

# Create the confusion matrix
conf_mat <- ....

# Calculate the accuracy
accuracy <- ....


run_tests({
    test_that("The predictions are correct.", {
        expect_equal(augment(choc_mod, type.predict = "response") %>% mutate(prediction = .fitted > .5), preds,
                        info = "Make sure you created your predictions correctly.")
    })
    test_that("The confusion matrix is correct.", {
        expect_equivalent(preds %>% select(chocolate, prediction) %>% table(), conf_mat,
                        info = "Make sure you created the cofusion matrix correctly.")
    })
    test_that("The accuracy is correct.", {
        expect_equal(sum(diag(conf_mat))/sum(conf_mat), accuracy,
                        info = "Make sure you calculated the accuracy correctly.")
    })
})
