import re

achievement_keywords = ["achieved", "awarded", "honored", "recognized", "accomplished", "prize", "medal", "trophy", "Achievements"]
demography = ['emails', 'phoneNumbers', 'state', 'city']
checked_data = {
    'demography': False,
    'education': False,
    'dates': True,
    'achievements': False,
    'job_title': False,
    'demography': False,
}

def extract_city_and_state(location):
    city = location['city']
    state = location['state']
    return city, state

def validate_demography(data):

    issues = []
    if not data['emails']:
        issues.append('emails')


    if not data['phoneNumbers']:
        issues.append('phoneNumbers')

    location = data['location']
    if location:
        city, state = extract_city_and_state(location)
    else:
        city,state='',''

    if not city:
        issues.append('city')

    if not state:
        issues.append('state')

    if all(data[key] for key in ['emails', 'phoneNumbers', 'location']):
        checked_data['demography'] = True

    return issues

def validate_education(data):
    issues = []
    if 'education' in data:
        checked_data['education'] = True
    else:
        issues.append('education')
    return issues

def validate_job_titles(data):
    job_entries = data['workExperience']
    job_titles = [entry['jobTitle'] for entry in job_entries]
    if len(job_entries) == len(job_titles):
        checked_data['job_title'] = True
    else:
        return ['job title']
    return []

def validate_achievements(data):
    issues = []
    for section in data['sections']:
        text = section['text']
        for keyword in achievement_keywords:
            if keyword in text:
                checked_data['achievements'] = True
                return []
    return ['achievement']

def validate_dates(data):
    issues = []
    for entry in data['education']:
        if "dates" in entry and not entry["dates"]:
            date_data=str(entry["organization"])+"'s date is missing"
            issues.append(date_data)

    for entry in data['workExperience']:
        if "dates" in entry and not entry["dates"]:
            date_data=str(entry["organization"])+"'s date is missing"  
            issues.append(date_data)

    checked_data['dates'] = not issues
    return issues

def validate(data):
    issues = []
    issues.extend(validate_demography(data))
    issues.extend(validate_education(data))
    issues.extend(validate_job_titles(data))
    issues.extend(validate_achievements(data))
    issues.extend(validate_dates(data))

    compare_value = 6
    score_obtained = (6 - len(issues)) / compare_value * 100
    return score_obtained, issues, checked_data

# Example usage:
data = {
    'emails': [],
    'phoneNumbers': [],
    'location': {'city': 'New York', 'state': 'NY'},
    'education': [],
    'workExperience': [],
    'sections': [{'text': 'Received an award'}]
}

score, validation_issues, checked_data = validate(data)
print(f"Validation Score: {score}%")
print(f"Validation Issues: {validation_issues}")
print(f"Checked Data: {checked_data}")
