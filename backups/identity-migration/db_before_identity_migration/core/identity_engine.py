import sqlite3

DB_PATH = "db/2fun.db"


class IdentityEngine:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    # --------------------------
    # COUNTRY CODE (3 digits)
    # --------------------------
    def get_country_code(self, country_id: int) -> str:
        return str(country_id).zfill(3)

    # --------------------------
    # GEOGRAPHY (2 digits each)
    # --------------------------
    def get_province_code(self, province_id: int) -> str:
        return str(province_id).zfill(2)

    def get_county_code(self, county_id: int) -> str:
        return str(county_id).zfill(2)

    def get_city_code(self, city_id: int) -> str:
        return str(city_id).zfill(2)

    # --------------------------
    # PERSONAL CODE (8 digits)
    # --------------------------
    def generate_personal_code(self, user_id: int) -> str:
        return str(user_id).zfill(8)

    # --------------------------
    # FULL ID GENERATION
    # --------------------------
    def generate_full_id(self, country, province, county, city, user_id):
        country_code = self.get_country_code(country)
        province_code = self.get_province_code(province)
        county_code = self.get_county_code(county)
        city_code = self.get_city_code(city)
        personal_code = self.generate_personal_code(user_id)

        return f"{country_code}-{province_code}-{county_code}-{city_code}-{personal_code}"

    # --------------------------
    # MASKING SYSTEM (ROLE BASED)
    # --------------------------
    def mask_id(self, full_id: str, role: str = "user") -> str:
        parts = full_id.split("-")

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
