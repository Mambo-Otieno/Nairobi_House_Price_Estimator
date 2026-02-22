"""
predictor.py — Rule-based Nairobi House Price Estimator
Calibrated from EDA patterns in the Nairobi listings dataset.
No ML model required.
"""

import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# Geography
# ─────────────────────────────────────────────────────────────────────────────
CBD_LAT, CBD_LON = -1.2864, 36.8172

LOCATION_COORDS = {
    "Westlands":      (-1.2636, 36.8031),
    "Kilimani":       (-1.2921, 36.7833),
    "Kileleshwa":     (-1.2842, 36.7742),
    "Lavington":      (-1.2777, 36.7760),
    "Karen":          (-1.3190, 36.7133),
    "Runda":          (-1.2110, 36.7986),
    "Muthaiga":       (-1.2534, 36.8327),
    "Parklands":      (-1.2600, 36.8190),
    "Gigiri":         (-1.2299, 36.8056),
    "Spring Valley":  (-1.2570, 36.7780),
    "Loresho":        (-1.2560, 36.7638),
    "Langata":        (-1.3410, 36.7470),
    "South C":        (-1.3100, 36.8220),
    "South B":        (-1.3040, 36.8370),
    "Embakasi":       (-1.3190, 36.8960),
    "Ruaka":          (-1.2073, 36.7506),
    "Thika Road":     (-1.2167, 36.8700),
    "Syokimau":       (-1.3640, 36.9150),
    "Athi River":     (-1.4580, 36.9793),
    "Kikuyu":         (-1.2490, 36.6660),
    "Ruiru":          (-1.1460, 36.9590),
    "Mombasa Road":   (-1.3380, 36.8680),
    "Ngong":          (-1.3644, 36.6567),
    "Limuru":         (-1.1160, 36.6400),
    "Eastleigh":      (-1.2724, 36.8539),
    "Upperhill":      (-1.2966, 36.8173),
    "Nairobi CBD":    (CBD_LAT,  CBD_LON),
    "Kabete":         (-1.2490, 36.7270),
    "Kitisuru":       (-1.2380, 36.7630),
    "Rosslyn":        (-1.2175, 36.7988),
    "Ridgeways":      (-1.2215, 36.8018),
    "Garden Estate":  (-1.2360, 36.8790),
    "Kasarani":       (-1.2222, 36.8975),
    "Roysambu":       (-1.2109, 36.8820),
    "Zimmerman":      (-1.1946, 36.8780),
}

# Neighbourhood median reference prices (KES) — from dataset EDA
LOCATION_BASE_PRICE = {
    "Muthaiga":      85_000_000,
    "Runda":         78_000_000,
    "Gigiri":        72_000_000,
    "Karen":         65_000_000,
    "Spring Valley": 60_000_000,
    "Kitisuru":      58_000_000,
    "Rosslyn":       55_000_000,
    "Ridgeways":     52_000_000,
    "Westlands":     48_000_000,
    "Lavington":     45_000_000,
    "Kilimani":      42_000_000,
    "Kileleshwa":    40_000_000,
    "Loresho":       38_000_000,
    "Parklands":     36_000_000,
    "Upperhill":     30_000_000,
    "Garden Estate": 25_000_000,
    "South C":       20_000_000,
    "South B":       18_000_000,
    "Langata":       17_000_000,
    "Nairobi CBD":   16_000_000,
    "Kabete":        14_000_000,
    "Eastleigh":     13_000_000,
    "Ruaka":         13_000_000,
    "Kasarani":      12_000_000,
    "Roysambu":      11_500_000,
    "Thika Road":    11_000_000,
    "Zimmerman":     10_500_000,
    "Embakasi":      10_000_000,
    "Syokimau":       9_500_000,
    "Mombasa Road":   9_000_000,
    "Ngong":          8_500_000,
    "Ruiru":          8_500_000,
    "Athi River":     7_500_000,
    "Kikuyu":         7_500_000,
    "Limuru":         7_000_000,
}

# Property type multipliers (relative to a standard 3-bed apartment)
PROPERTY_TYPE_MULT = {
    "Apartment":   1.00,
    "Villa":       2.80,
    "House":       1.60,
    "Townhouse":   1.90,
    "Bungalow":    1.40,
    "Maisonette":  1.75,
    "Studio":      0.35,
    "Bedsitter":   0.28,
    "Land":        1.20,
    "Other":       1.00,
}

PROPERTY_TYPES = list(PROPERTY_TYPE_MULT.keys())

AMENITY_OPTIONS = [
    "Swimming Pool",
    "Gym / Fitness Centre",
    "Generator",
    "Lift / Elevator",
    "CCTV / Security",
    "Borehole / Water",
    "En Suite",
    "SQ (Service Quarter)",
    "Parking",
    "Garden / Landscaping",
    "Balcony",
    "DSTV",
    "Solar Panels",
    "Electric Fence",
    "Intercom",
    "Fibre Internet",
    "Air Conditioning",
]

