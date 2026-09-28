def check_ppe(worker, risk):

    missing = []

    if not worker["helmet"]:
        missing.append("Helmet")

    if not worker["vest"]:
        missing.append("Safety Vest")

    if not worker["gloves"]:
        missing.append("Gloves")

    if not worker["boots"]:
        missing.append("Safety Shoes")

    # No PPE violation
    if not missing:
        message = "✅ Worker is Safe"

    # PPE violation
    else:
        message = "🚨 PPE Missing: " + ", ".join(missing)

    # Add AI risk level
    message += f"\n⚠️ Safety Risk: {risk}"

    return message






