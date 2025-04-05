 class Docente {
  /**
   * Creates a Docente (teacher)
   * @param {String} Cognome 
  */
  constructor(Cognome) {
    this.Cognome = Cognome
  }

  /**
   * Construct a Docente (teacher) from a plain object
   * @param {{}} json 
   * @return {Docente} the newly created Docente (teacher) object
   */
  static from(json) {
    return new Docente(json.Cognome);
  }
}

export default Docente;