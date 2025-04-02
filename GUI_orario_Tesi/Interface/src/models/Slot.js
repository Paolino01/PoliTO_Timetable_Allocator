import Insegnamento from './Insegnamento'
import PianoAllocazione from './PianoAllocazione'

 class Slot {
  /**
   * Creates a Slot
   * @param {PianoAllocazione} pianoAllocazione
   * @param {String} idSlot
   * @param {Number} nStudentiAssegnati
   * @param {String} tipoLez
   * @param {Number} numSlotConsecutivi
   * @param {Number} ID_INC
   * @param {String} giorno
   * @param {String} fasciaOraria
   * @param {String} tipoLocale
   * @param {String} tipoErogazione
  */
  constructor(pianoAllocazione, idSlot, nStudentiAssegnati, tipoLez, numSlotConsecutivi, ID_INC, giorno, fasciaOraria,
    tipoLocale, tipoErogazione) {
      this.pianoAllocazione = pianoAllocazione
      this.idSlot = idSlot
      this.nStudentiAssegnati = nStudentiAssegnati
      this.tipoLez = tipoLez
      this.numSlotConsecutivi = numSlotConsecutivi
      this.ID_INC = ID_INC
      this.giorno = giorno
      this.fasciaOraria = fasciaOraria
      this.tipoLocale = tipoLocale
      this.tipoErogazione = tipoErogazione
      this.listDocenti = []
      this.insegnamento = null
  }

  addDocente(docente) {
    if(!this.listDocenti.includes(docente))
      this.listDocenti.push(docente);
  }

  setInsegnamento(insegnamento){
    this.insegnamento = insegnamento;
    return this;
  }

  // Expands the Slot for every time slots that compose it
  expandSlot(){
    if(this.numSlotConsecutivi === 1)
      return [this];

    const LIST_FASCE = ["8.30-10.00","10.00-11.30","11.30-13.00","13.00-14.30","14.30-16.00","16.00-17.30","17.30-19.00"];
    let listRes = [];
    for(let i=0;i<this.numSlotConsecutivi;i++) {
      listRes.push(Slot.copySlot_fasciaOrariaCustom(this, LIST_FASCE[LIST_FASCE.indexOf(this.fasciaOraria)+i]));
    }
    return listRes;
  }

  static copySlot_fasciaOrariaCustom(slot, fasciaOraria){
    const slotRes = new Slot(slot.pianoAllocazione, slot.idSlot, slot.nStudentiAssegnati, slot.tipoLez, 1, slot.ID_INC, slot.giorno,
      fasciaOraria, slot.tipoLocale, slot.tipoErogazione);
    slot.listDocenti.forEach((doc) => slotRes.addDocente(doc));
    return slotRes.setInsegnamento(slot.insegnamento);
  }

  /**
   * Construct a Slot from a plain object
   * @param {{}} json 
   * @return {Slot} the newly created Slot object
   */
  static from(json) {
    return new Slot(json.pianoAllocazione, json.idSlot, json.nStudentiAssegnati, json.tipoLez, json.numSlotConsecutivi,
      json.ID_INC, json.giorno, json.fasciaOraria, json.tipoLocale, json.tipoErogazione);
  }
}

export default Slot;