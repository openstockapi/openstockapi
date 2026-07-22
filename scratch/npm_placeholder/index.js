module.exports = {
  init: (apiKey) => {
    console.log("OpenStockAPI JS Client initialized (Placeholder)");
    return {
      ohlcv: async () => {
        throw new Error("JS SDK is under construction. Please use the Python package 'openstockapi' in the meantime.");
      }
    };
  }
};
