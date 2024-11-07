export const ForceCastValueMap = {
  default: "No Change",
  uint: "Unsigned Integer",
  int: "Signed Integer",
  float: "Floating Point",
  category: "Category",
  complex: "Complex Number",
  object: "Text",
  datetime: "Date and Time",
};

export const NumberOptionsByValue = {
  uint: {
    uint8: "8 bits",
    uint16: "16 bits",
    uint32: "32 bits",
    // uint64: "64 bits", // Cannot use uint64 because sqlite3's biggest uint reaches 2**63
  },
  int: {
    int8: "8 bits",
    int16: "16 bits",
    int32: "32 bits",
    int64: "64 bits",
  },
  float: {
    float32: "32 bits",
    float64: "64 bits",
  },
};
