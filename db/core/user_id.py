import random


def generate_personal_code():
    """
    تولید کد شخصی 8 رقمی
    """
    return str(random.randint(10000000, 99999999))


def generate_user_id(country, province, county, city, personal_code):
    """
    ساخت User ID هفده رقمی
    """

    return (
        f"{int(country):03d}"
        f"{int(province):02d}"
        f"{int(county):02d}"
        f"{int(city):02d}"
        f"{int(personal_code):08d}"
    )


def parse_user_id(user_id):
    user_id = str(user_id)

    return {
        "country": user_id[0:3],
        "province": user_id[3:5],
        "county": user_id[5:7],
        "city": user_id[7:9],
        "personal_code": user_id[9:17],
    }


def validate_user_id(user_id):
    user_id = str(user_id)

    return (
        len(user_id) == 17
        and user_id.isdigit()
    )
