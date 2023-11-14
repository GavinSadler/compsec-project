
## To-do

- `contacts.json` data should be encrypted
- `contacts.json` data should have a separate field for each user's contact
- Combine `credentials.json` and `contacts.json` into one `userdata.json` file
    - Each user should have an email, password, and data field
    - The data field will contain the user's full name, along with the list of their contacts
        - Each contact should have an email and a full name
    - Allow users to delete contacts
- Fix how contacts are displayed
- Allow for graceful exiting when asking for user input
- When registering a user, automatically stop process if the user enters an email that has already been entered, rather than also asking for a password