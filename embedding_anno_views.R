# Embedding/interpretation views

################################################################################
####                                PARAMS                                  ####
################################################################################
FP_IN <- "grading_df_with_distance.csv"
################################################################################

# preconditions ----

# input interface ----
df <- readr::read_csv(FP_IN)
attr(df, "spec") <- NULL

################################################################################
####                                MAIN                                    ####
################################################################################
df %>% 
  group_by(grading_status)

ggplot(df, aes(y = dist_from_norm, x = grading_status)) +
  geom_violin()

# output interface ----