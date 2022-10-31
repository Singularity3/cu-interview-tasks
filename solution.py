import pandas as pd
import numpy as np
import datetime as dt

enrollments = pd.read_csv("enrollments.csv")
students = pd.read_csv("students.csv")

def get_age(birth_date):
    now = dt.datetime.today()
    dt_birth_date = dt.datetime.strptime(birth_date, '%m/%d/%y')
    age = now.year - dt_birth_date.year
    age -= ((now.month, now.day) < (dt_birth_date.month, dt_birth_date.day))
    return age

# 5. Aggregation. Perform this before merging because it allows easier dropping of duplicate student ids.
# Group students by student_id and return the majors within a group joined with a semicolon as delimiter.
# Then drop duplicate student ids and the original major column.
students['academic_plans'] = students['major'].groupby(students['student_id']).transform(lambda x: ';'.join(x))
students.drop_duplicates(subset='student_id', inplace=True)
students.drop(columns='major', inplace=True)

# 1. Merging data. Simple inner join of the students and enrollments on term_id and student_id.
# The type of join to use is somewhat ambiguous in this context, but I'm interpreting it to be inner
# based on some other clues.
merged_data = pd.merge(students, enrollments, how='inner', on=['term_id', 'student_id'])

# 2. Filtering data. Creates a selection of only the rows where credits_earned is greater than 90.
merged_data = merged_data.loc[merged_data['credits_earned'] > 90]

# 3. Dates. Adds age column, calculated with helper function above.
# The helper function assures the accuracy of the age, as a simpler deltatime comparison
# ignores the existence of leap years.
merged_data['age'] = merged_data['date_of_birth'].apply(get_age)

# 4. String manipulation. Pandas offers a vectorized split method, and it seems like a shame to not use it.
# Split with '-' as the delimiter, expand the result into four columns, and write those columns back into the original df.
# Then drop the placeholder.
merged_data[['course_subject', 'placeholder', 'course_number', 'course_section']] = merged_data['class_id'].str.split('-', expand=True)
merged_data.drop(columns='placeholder', inplace=True)

merged_data.to_csv('results.csv', index=False)