#*****************************************************************************************************************

# Program:

# Analyst: Eliza Blum

# Create Date: 01/23/2025

# Updated by: Eliza Blum

# Description: Cleans strike card data and organizes into region.

# Notes:

#***************************************************************************************************/

# Where it says "## UPDATE" please input correct information!!

 

######################### SET UP #######################

 

### Load common libraries

req_packages <- c("dplyr", "stringr", "tidyr", "tidyverse", "Cairo", "RODBC", "openxlsx","ggplot2","sf","fuzzyjoin","stringdist")

for(package in req_packages){

  # If you do not (!) have a package, install that package

  if(!require(package,character.only = TRUE)) install.packages(package)

  #Now load the package

  library(package,character.only = TRUE)

}

 

rm(req_packages)

 

# today's date

date <- as.character(format(Sys.time(), "%Y%m%d"))

 

############# BRING IN REMOVE DUPLICATES & OPT OUT #####################

 

# Replace 'your_file.csv' with your file's name and path

data_1 <- read.csv("G:/Personal Documents/EXPORTS/20250228/Strike Card 1.csv")%>%

  rename(Name = `Name.`) %>%

  select(Timestamp, Name, Email, Phone.number, Zip.code, Source)

 

data_2 <- read.csv("G:/Personal Documents/EXPORTS/20250228/Strike Card 2.csv") %>%

  rename(Name = `Name.`) %>%

  select(Timestamp, Name, Email, Phone.number, Zip.code, Source)

 

data_3 <- read.csv("G:/Personal Documents/EXPORTS/20250228/Strike Card 3.csv") %>%

  rename(Name = `Name.`) %>%

  select(Timestamp, Name, Email, Phone.number, Zip.code, Source)

 

data_4 <- read.csv("G:/Personal Documents/EXPORTS/20250228/Strike Card 4.csv") %>%

  rename(Name = `Name.`) %>%

  select(Timestamp, Name, Email, Phone.number, Zip.code, Source)

 

##UPDATE THIS ONE WITH DOWNLOADED V3#

data_5<- read.csv("G:/Personal Documents/EXPORTS/20250228/Strike Card 5.csv") %>%

  rename(Zip.code = 'Zip.Code') %>%

  select(Timestamp, Name, Email, Phone.number, Zip.code, Source)

 

 

# Convert Zip.code to integer in all dataframes

data_1 <- data_1 %>% mutate(Zip.code = as.integer(Zip.code))

data_2 <- data_2 %>% mutate(Zip.code = as.integer(Zip.code))

data_3 <- data_3 %>% mutate(Zip.code = as.integer(Zip.code))

data_4 <- data_4 %>% mutate(Zip.code = as.integer(Zip.code))

data_5 <- data_5 %>% mutate(Zip.code = as.integer(Zip.code))

 

# Check which rows contain non-numeric ZIP codes

problematic_zips <- bind_rows(data_1, data_2, data_3, data_4, data_5) %>%

  filter(!grepl("^\\d+$", Zip.code))  # Finds non-numeric values

 

# View problematic ZIP codes

print(problematic_zips)

 

# Combine all dataframes into one

data <- bind_rows(data_1, data_2, data_3, data_4, data_5) %>%

  distinct()  # Remove duplicate rows

 

# List of emails to remove

remove_emails <- c(


)

 

# Remove rows where Email matches any in remove_emails list

data <- data %>%

  filter(!Email %in% remove_emails)

 

# Remove duplicates based on Email and Phone.number or Name and Email

cleaned_data <- data %>%

  distinct(Email, Phone.number, .keep_all = TRUE) %>%

  distinct(Name, Email, .keep_all = TRUE)

 

# Remove all non-numeric characters from Phone.number

cleaned_data <- cleaned_data %>%

  mutate(Phone.number = gsub("[^0-9]", "", Phone.number))

 

################ REMOVE BAD PHONE NUMBERS ####################

 

# Remove rows where Phone.number is "0", empty, NULL, or contains all identical digits

