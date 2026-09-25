from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "script_acl_project"

# Sample Incident records
incidents = [
    {
        "id": 1,
        "number": "INC0001",
        "short_description": "Server Down",
        "priority": "1",
        "priority_name": "Critical"
    },
    {
        "id": 2,
        "number": "INC0002",
        "short_description": "Network Issue",
        "priority": "2",
        "priority_name": "High"
    },
    {
        "id": 3,
        "number": "INC0003",
        "short_description": "Email Problem",
        "priority": "3",
        "priority_name": "Moderate"
    },
    {
        "id": 4,
        "number": "INC0004",
        "short_description": "Printer Issue",
        "priority": "4",
        "priority_name": "Low"
    }
]


@app.route("/")
def home():
    return render_template("index.html", incidents=incidents)


@app.route("/login", methods=["POST"])
def login():
    role = request.form.get("role")

    if role == "admin":
        session["role"] = "admin"
    else:
        session["role"] = "user"

    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.pop("role", None)
    return redirect(url_for("home"))


@app.route("/incident/<int:incident_id>")
def view_incident(incident_id):

    role = session.get("role", "user")

    incident = next(
        (item for item in incidents if item["id"] == incident_id),
        None
    )

    if incident is None:
        return "Incident not found", 404

    # ACL logic
    # Critical incidents can be viewed only by admin
    if incident["priority"] == "1" and role != "admin":
        return """
        <h2>Access Denied</h2>
        <p>You are not authorized to view Critical incidents.</p>
        <a href="/">Back</a>
        """, 403

    return render_template(
        "incident.html",
        incident=incident,
        role=role
    )


if __name__ == "__main__":
    app.run(debug=True)
