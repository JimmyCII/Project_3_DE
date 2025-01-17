# Project_3_DE
Data Engineering of recreation.gov facility data

## Obtaining an RIDB API Key

To use the Recreation.gov API (RIDB API), you'll need an API key. This key authenticates your requests and allows you to access the data. Follow these steps to obtain one:

1. **Create a Recreation.gov Account:**
   - If you don't already have one, go to [Recreation.gov](https://www.recreation.gov/) and create an account.
   - Follow the on-screen instructions to register.

2. **Log In to Your Account:**
   - Once you have an account, log in to [Recreation.gov](https://www.recreation.gov/) using your credentials.

3. **Access Your Profile:**
   - After logging in, navigate to your profile page. This is usually found by clicking on your username or avatar in the upper right corner of the screen.
   - Select the **Profile** option (or a similarly labeled item) from the dropdown menu.

4. **Generate an API Key:**
   - On your profile page, look for a section or tab related to API keys, developer settings, or similar (it may be labeled something like "API Keys" or "Developer").
   - Within this section, you'll find an option to generate a new API key. Click on the appropriate button or link (e.g., "Generate API Key", "Create New Key", etc.).
   - If you already have a key you may want to use this one.

5. **Secure Your API Key:**
    - **Important:** Treat your API key like a password! **Do not share it publicly or commit it directly to your code repository.**
    -  Store it securely. Consider using environment variables, a dedicated secrets manager, or your operating system's secure keystore for storing the key during development.  Do not check it into any Git repository!
    - When committing files use `.gitignore` to exclude API keys.
6. **Use the API Key:**
   - You'll need to include your API key in your requests to the RIDB API.  Refer to the [RIDB API documentation](https://ridb.recreation.gov/docs#/) for instructions on how to include the key in the `apikey` request header for each API request.

## Code Documentation

The project's code is documented with comprehensive docstrings, making it easy to understand how each function works and can be used. You can access the docstrings in an interactive Python environment, or by using documentation generation tools such as sphinx.

## Notes for commit Delete when refining readme.
   - 1/17/2025 JC: removed print statement (No data found in API response) in the create_dataframe function to prevent unnecessary error messages in the console. 

## Explanation for Data Analyst For Presentation
"When we were designing how to store our data in the database, we had a few options on what data we would include in each table.
We started by pulling all of the data from the facilities endpoint, and got a lot of fields in our result. We noticed that the API was also sending back three fields in the facilities response: ACTIVITY, CAMPSITE, and EVENT. However, these fields were empty lists, and it was confusing to include those in the data frame when we had separate data frames that contained the related data.
When we first started, it was suggested that we remove these columns from the dataset. However, as we started using our data we realized that the original columns were helpful to have because we can use them as a high level indicator of whether or not a facility has related information without needing to join that table with another table. For instance, if you just wanted to check which facilities in Arizona had campsites you could quickly use df[df["CAMPSITES"].astype(bool)] and see what was available. So after some testing we decided it was useful to keep the original ACTIVITY, CAMPSITE, and EVENT columns in the facilities table even though they contained null values.
For the campsites table, however, we initially started off by adding a column for PERMITTEDEQUIPMENT and ATTRIBUTES. These columns contained information that was organized as a list of dictionaries (for example: [{'EquipmentName': 'Tent', 'MaxLength': 40}, {'EquipmentName': 'RV', 'MaxLength': 35}]).
Since we wanted to normalize our data, we decided to create new tables called PermittedEquipment and CampsiteAttributes that contained the information from these columns, so that they were no longer nested in the campsites table. Once we had done that, there was no longer a need to keep those nested values in our campsites table, and because of that, we dropped the PERMITTEDEQUIPMENT and ATTRIBUTES columns.
By doing this we have normalized our data, reduced data redundancy, and created more efficient tables to store and manage data."
Key Points to Emphasize for the Audience:
•	Data Normalization: We were aiming to create a well-structured, efficient data model by separating related information into different tables.
•	Redundancy: We avoided redundancy by not storing the same information in multiple tables.
•	Use Cases: We made a decision on whether to keep a column or not based on what use cases we would have for them. If the column is useful and does not duplicate other information, it's a good idea to keep the column. If it is duplicated data, and does not provide an additional benefit, then it is best to remove it.
•	Clarity: We wanted each table to contain a clear set of data and not be overly complex.
•	Flexibility: By separating the information into different tables we now have more flexibility to extend the data model with new features in the future.
