import Docente from './Docente'


 class Insegnamento {
  /**
   * Creates an Insegnamento (Teaching)
   * @param {Number} ID_INC 
   * @param {Number} nStudenti
   * @param {Number} nStudentiFreq
   * @param {String} collegio
   * @param {String} titolo
   * @param {String} CFU
   * @param {Number} oreLez
   * @param {Docente} titolare
  */
  constructor(ID_INC, nStudenti, nStudentiFreq, collegio, titolo, CFU, oreLez, titolare) {
    this.ID_INC = ID_INC
    this.nStudenti = nStudenti
    this.nStudentiFreq = nStudentiFreq
    this.collegio = collegio
    this.titolo = titolo
    this.CFU = CFU
    this.oreLez = oreLez
    this.titolare = titolare
    // To specify the orientation
    this.orientamento = null
    this.tipoInsegnamento = null
    this.periodoDidattico = null
    this.nStudentiOrientamento = null
    this.alfabetica = null
  }

  setOrientamento(orientamento, tipoInsegnamento, periodoDidattico, nStudentiOrientamento, alfabetica){
    this.orientamento = orientamento;
    this.tipoInsegnamento = tipoInsegnamento;
    this.periodoDidattico = periodoDidattico;
    this.nStudentiOrientamento = nStudentiOrientamento;
    this.alfabetica = alfabetica;
    return this;
  }

  /**
   * Construct an Insegnamento (Teaching) from a plain object
   * @param {{}} json 
   * @return {Insegnamento} the newly created Insegnamento (Teaching) object
   */
  static from(json) {
    return new Insegnamento(json.ID_INC, json.nStudenti, json.nStudentiFreq, json.collegio, json.titolo, json.CFU,
        json.oreLez, json.titolare);
  }
}

export default Insegnamento;