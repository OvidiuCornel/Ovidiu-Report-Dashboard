def generate_employee_report(employee_obj):
    return f"""
    <div>
        <h2>Raport pentru angajat: {employee_obj.name}</h2>
        <p><strong>ID:</strong> {employee_obj.id}</p>
        <p><strong>Rol:</strong> {employee_obj.role}</p>
        <p><strong>Departament:</strong> {employee_obj.department}</p>
    </div>
    """


def generate_team_report(team_obj):
    members_html = "".join(
        f"<li>{member.name} (rol: {member.role})</li>"
        for member in team_obj.members
    )

    return f"""
    <div>
        <h2>Raport pentru echipă: {team_obj.name}</h2>
        <p><strong>ID echipă:</strong> {team_obj.id}</p>
        <p><strong>Număr membri:</strong> {len(team_obj.members)}</p>
        <ul>{members_html}</ul>
    </div>
    """
