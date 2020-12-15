from flask.json import jsonify


data = [{'company_name': 'Metus', 'department_name': 'Management', 'job': 'manager', 'about': 'Started 7 year ago. So many memories about company. Soccer lover.'}]
print(data[0])



print(jsonify(data[0]))