cleaned_data <- cleaned_data %>%

  filter(

    !is.na(Phone.number),         # Exclude NULL values

    Phone.number != "",           # Exclude empty values

    Phone.number != "0",          # Exclude rows where Phone.number is "0"

    !grepl("^([0-9])\\1+$", Phone.number) # Exclude rows with all identical digits

  )

 

################# CLEAN EMAILS ##############################                                  # Get the top 10 most frequent suffixes

 

# Extract domain suffixes from the email column

email_suffixes <- cleaned_data %>%

  mutate(email_suffix = sub(".*@", "", Email)) %>%  # Extract text after @

  count(email_suffix, sort = TRUE) %>%  # Count occurrences

  top_n(50, n)  # Get top 50 most common suffixes

 

# Display results

print(email_suffixes)

 

# Function to correct common email typos

correct_email_typos <- function(email_column) {

  email_column <- gsub("@gnail\\.com$", "@gmail.com", email_column, ignore.case = TRUE)

  email_column <- gsub("@gamil\\.com$", "@gmail.com", email_column, ignore.case = TRUE)

  email_column <- gsub("@hotnail\\.com$", "@hotmail.com", email_column, ignore.case = TRUE)

  email_column <- gsub("@yaho\\.com$", "@yahoo.com", email_column, ignore.case = TRUE)

  email_column <- gsub("@ymial\\.com$", "@ymail.com", email_column, ignore.case = TRUE)

  return(email_column)

}

 

# Apply function to Email column in cleaned_data

cleaned_data <- cleaned_data %>%

  mutate(Email = correct_email_typos(Email))

 

# Correct ".con" to ".com" in the Email column

cleaned_email <- cleaned_data %>%

  mutate(Email = gsub("\\.con$", ".com", Email, ignore.case = TRUE))

 

# Add '@' if missing for specific domains

cleaned_email <- cleaned_email %>%

  mutate(

    Email = ifelse(grepl("^gmail\\.com$", Email, ignore.case = TRUE), paste0("@", Email), Email),

    Email = ifelse(grepl("^yahoo\\.com$", Email, ignore.case = TRUE), paste0("@", Email), Email),

    Email = ifelse(grepl("^aol\\.com$", Email, ignore.case = TRUE), paste0("@", Email), Email),

    Email = ifelse(grepl("^hotmail\\.com$", Email, ignore.case = TRUE), paste0("@", Email), Email),

    Email = ifelse(grepl("^icloud\\.com$", Email, ignore.case = TRUE), paste0("@", Email), Email),

    Email = ifelse(grepl("^outlook\\.com$", Email, ignore.case = TRUE), paste0("@", Email), Email)

  )

 

# Function to check for valid email syntax

is_valid_email <- function(email) {

  str_detect(email, "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$")

}

 

# Separate invalid emails and REMOVE them from cleaned_email immediately

invalid_emails <- cleaned_email %>%

  filter(!is_valid_email(Email) | is.na(Email) | Email == "")

 

cleaned_email <- cleaned_email %>%

  filter(is_valid_email(Email) & !is.na(Email) & Email != "")  # Keep only valid emails

 

# Display invalid emails

print(invalid_emails)

 

# Define list of major email providers

email_providers <- c("gmail", "yahoo", "hotmail", "icloud", "outlook",

                     "aol", "protonmail", "mac", "live", "msn", "me")

 

# Function to clean email domains dynamically (applies only to invalid emails)

clean_email_domains <- function(email) {

  # Convert to lowercase

  email <- tolower(email)

 

  for (provider in email_providers) {

    # Remove any extra characters after "@provider.com"

    email <- str_replace_all(email, paste0("@", provider, "\\..*"), paste0("@", provider, ".com"))

   

    # Fix common typos and variations

    email <- str_replace_all(email, paste0("@", provider, "c$"), paste0("@", provider, ".com"))

    email <- str_replace_all(email, paste0("@", provider, "-com$"), paste0("@", provider, ".com"))

    email <- str_replace_all(email, paste0("@", provider, "$"), paste0("@", provider, ".com"))

    email <- str_replace_all(email, paste0("@", provider, "com$"), paste0("@", provider, ".com"))

    email <- str_replace_all(email, paste0("@", provider, "co$"), paste0("@", provider, ".com"))

  }

 

  return(email)

}

 

