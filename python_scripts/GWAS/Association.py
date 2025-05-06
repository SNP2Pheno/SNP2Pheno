class Association:
    def __init__(self):
        self.pValueExponent = 0
        self.pValueMantissa = 0
        self.orValue = 0.0
        self.CIMax = 0.0
        self.CIMin = 0.0
        self.expression = "Unknown"
        self.trait_name = "Unknown Trait"

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
