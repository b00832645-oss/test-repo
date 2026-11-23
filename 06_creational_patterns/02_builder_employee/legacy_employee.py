"""Starting code from the course exercise (kept for comparison; do not use)."""


def create_employee(first_name, last_name, email, department, position, salary, start_date,
                    manager_id=None, phone=None, address=None, emergency_contact=None,
                    has_parking=False, has_laptop=False, has_vpn_access=False,
                    has_admin_rights=False, office_location=None, contract_type="permanent"):
    employee = dict(first_name=first_name, last_name=last_name, email=email, department=department,
                    position=position, salary=salary, start_date=start_date, manager_id=manager_id,
                    phone=phone, address=address, emergency_contact=emergency_contact,
                    has_parking=has_parking, has_laptop=has_laptop, has_vpn_access=has_vpn_access,
                    has_admin_rights=has_admin_rights, office_location=office_location,
                    contract_type=contract_type)
    if not first_name or not last_name:
        raise ValueError("Name is required")
    if not email or "@" not in email:
        raise ValueError("Valid email is required")
    if salary < 0:
        raise ValueError("Salary cannot be negative")
    return employee