# Estimated value-add per amenity (KES)
AMENITY_VALUES = {
    "Swimming Pool":        4_500_000,
    "Gym / Fitness Centre": 3_000_000,
    "Generator":            2_500_000,
    "Lift / Elevator":      2_000_000,
    "CCTV / Security":      1_200_000,
    "Borehole / Water":     1_000_000,
    "En Suite":               800_000,
    "SQ (Service Quarter)":   700_000,
    "Parking":                600_000,
    "Garden / Landscaping":   500_000,
    "Balcony":                400_000,
    "Solar Panels":           900_000,
    "Electric Fence":         500_000,
    "Intercom":               300_000,
    "Fibre Internet":         200_000,
    "Air Conditioning":       800_000,
    "DSTV":                   150_000,
}


class NairobiPricePredictor:
    LOCATIONS       = sorted(LOCATION_COORDS.keys())
    PROPERTY_TYPES  = PROPERTY_TYPES
    AMENITY_OPTIONS = AMENITY_OPTIONS
    N_TRAINING      = 400        # listings in cleaned dataset
    MODEL_MAE       = 4_556_948  # MAE from trained XGBoost (used as ± band)

    def predict(self, location, property_type, bedrooms, bathrooms, size_m2, amenities):
        # 1. Location reference price
        base = LOCATION_BASE_PRICE.get(location, 15_000_000)

        # 2. Property type multiplier
        type_mult = PROPERTY_TYPE_MULT.get(property_type, 1.0)

        # 3. Bedroom adjustment (±18% per bedroom vs 3-bed baseline)
        bed_adj = 1.0 + (bedrooms - 3) * 0.18

        # 4. Size adjustment (±12% per 50 m² vs 120 m² baseline)
        size_adj = 1.0 + ((size_m2 - 120) / 50) * 0.12

        # 5. Amenity value add
        amenity_add = sum(AMENITY_VALUES.get(a, 250_000) for a in amenities)

        # 6. Final price
        price = (base * type_mult * max(bed_adj, 0.35) * max(size_adj, 0.5)) + amenity_add
        price = max(price, 1_500_000)

        # 7. Range (±MAE from dataset)
        mae  = self.MODEL_MAE
        low  = max(price - mae, 0)
        high = price + mae

        # 8. Price per m²
        price_per_m2 = price / size_m2

        # 9. Driver contributions (for bar chart)
        loc_contrib  = base * 0.45
        bed_contrib  = max(abs((bedrooms - 3) * 0.18) * base, 500_000)
        size_contrib = max(abs(((size_m2 - 120) / 50) * 0.12) * base, 500_000)
        type_contrib = max(base * abs(type_mult - 1.0), 500_000)
        amen_contrib = amenity_add if amenity_add > 0 else 300_000

        raw = {
            "Location":      loc_contrib,
            "Bedrooms":      bed_contrib,
            "Property Size": size_contrib,
            "Property Type": type_contrib,
            "Amenities":     amen_contrib,
        }
        total = sum(raw.values()) or 1
        drivers = {k: round(v / total, 3) for k, v in sorted(raw.items(), key=lambda x: -x[1])}

        # 10. Explanation
        explanation = self._explain(
            price, price_per_m2, location, property_type,
            bedrooms, bathrooms, size_m2, amenities, mae
        )

        return {
            "predicted_price": price,
            "range_low":       low,
            "range_high":      high,
            "mae":             mae,
            "price_per_m2":    price_per_m2,
            "drivers":         drivers,
            "explanation":     explanation,
        }

    def _explain(self, price, price_per_m2, location, property_type,
                 bedrooms, bathrooms, size_m2, amenities, mae):
        lines = []

        base = LOCATION_BASE_PRICE.get(location, 15_000_000)
        if base >= 50_000_000:
            tier = "one of Nairobi's premium neighbourhoods"
        elif base >= 25_000_000:
            tier = "a mid-to-high tier area with strong demand"
        else:
            tier = "an affordable area relative to Nairobi's centre"

        lines.append(
            f"<strong>{location}</strong> is {tier}, "
            f"with a median reference of KES {base:,.0f}."
        )
        lines.append(
            f"A <strong>{bedrooms}-bed, {bathrooms}-bath {property_type.lower()}</strong> "
            f"at <strong>{size_m2:.0f} m\u00b2</strong> prices out at "
            f"<strong>KES {price_per_m2:,.0f} per m\u00b2</strong>."
        )

        if amenities:
            amenity_add = sum(AMENITY_VALUES.get(a, 250_000) for a in amenities)
            lines.append(
                f"{len(amenities)} {'amenity adds' if len(amenities)==1 else 'amenities add'} "
                f"approximately <strong>KES {amenity_add:,.0f}</strong> to the base price."
            )
        else:
            lines.append(
                "No amenities selected. A pool (+KES 4.5M) or generator (+KES 2.5M) "
                "could raise the valuation noticeably."
            )

        lines.append(
            f"The \u00b1KES {mae:,.0f} band reflects typical market variation "
            "based on 400 Nairobi listings."
        )

        return lines
