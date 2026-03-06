class KgToLbsTool:
    name = "kg_to_lbs"

    def run(self, value: float) -> float:
        return value * 2.2046226218


class LbsToKgTool:
    name = "lbs_to_kg"

    def run(self, value: float) -> float:
        return value / 2.2046226218


class MToFtTool:
    name = "m_to_ft"

    def run(self, value: float) -> float:
        return value * 3.280839895


class FtToMTool:
    name = "ft_to_m"

    def run(self, value: float) -> float:
        return value / 3.280839895


class CToFTool:
    name = "c_to_f"

    def run(self, value: float) -> float:
        return (value * 9 / 5) + 32


class FToCTool:
    name = "f_to_c"

    def run(self, value: float) -> float:
        return (value - 32) * 5 / 9


class GallonsToLitersTool:
    name = "gal_to_l"

    def run(self, value: float) -> float:
        return value * 3.785411784


class LitersToGallonsTool:
    name = "l_to_gal"

    def run(self, value: float) -> float:
        return value / 3.785411784


class MphToKmhTool:
    name = "mph_to_kmh"

    def run(self, value: float) -> float:
        return value * 1.609344


class KmhToMphTool:
    name = "kmh_to_mph"

    def run(self, value: float) -> float:
        return value / 1.609344


class CmToInchesTool:
    name = "cm_to_in"

    def run(self, value: float) -> float:
        return value * 0.3937007874


class InchesToCmTool:
    name = "in_to_cm"

    def run(self, value: float) -> float:
        return value / 0.3937007874