# Apply the function only to invalid emails

invalid_emails <- invalid_emails %>%

  mutate(Email = clean_email_domains(Email))

 

# Merge corrected invalid emails back into cleaned_email dataset

cleaned_email <- cleaned_email %>%

  filter(!(Email %in% invalid_emails$Email)) %>%  # Remove old invalid rows

  bind_rows(invalid_emails)  # Add corrected rows back

 

# Re-run the validation to find any emails still invalid after cleaning and REMOVE

final_invalid_emails <- cleaned_email %>%

  filter(!is_valid_email(Email) | is.na(Email) | Email == "")

 

#remove those still bad from cleaned email

cleaned_email <- anti_join(cleaned_email, final_invalid_emails, by = "Email")

 

# Check remaining invalids (should be 0)

remaining_invalid <- cleaned_email %>%

  filter(!is_valid_email(Email) | is.na(Email) | Email == "")

 

cat("Number of invalid emails remaining:", nrow(remaining_invalid), "\n")

 

################## SINGLE PHONE NUMBER ONLY ####################

 

# Create a new dataframe with duplicate phone numbers removed

cleaned_phone <- cleaned_email %>%

  distinct(Phone.number, .keep_all = TRUE)

 

# Remove rows where Phone.number has fewer than 7 digits

cleaned_phone <- cleaned_phone %>%

  filter(nchar(Phone.number) >= 8 & nchar(Phone.number) <= 15)

 

################## FILTER OUT HACKERS BAD DATA ####################

 

# Step 1: Identify rows with multiline data in Name or Email columns

hacker_data <- cleaned_phone %>%

  filter(

    grepl("\\n|\\r", Name) | grepl("\\n|\\r", Email)  # Detect newline or carriage return characters

  )

 

# Step 2: Create a cleaned dataset without multiline data

cleaned_hacker <- cleaned_phone %>%

  filter(

    !grepl("\\n|\\r", Name) & !grepl("\\n|\\r", Email)  # Keep rows where Name and Email are single-line

  )

 

################ OVERALL CLEANING & EXPORT ######################################

 

# Convert Phone.number and Zip.code columns to numeric

cleaned_final <- cleaned_hacker %>%

  mutate(

    Phone.number = as.numeric(Phone.number),

    Zip.code = as.numeric(Zip.code)  # Ensure Zip.code column exists and is numeric

  )

 

# Create an Excel workbook and add the cleaned_final data

wb <- createWorkbook()

 

# Add a worksheet

addWorksheet(wb, "Cleaned Data")

 

# Write data to the worksheet

writeData(wb, "Cleaned Data", cleaned_final, headerStyle = createStyle(textDecoration = "bold"))

 

# Step 3: Format the first row (header row) to be bold and highlighted in light blue

header_style <- createStyle(

  fontColour = "black",

  fontSize = 12,

  halign = "center",

  valign = "center",

  textDecoration = "bold",

  fgFill = "#DDEBF7"  # Lightest blue

)

 

# Apply the style to the first row

addStyle(wb, "Cleaned Data", style = header_style, rows = 1, cols = 1:ncol(cleaned_final), gridExpand = TRUE)

 

# Step 4: Save the workbook with the dynamic date

file_name <- paste0("G:/Personal Documents/OUTPUT/", date, "_strike_card_cleaned.xlsx")

saveWorkbook(wb, file_name, overwrite = TRUE)

 

################################################################################

############################ DIVIDE LIST BY REGION #############################

################################################################################

 

########################### Bring in Zip Code data ##############################

 

#download zip shapefile

