from datetime import datetime
from flask import Flask, request, jsonify
from app.db import connect_db

app = Flask(__name__)
app.json.sort_keys = False

@app.route("/property/<address>/", methods=["GET"])
def get_property(address):
    # normalize address to match format
    address = address.strip().lower()

    conn = connect_db()
    cursor = conn.cursor()

    # query all violations for this address
    cursor.execute("""
        SELECT date, code, status, description, inspector_comments
        FROM violations
        WHERE LOWER(TRIM(address)) = %s
    """, (address,))
    rows = cursor.fetchall()

    # return 404 if no violations found for this address
    if not rows:
        cursor.close()
        conn.close()
        return jsonify({"error": "No property found for this address"}), 404

    # build violations array from query results
    violations = []
    for row in rows:
        violations.append({
            "date": row[0].isoformat() if row[0] else None,
            "code": row[1],
            "status": row[2],
            "description": row[3],
            "inspector_comments": row[4]
        })

    # calculate last violation date and total count
    valid_dates = []
    for v in violations:
        if v["date"]:
            valid_dates.append(v["date"])
    last_violation_date = max(valid_dates)

    total_count = len(violations)

    # check if address is a scofflaw
    cursor.execute("""
        SELECT EXISTS (
            SELECT 1 FROM scofflaws
            WHERE LOWER(TRIM(address)) = %s
        )
    """, (address,))
    scofflaw = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return jsonify({
        "address": address,
        "last_violation_date": last_violation_date,
        "total_violation_count": total_count,
        "violations": violations,
        "scofflaw": scofflaw
    }), 200

@app.route("/property/<address>/comments/", methods=["POST"])
def post_comment(address):
    data = request.get_json()

    # sanitization - make sure data exists
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # sanitization - check required fields
    author = data.get("author", "").strip()
    comment = data.get("comment", "").strip()

    missing = []
    if not author:
        missing.append("author")
    if not comment:
        missing.append("comment")

    # return 400 if required fields are missing
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    # normalize address to match format
    address = address.strip().lower()

    # generate timestamp automatically
    timestamp = datetime.now()

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO comments (author, datetime, address, comment)
        VALUES (%s, %s, %s, %s)
    """, (
        author,
        timestamp,
        address,
        comment
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Comment created successfully"}), 201


@app.route("/property/scofflaws/violations", methods=["GET"])
def get_scofflaw_violations():

    # access since query parameter from the URL
    since = request.args.get("since")

    # make sure since parameter exists
    if not since:
        return jsonify({"error": "Missing required query parameter: since"}), 400

    # validate date format
    try:
        since_date = datetime.strptime(since.strip(), "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format, expected YYYY-MM-DD"}), 400

    conn = connect_db()
    cursor = conn.cursor()

    # get all scofflaw addresses that had violations on or after since date
    cursor.execute("""
        SELECT DISTINCT s.address
        FROM scofflaws s
        JOIN violations v ON LOWER(TRIM(v.address)) = LOWER(TRIM(s.address))
        WHERE v.date >= %s
    """, (since_date,))

    rows = cursor.fetchall() # list of rows

    cursor.close()
    conn.close()

    # build an array of address strings
    addresses = []

    for row in rows:
        address = row[0] 
        addresses.append(address)

    return jsonify({"addresses": addresses}), 200


if __name__ == "__main__":
    app.run(debug=True)