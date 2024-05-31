setwd("C:\\Users\\Elvis Ortega\\OneDrive - Universitat Oberta de Catalunya\\UOC\\PhD_Ortega_E\\systematic_literature_review_artificial_agents_emotion_regulation\\automated_app_reviews\\src")
data <- read.csv(file.choose())

## MAKE SURE TO ADD 1 TO THE ROW NUMBER IF EDITING IN EXCEL

print("Checking Titles")
ass_vector <- data$title

for (av_index in 1:length(ass_vector)) {
  
  tmp_variable <- ass_vector[av_index]
  
  if (grepl("[\\p{Cyrillic}]", tmp_variable, perl = T)){
    print(paste("Cyrillic found @ row ", av_index))
  }
  
  if (grepl("[\\p{Han}]", tmp_variable, perl = T)){
    print(paste("Chinese characters found @ row ", av_index))
  }
  
  if (grepl("[\\p{Hiragana}]", tmp_variable, perl = T)){
    print(paste("Hiragana characters found @ row ", av_index))
  }
  
  if (grepl("[\\p{Katakana}]", tmp_variable, perl = T)){
    print(paste("Katakana characters found @ row ", av_index))
  }
  
  if (grepl("[\\p{Hangul}]", tmp_variable, perl = T)){
    print(paste("Korean characters found @ row ", av_index))
  }
  
}
  

print("Checking Abstracts")
ass_vector <- data$abstract

for (av_index in 1:length(ass_vector)) {
  
  tmp_variable <- ass_vector[av_index]
  
  if (grepl("[\\p{Cyrillic}]", tmp_variable, perl = T)){
    print(paste("Cyrillic found @ row ", av_index))
  }
  
  if (grepl("[\\p{Han}]", tmp_variable, perl = T)){
    print(paste("Chinese characters found @ row ", av_index))
  }
  
  if (grepl("[\\p{Hiragana}]", tmp_variable, perl = T)){
    print(paste("Hiragana characters found @ row ", av_index))
  }
  
  if (grepl("[\\p{Katakana}]", tmp_variable, perl = T)){
    print(paste("Katakana characters found @ row ", av_index))
  }
  
  if (grepl("[\\p{Hangul}]", tmp_variable, perl = T)){
    print(paste("Korean characters found @ row ", av_index))
  }
}


