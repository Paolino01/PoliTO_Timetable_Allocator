import Insegnamento from "./Insegnamento"
import Orientamento from "./Orientamento"

 class InsegnamentoInOrientamento {
  /**
   * Creates an InsegnamentoInOrientamento (Teaching Orientation)
   * @param {Insegnamento} insegnamento 
   * @param {Orientamento} orientamento
   * @param {String} tipoInsegnamento
   * @param {String} periodoDidattico
   * @param {Number} nStudenti
   * @param {String} alfabetica
  */
  constructor(insegnamento, orientamento, tipoInsegnamento,periodoDidattico, nStudenti, alfabetica) {  
    this.insegnamento = insegnamento
    this.orientamento = orientamento
    this.tipoInsegnamento = tipoInsegnamento
    this.periodoDidattico = periodoDidattico
    this.nStudenti = nStudenti
    this.alfabetica = alfabetica
  }

  /**
   * Construct an InsegnamentoInOrientamento (TeachingOrientation) from a plain object
   * @param {{}} json 
   * @return {InsegnamentoInOrientamento} the newly created InsegnamentoInOrientamento (TeachingOrientation) object
   */
  static from(json) {
    return new InsegnamentoInOrientamento(json.insegnamento, json.orientamento, json.tipoInsegnamento, 
      json.periodoDidattico, json.nStudenti, json.alfabetica);
  }
}

export default InsegnamentoInOrientamento;