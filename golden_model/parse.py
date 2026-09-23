from messages import ALL_FIELDS, Message, incompleteMessageError, illegalLengthError

type_to_length = {
    "S": 12,   # System Event
    "R": 39,   # Stock Directory
    "H": 25,   # Stock Trading Action
    "Y": 20,   # Reg SHO Restriction
    "L": 26,   # Market Participant Position
    "V": 35,   # MWCB Decline Level
    "W": 12,   # MWCB Status
    "K": 28,   # IPO Quoting Period Update
    "J": 35,   # LULD Auction Collar
    "h": 21,   # Operational Halt
    "A": 36,   # Add Order (no MPID)
    "F": 40,   # Add Order (MPID attribution)
    "E": 31,   # Order Executed
    "C": 36,   # Order Executed with Price
    "X": 23,   # Order Cancel
    "D": 19,   # Order Delete
    "U": 35,   # Order Replace
    "P": 44,   # Trade (non-cross)
    "Q": 40,   # Cross Trade
    "B": 19,   # Broken Trade
    "I": 50,   # NOII
    "N": 20,   # RPII
    "O": 48,   # Direct Listing with Capital Raise
}
type_to_shape = {
    "S": {"fields": ["eventCode"],
          "lengths": [1]},

    "R": {"fields": ["stock", "marketCategory", "financialStatusIndicator", "roundLotSize",
                     "roundLotsOnly", "issueClassification", "issueSubType", "authenticity",
                     "shortSaleThresholdIndicator", "ipoFlag", "luldReferencePriceTier",
                     "etpFlag", "etpLeverageFactor", "inverseIndicator"],
          "lengths": [8, 1, 1, 4, 1, 1, 2, 1, 1, 1, 1, 1, 4, 1]},

    "H": {"fields": ["stock", "tradingState", "reserved", "reason"],
          "lengths": [8, 1, 1, 4]},

    "Y": {"fields": ["stock", "regShoAction"],
          "lengths": [8, 1]},

    "L": {"fields": ["mpid", "stock", "primaryMarketMaker", "marketMakerMode",
                     "marketParticipantState"],
          "lengths": [4, 8, 1, 1, 1]},

    "V": {"fields": ["level1", "level2", "level3"],
          "lengths": [8, 8, 8]},

    "W": {"fields": ["breachedLevel"],
          "lengths": [1]},

    "K": {"fields": ["stock", "ipoQuotationReleaseTime", "ipoQuotationReleaseQualifier",
                     "ipoPrice"],
          "lengths": [8, 4, 1, 4]},

    "J": {"fields": ["stock", "auctionCollarReferencePrice", "upperAuctionCollarPrice",
                     "lowerAuctionCollarPrice", "auctionCollarExtension"],
          "lengths": [8, 4, 4, 4, 4]},

    "h": {"fields": ["stock", "marketCode", "operationalHaltAction"],
          "lengths": [8, 1, 1]},

    "A": {"fields": ["orderReferenceNumber", "buySellIndicator", "shares", "stock", "price"],
          "lengths": [8, 1, 4, 8, 4]},

    "F": {"fields": ["orderReferenceNumber", "buySellIndicator", "shares", "stock",
                     "price", "attribution"],
          "lengths": [8, 1, 4, 8, 4, 4]},

    "E": {"fields": ["orderReferenceNumber", "executedShares", "matchNumber"],
          "lengths": [8, 4, 8]},

    "C": {"fields": ["orderReferenceNumber", "executedShares", "matchNumber",
                     "printable", "executionPrice"],
          "lengths": [8, 4, 8, 1, 4]},

    "X": {"fields": ["orderReferenceNumber", "cancelledShares"],
          "lengths": [8, 4]},

    "D": {"fields": ["orderReferenceNumber"],
          "lengths": [8]},

    "U": {"fields": ["originalOrderReferenceNumber", "newOrderReferenceNumber",
                     "shares", "price"],
          "lengths": [8, 8, 4, 4]},

    "P": {"fields": ["orderReferenceNumber", "buySellIndicator", "shares", "stock",
                     "price", "matchNumber"],
          "lengths": [8, 1, 4, 8, 4, 8]},

    "Q": {"fields": ["shares", "stock", "crossPrice", "matchNumber", "crossType"],
          "lengths": [8, 8, 4, 8, 1]},

    "B": {"fields": ["matchNumber"],
          "lengths": [8]},

    "I": {"fields": ["pairedShares", "imbalanceShares", "imbalanceDirection", "stock",
                     "farPrice", "nearPrice", "currentReferencePrice", "crossType",
                     "priceVariationIndicator"],
          "lengths": [8, 8, 1, 8, 4, 4, 4, 1, 1]},

    "N": {"fields": ["stock", "interestFlag"],
          "lengths": [8, 1]},

    "O": {"fields": ["stock", "openEligibilityStatus", "minimumAllowablePrice",
                     "maximumAllowablePrice", "nearExecutionPrice", "nearExecutionTime",
                     "lowerPriceRangeCollar", "upperPriceRangeCollar"],
          "lengths": [8, 1, 4, 4, 4, 8, 4, 4]},
}
COMMON_FIELDS = ["messageType", "stockLocate", "trackingNumber", "timestamp"]
COMMON_LENGTHS = [1, 2, 2, 6]

# Checks all dictionaries and arrays declared above to ensure they are consistent with each other.
for t, shape in type_to_shape.items():
    assert len(shape["fields"]) == len(shape["lengths"]), f"{t}: fields and lengths differ in count"
    assert 11 + sum(shape["lengths"]) == type_to_length[t], f"{t}: lengths sum to wrong total"

names = set(COMMON_FIELDS)
for shape in type_to_shape.values():
    names.update(shape["fields"])
assert names == set(ALL_FIELDS), f"mismatch: {names ^ set(ALL_FIELDS)}"




def parse(msg_in):
    # Requires a full ITCH 5 message, which is to be parsed fully.
    # 'msg_in' input must be provided as a string to be processed correctly. (Python cannot natively store hexadecimal numbers)
    length_prefix = int(msg_in[0:4], 16) # Extracts length prefix from message
    type = chr(int(msg_in[4:6], 16)) # Extracts type from message and converts into charecter

    # Error Handling
    if len(msg_in) % 2 != 0:
        raise illegalLengthError
    if (len(msg_in) / 2 - 2) != length_prefix:
        raise incompleteMessageError
    try:
        length = type_to_length[type]
    except KeyError:
        return "illegalType"
    if length != length_prefix:
        return "lengthMismatch"


    index = 4
    msg = Message()
    fields = COMMON_FIELDS + type_to_shape[type]["fields"]
    lengths = COMMON_LENGTHS + type_to_shape[type]["lengths"]

    for field in range(0, len(fields)):
        data = msg_in[index:index + 2*lengths[field]]
        setattr(msg, fields[field], int(data,16))
        index += 2*lengths[field]
    return msg
