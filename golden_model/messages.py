ALL_FIELDS = [
    # Header
    "messageType", "stockLocate", "trackingNumber", "timestamp",
    # S
    "eventCode",
    # R
    "stock", "marketCategory", "financialStatusIndicator", "roundLotSize",
    "roundLotsOnly", "issueClassification", "issueSubType", "authenticity",
    "shortSaleThresholdIndicator", "ipoFlag", "luldReferencePriceTier",
    "etpFlag", "etpLeverageFactor", "inverseIndicator",
    # H
    "tradingState", "reserved", "reason",
    # Y
    "regShoAction",
    # L
    "mpid", "primaryMarketMaker", "marketMakerMode", "marketParticipantState",
    # V
    "level1", "level2", "level3",
    # W
    "breachedLevel",
    # K
    "ipoQuotationReleaseTime", "ipoQuotationReleaseQualifier", "ipoPrice",
    # J
    "auctionCollarReferencePrice", "upperAuctionCollarPrice",
    "lowerAuctionCollarPrice", "auctionCollarExtension",
    # h
    "marketCode", "operationalHaltAction",
    # A
    "orderReferenceNumber", "buySellIndicator", "shares", "price",
    # F
    "attribution",
    # E
    "executedShares", "matchNumber",
    # C
    "printable", "executionPrice",
    # X
    "cancelledShares",
    # U
    "originalOrderReferenceNumber", "newOrderReferenceNumber",
    # Q
    "crossPrice", "crossType",
    # I
    "pairedShares", "imbalanceShares", "imbalanceDirection", "farPrice",
    "nearPrice", "currentReferencePrice", "priceVariationIndicator",
    # N
    "interestFlag",
    # O
    "openEligibilityStatus", "minimumAllowablePrice", "maximumAllowablePrice",
    "nearExecutionPrice", "nearExecutionTime", "lowerPriceRangeCollar",
    "upperPriceRangeCollar",
]

class incompleteMessageError(Exception):
    pass

class illegalLengthError(Exception):
    pass

class Message:
    def __init__(self):
        for field in ALL_FIELDS:
            setattr(self, field, 0)
