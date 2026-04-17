def validate_sector(sector: str):
    if not sector.isalpha():
        raise ValueError("Sector must contain only letters")
    return sector.lower()