class IdentityMasking:
    """
    Role-based masking for the structured 17-digit User ID.

    Preserves the legacy masking contract:
    - leader  -> full identity
    - deputy1 -> full identity
    - deputy2 -> country + province + masked county/city
    - user/other -> country + masked province/county/city
    """

    def mask_id(self, full_id: str, role: str = "user") -> str:
        parts = full_id.split("-")

        if len(parts) != 5:
            raise ValueError("Invalid structured identity format")

        country = parts[0]
        province = parts[1]
        county = parts[2]
        city = parts[3]
        personal = parts[4]

        if role == "leader":
            return full_id

        if role == "deputy1":
            return f"{country}-{province}-{county}-{city}-{personal}"

        if role == "deputy2":
            return f"{country}-{province}-XX-XX-{personal}"

        return f"{country}-XXX-XX-XX-{personal}"
