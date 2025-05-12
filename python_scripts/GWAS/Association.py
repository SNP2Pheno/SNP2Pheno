from enum import Enum

class TYPE(Enum):
    DISEASE = 1
    APPEARANCE = 2

class Association:
    def __init__(self):
        self.pValueExponent = 0
        self.pValueMantissa = 0
        self.orValue = 0.0
        self.betaNum = 0.0
        self.betaUnit = "Unknown"
        self.betaDirection = "Unknown"
        self.CIMax = 0.0
        self.CIMin = 0.0
        self.expression = "Unknown"
        self.trait_name = "Unknown Trait"
        self.type = TYPE.DISEASE
        self.NumOfIndividualsInStudy = 0


    # Getter and Setter for pValueExponent
    @property
    def pValueExponent(self):
        return self._pValueExponent

    @pValueExponent.setter
    def pValueExponent(self, value):
        self._pValueExponent = value

    # Getter and Setter for pValueMantissa
    @property
    def pValueMantissa(self):
        return self._pValueMantissa

    @pValueMantissa.setter
    def pValueMantissa(self, value):
        self._pValueMantissa = value

    # Getter and Setter for orValue
    @property
    def orValue(self):
        return self._orValue

    @orValue.setter
    def orValue(self, value):
        self._orValue = value

    # Getter and Setter for CIMax
    @property
    def CIMax(self):
        return self._CIMax

    @CIMax.setter
    def CIMax(self, value):
        self._CIMax = value

    # Getter and Setter for CIMin
    @property
    def CIMin(self):
        return self._CIMin

    @CIMin.setter
    def CIMin(self, value):
        self._CIMin = value

    # Getter and Setter for expression
    @property
    def expression(self):
        return self._expression

    @expression.setter
    def expression(self, value):
        self._expression = value

    # Getter and Setter for trait_name
    @property
    def trait_name(self):
        return self._trait_name

    @trait_name.setter
    def trait_name(self, value):
        self._trait_name = value

    # Getter and Setter for type
    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if isinstance(value, TYPE):
            self._type = value
        else:
            raise ValueError("Invalid type. Must be an instance of TYPE Enum.")

    # Getter and Setter for betaNum
    @property
    def betaNum(self):
        return self._betaNum

    @betaNum.setter
    def betaNum(self, value):
        self._betaNum = value


    # Getter and Setter for betaUnit
    @property
    def betaUnit(self):
        return self._betaUnit

    @betaUnit.setter
    def betaUnit(self, value):
        self._betaUnit = value


    # Getter and Setter for betaDirection
    @property
    def betaDirection(self):
        return self._betaDirection

    @betaDirection.setter
    def betaDirection(self, value):
        self._betaDirection = value

    # Getter and Setter for NumOfIndividualsInStudy
    @property
    def NumOfIndividualsInStudy(self):
        return self._NumOfIndividualsInStudy

    @NumOfIndividualsInStudy.setter
    def NumOfIndividualsInStudy(self, value):
        self._NumOfIndividualsInStudy = value

    def __str__(self):
        return (
            f"Association("
            f"pValueExponent={self.pValueExponent}, "
            f"pValueMantissa={self.pValueMantissa}, "
            f"orValue={self.orValue}, "
            f"betaNum={self.betaNum}, "
            f"betaUnit='{self.betaUnit}', "
            f"betaDirection='{self.betaDirection}', "
            f"CIMax={self.CIMax}, "
            f"CIMin={self.CIMin}, "
            f"expression='{self.expression}', "
            f"trait_name='{self.trait_name}', "
            f"type={self.type.name}), "
            f"NumOfIndividualsInStudy={self.NumOfIndividualsInStudy}"
        )