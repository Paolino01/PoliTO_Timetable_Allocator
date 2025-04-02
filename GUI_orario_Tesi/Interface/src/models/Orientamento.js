import CorsoDiLaurea from './CorsoDiLaurea'

 class Orientamento {
  /**
   * Creates an Orientamento (Orientation)
   * @param {String} orientamento 
   * @param {CorsoDiLaurea} corsoDiLaurea
  */
  constructor(orientamento, corsoDiLaurea) {
    this.orientamento = orientamento
    this.corsoDiLaurea = corsoDiLaurea
  }

  /**
   * Construct an Orientamento (Orientation) from a plain object
   * @param {{}} json 
   * @return {Orientamento} the newly created Orientamento (Orientation) object
   */
  static from(json) {
    return new Orientamento(json.orientamento, json.corsoDiLaurea);
  }
}

export default Orientamento;