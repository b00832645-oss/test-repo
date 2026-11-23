import dataclasses
import pytest
from employee_builder import EmployeeBuilder, DeveloperBuilder, InternBuilder, Employee


def full_builder():
    return (EmployeeBuilder().with_name("John", "Doe").with_email("john@co.com")
            .with_job("Engineering", "Senior Developer", 75000))


def test_fluent_build():
    emp = full_builder().with_equipment(laptop=True).with_access(vpn=True, admin=True).build()
    assert isinstance(emp, Employee)
    assert (emp.has_laptop, emp.has_vpn_access, emp.has_admin_rights, emp.has_parking) == (True, True, True, False)


def test_each_step_returns_the_builder():
    b = EmployeeBuilder()
    assert b.with_name("A", "B") is b and b.with_email("a@b.c") is b


@pytest.mark.parametrize("builder, message", [
    (EmployeeBuilder().with_email("a@b.c").with_job("X", "Y", 1), "Name is required"),
    (EmployeeBuilder().with_name("A", "B").with_email("nope").with_job("X", "Y", 1), "email"),
    (EmployeeBuilder().with_name("A", "B").with_email("a@b.c"), "Job"),
    (EmployeeBuilder().with_name("A", "B").with_email("a@b.c").with_job("X", "Y", -5), "negative"),
])
def test_validation_in_build(builder, message):
    with pytest.raises(ValueError, match=message):
        builder.build()


def test_developer_preset_encodes_rules():
    dev = DeveloperBuilder("John", "Doe", "john@co.com").build()
    assert dev.has_admin_rights and dev.has_vpn_access and dev.has_laptop
    assert dev.department == "Engineering"


def test_intern_preset_and_rule():
    intern = InternBuilder("Jane", "Smith", "jane@co.com", "Marketing").with_manager(42).build()
    assert intern.contract_type == "internship" and intern.manager_id == 42
    with pytest.raises(ValueError, match="Interns cannot have admin"):
        InternBuilder("Jane", "Smith", "jane@co.com", "Marketing").with_access(admin=True).build()


def test_product_is_immutable():
    emp = full_builder().build()
    with pytest.raises(dataclasses.FrozenInstanceError):
        emp.salary = 1
