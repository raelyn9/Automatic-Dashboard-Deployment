# Arcadia Deployment Automation

Set up dashboard deployment environment from Hadoop Impala dataset.
Run arcadia.py to start the program.
Users can select specific steps they want to execute.

# Steps
- Step 1: Export the dashboard from source 
- Step 2: Copy the table from source to target
- Step 3: Invalidate metadata for the table in Impala
- Step 4: Invalidata metadata for the table in Arcadia
- Step 5: Modify dashboard json file (title, database, table, dataset)
- Step 6: Import dashboard to prod environment