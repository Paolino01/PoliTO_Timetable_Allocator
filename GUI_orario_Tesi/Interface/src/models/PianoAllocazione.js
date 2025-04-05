 class PianoAllocazione {
  /**
   * Creates a PianoAllocazione (AllocationPlan)
   * @param {String} pianoAllocazione 
  */
  constructor(pianoAllocazione) {
    this.pianoAllocazione = pianoAllocazione
  }

  /**
   * Construct a PianoAllocazione (AllocationPlan) from a plain object
   * @param {{}} json 
   * @return {PianoAllocazione} the newly created PianoAllocazione (AllocationPlan) object
   */
  static from(json) {
    return new PianoAllocazione(json.pianoAllocazione);
  }
}

export default PianoAllocazione;