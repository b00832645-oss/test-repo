"""Builder refactoring of the HR employee onboarding system."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional

CONTRACT_TYPES = {"permanent", "fixed-term", "internship", "apprenticeship", "freelance"}


@dataclass(frozen=True)
class Employee:
    """The product: an immutable record."""
    first_name: str
    last_name: str
    email: str
    department: str
    position: str
    salary: float
    start_date: str
    manager_id: Optional[int] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    has_parking: bool = False
    has_laptop: bool = False
    has_vpn_access: bool = False
    has_admin_rights: bool = False
    office_location: Optional[str] = None
    contract_type: str = "permanent"


class EmployeeBuilder:
    def __init__(self):
        self._data: dict = {"start_date": date.today().isoformat()}

    def with_name(self, first_name: str, last_name: str) -> "EmployeeBuilder":
        self._data.update(first_name=first_name, last_name=last_name)
        return self

    def with_email(self, email: str) -> "EmployeeBuilder":
        self._data["email"] = email
        return self

    def with_job(self, department: str, position: str, salary: float) -> "EmployeeBuilder":
        self._data.update(department=department, position=position, salary=salary)
        return self

    def with_start_date(self, start_date: str) -> "EmployeeBuilder":
        self._data["start_date"] = start_date
        return self

    def with_manager(self, manager_id: int) -> "EmployeeBuilder":
        self._data["manager_id"] = manager_id
        return self

    def with_contact(self, phone: str = None, address: str = None,
                     emergency_contact: str = None) -> "EmployeeBuilder":
        self._data.update(phone=phone, address=address, emergency_contact=emergency_contact)
        return self

    def with_equipment(self, laptop: bool = False, parking: bool = False) -> "EmployeeBuilder":
        self._data.update(has_laptop=laptop, has_parking=parking)
        return self

    def with_access(self, vpn: bool = False, admin: bool = False) -> "EmployeeBuilder":
        self._data.update(has_vpn_access=vpn, has_admin_rights=admin)
        return self

    def at_office(self, location: str) -> "EmployeeBuilder":
        self._data["office_location"] = location
        return self

    def with_contract(self, contract_type: str) -> "EmployeeBuilder":
        self._data["contract_type"] = contract_type
        return self

    def build(self) -> Employee:
        """Validate everything in one place, then create the product."""
        d = self._data
        if not d.get("first_name") or not d.get("last_name"):
            raise ValueError("Name is required")
        if "@" not in d.get("email", ""):
            raise ValueError("Valid email is required")
        if not d.get("department") or not d.get("position"):
            raise ValueError("Job (department and position) is required")
        if d.get("salary", 0) < 0:
            raise ValueError("Salary cannot be negative")
        if d.get("contract_type", "permanent") not in CONTRACT_TYPES:
            raise ValueError(f"Unknown contract type: {d['contract_type']}")
        if d.get("has_admin_rights") and d.get("contract_type") == "internship":
            raise ValueError("Interns cannot have admin rights")
        return Employee(**d)


class DeveloperBuilder(EmployeeBuilder):
    """Preset: developers always get a laptop, VPN and admin rights."""

    def __init__(self, first_name: str, last_name: str, email: str, salary: float = 60000):
        super().__init__()
        (self.with_name(first_name, last_name).with_email(email)
             .with_job("Engineering", "Developer", salary)
             .with_equipment(laptop=True).with_access(vpn=True, admin=True)
             .at_office("Paris HQ"))


class InternBuilder(EmployeeBuilder):
    """Preset: interns get a laptop only, on an internship contract."""

    def __init__(self, first_name: str, last_name: str, email: str, department: str, salary: float = 15000):
        super().__init__()
        (self.with_name(first_name, last_name).with_email(email)
             .with_job(department, "Intern", salary)
             .with_equipment(laptop=True).with_contract("internship")
             .at_office("Paris HQ"))


if __name__ == "__main__":
    emp = (EmployeeBuilder().with_name("John", "Doe").with_email("john.doe@company.com")
           .with_job("Engineering", "Senior Developer", 75000)
           .with_equipment(laptop=True, parking=False).with_access(vpn=True, admin=True).build())
    print(emp)
    print(DeveloperBuilder("John", "Doe", "john.doe@company.com").build())
    print(InternBuilder("Jane", "Smith", "jane.smith@company.com", "Marketing").with_manager(42).build())
