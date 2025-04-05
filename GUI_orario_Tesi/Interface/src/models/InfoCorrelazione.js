 class InfoCorrelazione {
  /**
   * Creates a InfoCorrelazione (Correlation Info)
   * @param {Number} ID_INC_1
   * @param {Number} ID_INC_2
   * @param {Number} correlazione
  */
  constructor(id1, id2, corr) {
      this.ID_INC_1 = id1
      this.ID_INC_2 = id2
      this.correlazione = corr
  }

  /**
   * Construct an Slot from a plain object
   * @param {{}} json 
   * @return {InfoCorrelazione} the newly created Slot object
   */
    static from(json) {
      return new InfoCorrelazione(json.ID_INC_1, json.ID_INC_2, json.correlazione);
    }
}

export default InfoCorrelazione;