from flask import jsonify, request
from hr_system import app, db
from .models import Employee, Department

@app.route('/employees/<department_name>', methods=['GET'])
def get_employees_by_department(department_name):
    department = Department.query.filter_by(name=department_name).first()
    if department:
        employees = Employee.query.filter_by(department_id=department.id).all()
        return jsonify([{'name': employee.name, 'age': employee.age, 'hiring_date': str(employee.hiring_date)} for employee in employees])
    return jsonify({'message': 'Department not found'}), 404

@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.json
    department_name = data.get('department')
    department = Department.query.filter_by(name=department_name).first()
    if not department:
        return jsonify({'message': 'Department not found'}), 404

    employee = Employee(name=data['name'], age=data['age'], hiring_date=data['hiring_date'], department=department)
    db.session.add(employee)
    db.session.commit()
    return jsonify({'message': 'Employee added successfully'}), 201
