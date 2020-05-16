# Preproc annotations

################################################################################
####                                PARAMS                                  ####
################################################################################
FP_IN_SAM <- "grading_test_set_annotated.csv"  # annotation file provided by Sam (preprocessed)
FP_IN_RAW <- "notebooks/all_annos.csv"
################################################################################

# preconditions ----

# input interface ----
df <- readr::read_csv(FP_IN_SAM)
attr(df, "spec") <- NULL

raw_df <- readr::read_csv(FP_IN_RAW)
raw_df$dataset_version <- NULL


################################################################################
####                                MAIN                                    ####
################################################################################

# Filter raw data to just the 100 colon grade annotations

# there's no date in Sam's curated data.frame, so I'll have to find a cutoff just in the raw data
ggplot(raw_df, aes(x = createdAt)) +
  geom_histogram()

raw_df %<>% 
  filter(user_email == "yingchun.lo.5@gmail.com") %>% 
  filter(createdAt > as.POSIXct("2020-04-01 00:00:00"))
raw_df$user_email <- NULL
# yields 102 samples; expected 100

# investigate dups
raw_df$file_name %>% compose(length, unique)()
dupd_fns <- raw_df$file_name[raw_df$file_name %>% duplicated()]

raw_df %>% 
  filter(file_name %in% dupd_fns)

raw_df %<>% 
  filter(`_id` != "5e9bb00e537048485d8187f0") %>% 
  filter(`_id` != "5e9bac258ea0d1d5c08187cd")

# tidy
raw_df$`_id` <- NULL
attr(raw_df, "problems") <- NULL
attr(raw_df, "spec") <- NULL
raw_df %<>% select(aws_wsi_fp = file_name, anno_date = createdAt, apical_status, text_comments)

# label frequency distribution
raw_df %>% 
  Tally(by = "apical_status") %>% 
  knitr::kable(format = "html")

# consolidate free text
raw_df$text_comments %>% table_()
raw_df %<>% 
  mutate(is_tumor_tiny = !is.na(text_comments))

raw_df %>% 
  filter(is_tumor_tiny) %>% 
  Tally(by = "apical_status") %>% 
  knitr::kable(format = "html")

# output interface
readr::write_csv(raw_df, path = "crc_stage_annos.csv")
