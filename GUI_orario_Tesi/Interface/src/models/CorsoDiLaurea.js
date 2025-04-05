
 class CorsoDiLaurea {
  /**
   * Creates a CorsoDiLaurea (Degree course)
   * @param {String} tipoCdl 
   * @param {String} nomeCdl
  */
  constructor(tipoCdl, nomeCdl) {
    this.tipoCdl = tipoCdl
    this.nomeCdl = nomeCdl
  }

  /**
   * Construct a CorsoDiLaurea (Degree course) from a plain object
   * @param {{}} json 
   * @return {CorsoDiLaurea} the newly created Exam object
   */
  static from(json) {
    return new CorsoDiLaurea(json.tipoCdl, json.nomeCdl);
  }
}

export default CorsoDiLaurea;