zip <- st_read("H:/GOSR-Research and Strategic Analysis/Requests/20240201_Buyout_Priority_Index/tl_2020_us_zcta520.shp") %>%

  select(GEOID20, geometry)

 

# Get state shapefile

state <- st_read("H:/GOSR-Research and Strategic Analysis/Requests/20240201_Buyout_Priority_Index/tl_rd22_us_state.shp") %>%

  select(STUSPS, NAME, geometry)

 

# Spatially join states to ZIP codes (left join to keep all ZIPs)

zip_states_joined <- st_join(zip, state, left = TRUE)

 

# Convert both columns to integer (ensuring they are numeric)

cleaned_final <- cleaned_final %>%

  mutate(Zip.code = as.integer(Zip.code))

 

zip_states_joined <- zip_states_joined %>%

  mutate(GEOID20 = as.integer(GEOID20))

 

# Join data by numeric ZIP codes

cleaned_final_joined <- left_join(cleaned_final, zip_states_joined,

                                  by = c("Zip.code" = "GEOID20"),

                                  relationship = "many-to-many")

 

# make final list #

final <- cleaned_final_joined %>%

  select(Timestamp, Name, Email, Phone.number, Zip.code, NAME, STUSPS, Source)

 

############################# DEAL WITH PO BOXES ###############################

 

# Convert `Zip.code` to character to preserve leading zeros

final <- final %>%

  mutate(Zip.code = as.character(Zip.code))

 

# Ensure zip_po uses 5-digit format and join it with `final`

 

zip_po <- read.csv("G:/Personal Documents/ANALYSIS/zip_code_database_with_PO_Boxes.csv") %>%

  mutate(zip = str_pad(as.character(zip), 5, pad = "0")) %>%  # Preserve leading zeros

  select(zip, state) %>%

  rename(Zip.code = zip)

 

# Join to fill missing STUSPS values

final <- final %>%

  left_join(zip_po, by = "Zip.code") %>%

  mutate(STUSPS = ifelse(!is.na(Zip.code) & (is.na(STUSPS) | STUSPS == ""), state, STUSPS)) %>%

  select(-state)

 

# Identify rows where STUSPS is still missing

missing_stusps <- final %>%

  filter(is.na(STUSPS) | STUSPS == "")

 

# Count how many Zip.codes are missing

num_missing_zip <- final %>%

  filter(is.na(Zip.code) | Zip.code == "" | nchar(Zip.code) < 5) %>%

  nrow()

print(paste("Number of rows with missing or invalid Zip.code:", num_missing_zip))

 

# Create state lookup with numeric zip ranges

state_zip_lookup <- data.frame(

  STUSPS = c("AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",

             "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",

             "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",

             "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",

             "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"),

  NAME = c("Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",

           "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",

           "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",

           "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",

           "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",

           "New Hampshire", "New Jersey", "New Mexico", "New York",

           "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",

           "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",

           "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",

           "West Virginia", "Wisconsin", "Wyoming"),

  ZIP_MIN = c(35000, 99500, 85000, 71600, 90000, 80000, 6000, 19700, 32000, 30000,

              96700, 83200, 60000, 46000, 50000, 66000, 40000, 70000, 3900, 20600,

              1000, 48000, 55000, 38600, 63000, 59000, 68000, 88900, 3000, 7000,

              87000, 10000, 27000, 58000, 43000, 73000, 97000, 15000, 2800, 29000,

              57000, 37000, 75000, 84000, 5000, 20100, 98000, 24700, 53000, 82000),

  ZIP_MAX = c(36999, 99999, 86999, 72999, 96199, 81999, 6999, 19999, 34999, 31999,

              96999, 83999, 62999, 47999, 52999, 67999, 42999, 71599, 4999, 21999,

              2799, 49999, 56799, 39999, 65999, 59999, 69999, 89999, 3899, 8999,

              88499, 14999, 28999, 58899, 45999, 74999, 97999, 19699, 2999, 29999,

              57999, 38599, 79999, 84999, 5999, 24699, 99499, 26899, 54999, 83199)

)

 

