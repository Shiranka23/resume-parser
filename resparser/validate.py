import re

achievement_keywords = ["achieved", "awarded", "honored", "recognized", "accomplished", "prize", "medal", "trophy", "Achievements",'Certificate','certificate','award']
demography = ['emails', 'phoneNumbers', 'state', 'city']


checked_data = {
    'demography': False,
    'education': False,
    'dates': True,
    'achievements': False,
    'job_description': False,
    'company_description':False,
}

def extract_city_and_state(location):
    city = location['city']
    state = location['state']
    return city, state

def validate_demography(data):
    issues=[]
    if not data['emails']:
        issues.append('emails')

    if not data['phoneNumbers']:
        issues.append('phoneNumbers')

    location = data['location']
    city,state='',''
    if location:
        city, state = extract_city_and_state(location)

    if not city:
        issues.append('city')

    if not state:
        issues.append('state')

    if all(data[key] for key in ['emails', 'phoneNumbers', 'location']):
        checked_data['demography'] = True

    return issues

def validate_education(data):
    issues=[]
    if 'education' in data:
        checked_data['education'] = True
    else:
        issues.append('education')
    
    return issues

def validate_job_description(data):
    if data['workExperience']:
        job_entries = data['workExperience']
    else:
        # print("job")
        return ['jobDescription']
    job_titles = [entry['jobTitle'] for entry in job_entries]
    for entry in job_entries:
        print(entry['jobDescription'])
        if entry['jobDescription']:
            jobDescription = entry['jobDescription']
        else:
            # print('job2')
            return [str(entry['jobTitle'])+"'s job description is"] 

    if len(job_entries):
        checked_data['job_description'] = True
    else:
        return ['jobDescription']
    
    return []

def validate_achievements(data):
    for section in data['sections']:
        text = section['text']
        for keyword in achievement_keywords:
            if keyword in text:
                checked_data['achievements'] = True
                return []
    return ['achievements']

def validate_dates(data):
    issues=[]
    for entry in data['education']:
        if not entry["dates"]:
            date_data=str(entry["organization"])+"'s date is missing"
            issues.append(date_data)

    for entry in data['workExperience']:
        if not entry["dates"]:
            if entry["organization"] is not None:
                date_data=str(entry["organization"])+"'s date is missing"
                issues.append(date_data)
            else:
                issues.append('organization is missing')

    checked_data['dates'] = not issues
    return issues

def validate_company_description(data):
    issues = []
    issues.append('company description')
    return issues

def validate(data):
    issues = []
    print('1')
    issues.extend(validate_demography(data))
    print('2')
    issues.extend(validate_education(data))
    print('3')
    issues.extend(validate_job_description(data))
    print('4')
    issues.extend(validate_achievements(data))
    print('5')
    issues.extend(validate_dates(data))
    print('6')
    issues.extend(validate_company_description(data))
    print('7')

    compare_value = 6
    issues_count=0
    for count in checked_data:
        if checked_data[count]==False:
            issues_count += 1
    score_obtained = (6 - issues_count) / compare_value * 100
    score_obtained=round(score_obtained, 2)
    # print("issues : ",issues,"checked data : ",checked_data,"score : ",score_obtained)
    return score_obtained, issues, checked_data

# Example usage:
# data = {
#     'emails': [],
#     'phoneNumbers': [],
#     'location': {'city': 'New York', 'state': 'NY'},
#     'education': [],
#     'workExperience': [],
#     'sections': [{'text': 'Received an award'}]
# }

# score, validation_issues, checked_data = validate(data)
# print(f"Validation Score: {score}%")
# print(f"Validation Issues: {validation_issues}")
# print(f"Checked Data: {checked_data}")
