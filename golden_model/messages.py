type_to_shape = {
    "S": {"fields": ["eventCode"],
          "lengths": [1],
          "kinds": ["alpha"]},

    "R": {"fields": ["stock", "marketCategory", "financialStatusIndicator", "roundLotSize",
                     "roundLotsOnly", "issueClassification", "issueSubType", "authenticity",
                     "shortSaleThresholdIndicator", "ipoFlag", "luldReferencePriceTier",
                     "etpFlag", "etpLeverageFactor", "inverseIndicator"],
          "lengths": [8, 1, 1, 4, 1, 1, 2, 1, 1, 1, 1, 1, 4, 1],
          "kinds": ["alpha", "alpha", "alpha", "int", "alpha", "alpha", "alpha", "alpha",
                    "alpha", "alpha", "alpha", "alpha", "int", "alpha"]},

    "H": {"fields": ["stock", "tradingState", "reserved", "reason"],
          "lengths": [8, 1, 1, 4],
          "kinds": ["alpha", "alpha", "alpha", "alpha"]},

    "Y": {"fields": ["stock", "regShoAction"],
          "lengths": [8, 1],
          "kinds": ["alpha", "alpha"]},

    "L": {"fields": ["mpid", "stock", "primaryMarketMaker", "marketMakerMode",
                     "marketParticipantState"],
          "lengths": [4, 8, 1, 1, 1],
          "kinds": ["alpha", "alpha", "alpha", "alpha", "alpha"]},

    "V": {"fields": ["level1", "level2", "level3"],
          "lengths": [8, 8, 8],
          "kinds": ["price8", "price8", "price8"]},

    "W": {"fields": ["breachedLevel"],
          "lengths": [1],
          "kinds": ["alpha"]},

    "K": {"fields": ["stock", "ipoQuotationReleaseTime", "ipoQuotationReleaseQualifier",
                     "ipoPrice"],
          "lengths": [8, 4, 1, 4],
          "kinds": ["alpha", "int", "alpha", "price4"]},

    "J": {"fields": ["stock", "auctionCollarReferencePrice", "upperAuctionCollarPrice",
                     "lowerAuctionCollarPrice", "auctionCollarExtension"],
          "lengths": [8, 4, 4, 4, 4],
          "kinds": ["alpha", "price4", "price4", "price4", "int"]},

    "h": {"fields": ["stock", "marketCode", "operationalHaltAction"],
          "lengths": [8, 1, 1],
          "kinds": ["alpha", "alpha", "alpha"]},

    "A": {"fields": ["orderReferenceNumber", "buySellIndicator", "shares", "stock", "price"],
          "lengths": [8, 1, 4, 8, 4],
          "kinds": ["int", "alpha", "int", "alpha", "price4"]},

    "F": {"fields": ["orderReferenceNumber", "buySellIndicator", "shares", "stock",
                     "price", "attribution"],
          "lengths": [8, 1, 4, 8, 4, 4],
          "kinds": ["int", "alpha", "int", "alpha", "price4", "alpha"]},

    "E": {"fields": ["orderReferenceNumber", "executedShares", "matchNumber"],
          "lengths": [8, 4, 8],
          "kinds": ["int", "int", "int"]},

    "C": {"fields": ["orderReferenceNumber", "executedShares", "matchNumber",
                     "printable", "executionPrice"],
          "lengths": [8, 4, 8, 1, 4],
          "kinds": ["int", "int", "int", "alpha", "price4"]},

    "X": {"fields": ["orderReferenceNumber", "cancelledShares"],
          "lengths": [8, 4],
          "kinds": ["int", "int"]},

    "D": {"fields": ["orderReferenceNumber"],
          "lengths": [8],
          "kinds": ["int"]},

    "U": {"fields": ["originalOrderReferenceNumber", "newOrderReferenceNumber",
                     "shares", "price"],
          "lengths": [8, 8, 4, 4],
          "kinds": ["int", "int", "int", "price4"]},

    "P": {"fields": ["orderReferenceNumber", "buySellIndicator", "shares", "stock",
                     "price", "matchNumber"],
          "lengths": [8, 1, 4, 8, 4, 8],
          "kinds": ["int", "alpha", "int", "alpha", "price4", "int"]},

    "Q": {"fields": ["shares", "stock", "crossPrice", "matchNumber", "crossType"],
          "lengths": [8, 8, 4, 8, 1],
          "kinds": ["int", "alpha", "price4", "int", "alpha"]},

    "B": {"fields": ["matchNumber"],
          "lengths": [8],
          "kinds": ["int"]},

    "I": {"fields": ["pairedShares", "imbalanceShares", "imbalanceDirection", "stock",
                     "farPrice", "nearPrice", "currentReferencePrice", "crossType",
                     "priceVariationIndicator"],
          "lengths": [8, 8, 1, 8, 4, 4, 4, 1, 1],
          "kinds": ["int", "int", "alpha", "alpha", "price4", "price4", "price4",
                    "alpha", "alpha"]},

    "N": {"fields": ["stock", "interestFlag"],
          "lengths": [8, 1],
          "kinds": ["alpha", "alpha"]},

    "O": {"fields": ["stock", "openEligibilityStatus", "minimumAllowablePrice",
                     "maximumAllowablePrice", "nearExecutionPrice", "nearExecutionTime",
                     "lowerPriceRangeCollar", "upperPriceRangeCollar"],
          "lengths": [8, 1, 4, 4, 4, 8, 4, 4],
          "kinds": ["alpha", "alpha", "price4", "price4", "price4", "int", "price4", "price4"]},
}

class Message:
    def __init__(self):
        # Creates the object with key fields and components that all messages must contain.
        self.fields = ["messageType", "stockLocate", "trackingNumber", "timestamp"]
        self.kinds = ["alpha", "int", "int", "int"]
        self.lengths = [1, 2, 2, 6]
        self.messageType = None
        self.stockLocate = None
        self.trackingNumber = None
        self.timestamp = None
    def set_type(self, type):
        # Adds type specific fields, lengths of each field, and the kind of data each field contains based on the type of message.
        self.fields = self.fields + type_to_shape[type]["fields"]
        self.lengths = self.lengths + type_to_shape[type]["lengths"]
        self.kinds = self.kinds + type_to_shape[type]["kinds"]