# Convert ZIP_MIN & ZIP_MAX to numeric

state_zip_lookup <- state_zip_lookup %>%

  mutate(ZIP_MIN = as.numeric(ZIP_MIN),

         ZIP_MAX = as.numeric(ZIP_MAX)) %>%

  arrange(ZIP_MIN, ZIP_MAX)

 

# Function to find the correct state for a given ZIP Code

find_state <- function(zip) {

  zip <- as.numeric(zip)  # Convert Zip.code to numeric

  match_idx <- which(state_zip_lookup$ZIP_MIN <= zip & zip <= state_zip_lookup$ZIP_MAX)

  if (length(match_idx) > 0) {

    return(state_zip_lookup[match_idx[1], c("STUSPS", "NAME")])

  } else {

    return(data.frame(STUSPS = NA, NAME = NA))

  }

}

 

# Apply state lookup only to missing STUSPS entries

missing_stusps_indices <- which(is.na(final$STUSPS) | final$STUSPS == "")

 

state_data <- map_dfr(final$Zip.code[missing_stusps_indices], find_state)

 

# Ensure length match before assigning values

if (nrow(state_data) == length(missing_stusps_indices)) {

  final$STUSPS[missing_stusps_indices] <- state_data$STUSPS

  final$NAME[missing_stusps_indices] <- state_data$NAME

} else {

  stop("Mismatch in number of rows between `state_data` and `missing_stusps_indices`")

}

 

# Final count of missing STUSPS

num_missing_stusps <- sum(is.na(final$STUSPS) | final$STUSPS == "")

print(paste("Number of rows with missing STUSPS:", num_missing_stusps))

 

##################### CREATE STATE AND ZIP CODE COUNTS #########################

 

# Count the number of rows per state

state_counts <- final %>%

  count(STUSPS, name = "Count") %>%  # Count occurrences of each state

  arrange(desc(Count))  # Sort by count (descending)

 

# Join state_counts to state shapefile based on STUSPS

state_count_shp <- state %>%

  left_join(state_counts, by = "STUSPS")

 

st_write(state_count_shp,

         dsn = "G:/Personal Documents/OUTPUT/state_counts.shp",

         driver = "ESRI Shapefile",

         delete_layer = TRUE)

 

# Count the number of rows per Zip Code in final

zip_counts <- final %>%

  count(Zip.code, name = "Count") %>%  # Count occurrences of each Zip Code

  arrange(desc(Count))  # Sort by count (descending)

 

# Convert Zip.code and GEOID20 to integers for correct matching

zip_counts <- zip_counts %>%

  mutate(Zip.code = as.integer(Zip.code))

 

zip <- zip %>%

  mutate(GEOID20 = as.integer(GEOID20))

 

# Join zip_counts to zip shapefile based on Zip.code (final) and GEOID20 (zip)

zip_count_shp <- zip %>%

  left_join(zip_counts, by = c("GEOID20" = "Zip.code"))

 

# Save as a shapefile

st_write(zip_count_shp,

         dsn = "G:/Personal Documents/OUTPUT/zip_counts.shp",

         driver = "ESRI Shapefile",

         delete_layer = TRUE)

 

# Save as an Excel file (ensure file extension is .xlsx)

#write.xlsx(zip_count_shp, "zip_count.xlsx", overwrite = TRUE)

 

####################### EXPORT FINAL STATES ###################################

 

# Filter dataset to only include rows where STUSPS is "OR"

illinois <- final %>%

  filter(STUSPS == "IL") %>%

  separate(Name, into = c("First Name", "Last Name"), sep = " ", extra = "merge", fill = "right")

 

# Define file path with today's date in the filename

file_path <- paste0("G:/Personal Documents/OUTPUT/IL_", date, ".csv")

 

# Export the filtered dataset as a CSV file

write.csv(illinois, file_path, row.names = FALSE)
