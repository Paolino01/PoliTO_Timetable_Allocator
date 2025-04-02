/**
 * All the API calls
 */
import CorsoDiLaurea from "./models/CorsoDiLaurea";
import Docente from "./models/Docente";
import Insegnamento from "./models/Insegnamento"
import Orientamento from "./models/Orientamento";
import PianoAllocazione from "./models/PianoAllocazione";
import Slot from "./models/Slot"
import InfoCorrelazione from "./models/InfoCorrelazione";

const BASEURL = '/api';

async function get_Insegnamenti() {
  // GET /api/insegnamenti
  const response = await fetch(BASEURL + "/insegnamenti");
  const insegnamentiJson = await response.json();
  if (response.ok) {
    return insegnamentiJson.map((ins) => Insegnamento.from(ins));
  } else {
    throw insegnamentiJson;
  }
}

async function get_PianoAllocazione() {
  // GET /api/pianoAllocazione
  const response = await fetch(BASEURL + "/pianoAllocazione");
  const pianiAllocJson = await response.json();
  if (response.ok) {
    return pianiAllocJson.map((piano) => PianoAllocazione.from(piano));
  } else {
    throw pianiAllocJson;
  }
}

async function get_slots_pianoAllocazione(pianoAllocazione) {
  // GET /api/pianoAllocazione/:pianoAllocazione
  const response = await fetch(BASEURL + "/pianoAllocazione/" + pianoAllocazione);
  const slotsJson = await response.json();
  if (response.ok) {
    let listSlot = [];
    let prevSlotId = "";
    
    for (let slot of slotsJson) {
      let currSlotId = slot.idSlot;

      if (currSlotId != prevSlotId) {
        listSlot.push(Slot.from(slot).setInsegnamento(Insegnamento.from(slot)));
      }
      listSlot[listSlot.length - 1].addDocente(slot.Cognome);
      prevSlotId = currSlotId;
    }
    return listSlot;
  } else {
    throw slotsJson;
  }
}

async function get_pianoAllocazioneDocente(pianoAllocazione, docente) {
  // GET /api/pianoAllocazione/:pianoAllocazione/:docente
  const response = await fetch(BASEURL + "/pianoAllocazione/" + pianoAllocazione + "/" + docente);
  const slotsJson = await response.json();
  if (response.ok) {
    let listSlot = [];
    let prevSlotId = "";
    
    for (let slot of slotsJson) {
      let currSlotId = slot.idSlot;

      if (currSlotId != prevSlotId) {
        listSlot.push(Slot.from(slot).setInsegnamento(Insegnamento.from(slot)));
      }
      listSlot[listSlot.length - 1].addDocente(slot.Cognome);
      prevSlotId = currSlotId;
    }
    return listSlot;
  } else {
    throw slotsJson;
  }
}

async function get_docenti() {
  // GET /api/docenti
  const response = await fetch(BASEURL + "/docenti");
  const docentiJson = await response.json();
  if (response.ok) {
    return docentiJson.map((doc) => Docente.from(doc));
  } else {
    throw docentiJson;
  }
}

async function get_pianoAllocazioneID_INC_withDocenti(pianoAllocazione, ID_INC) {
  // GET /api/pianoAllocazione/:pianoAllocazione/:ID_INC
  const response = await fetch(BASEURL + "/pianoAllocazione/" + pianoAllocazione + "/" + ID_INC);
  const slotsJson = await response.json();
  if (response.ok) {
    let listSlot = [];

    let prevSlotId = "";
    for (let slot of slotsJson) {
      let currSlotId = slot.idSlot;

      if (currSlotId != prevSlotId) {
        listSlot.push(Slot.from(slot));
      }
      listSlot[listSlot.length - 1].addDocente(slot.Cognome);
      prevSlotId = currSlotId;
    }
    return listSlot;
  } else {
    throw slotsJson;
  }
}

async function get_pianoAllocazioneOrientamento_withDocenti(pianoAllocazione, tipoCdl, nomeCdl, orientamento, periodoDidattico) {
  // GET /api/pianoAllocazione/:pianoAllocazione/:tipoCdl/:nomeCdl/:orientamento/:periodoDidattico
  const response = await fetch(BASEURL + "/pianoAllocazione/" + pianoAllocazione + "/" + tipoCdl + "/" + nomeCdl + "/" + orientamento + "/" + periodoDidattico);
  const slotsJson = await response.json();
  if (response.ok) {
    let listSlot = [];

    let prevSlotId = "";
    for (let slot of slotsJson) {
      let currSlotId = slot.idSlot;

      if (currSlotId != prevSlotId) {
        listSlot.push(Slot.from(slot)
          .setInsegnamento(Insegnamento.from(slot)
            .setOrientamento(
              new Orientamento(orientamento, new CorsoDiLaurea(tipoCdl, nomeCdl)),
              slot.tipoInsegnamento, periodoDidattico, slot.nStudentiOrient, slot.alfabetica
            )));
      }
      listSlot[listSlot.length - 1].addDocente(slot.Cognome);
      prevSlotId = currSlotId;
    }
    return listSlot;
  } else {
    throw slotsJson;
  }
}

async function get_corsiDiLaurea() {
  // GET /api/corsiDiLaurea
  const response = await fetch(BASEURL + "/corsiDiLaurea");
  const cdlJson = await response.json();
  if (response.ok) {
    return cdlJson.map((cdl) => CorsoDiLaurea.from(cdl));
  } else {
    throw cdlJson;
  }
}

async function get_corsiDiLaurea_withTipoCdl(tipoCdl) {
  // GET /api/corsiDiLaurea/:tipoCdl
  const response = await fetch(BASEURL + "/corsiDiLaurea/" + tipoCdl);
  const cdlJson = await response.json();
  if (response.ok) {
    return cdlJson.map((cdl) => CorsoDiLaurea.from(cdl));
  } else {
    throw cdlJson;
  }
}

async function get_Orientamenti() {
  // GET /api/orientamenti
  const response = await fetch(BASEURL + "/orientamenti");
  const orientsJson = await response.json();
  if (response.ok) {
    return orientsJson.map((orient) => Orientamento.from(orient));
  } else {
    throw orientsJson;
  }
}

async function get_Orientamenti_Cdl(nomeCdl, tipoCdl) {
  // GET /api/orientamenti/:tipoCdl/:nomeCdl
  const response = await fetch(BASEURL + "/orientamenti/" + tipoCdl + "/" + nomeCdl);
  const orientsJson = await response.json();
  if (response.ok) {
    return orientsJson.map((orient) => Orientamento.from(orient));
  } else {
    throw orientsJson;
  }
}

async function get_Insegnamenti_withOrientamento(orientamento, nomeCdl, tipoCdl) {
  // GET /api/insegnamenti/:tipoCdl/:nomeCdl/:orientamento
  const response = await fetch(BASEURL + "/insegnamenti/" + tipoCdl + "/" + nomeCdl + "/" + orientamento);
  const insJson = await response.json();
  if (response.ok) {
    return insJson.map((ins) => Insegnamento.from(ins).setOrientamento(new Orientamento(orientamento, new CorsoDiLaurea(tipoCdl, nomeCdl)),
      ins.tipoInsegnamento, ins.periodoDidattico, ins.nStudentiOrient, ins.alfabetica));
  } else {
    throw insJson;
  }
}

async function get_fasceOrarie() {
  // GET /api/fasceOrarie
  const response = await fetch(BASEURL + "/fasceOrarie");
  console.log(response)
  const fasceJson = await response.json();
  if (response.ok) {
    return fasceJson.map((fascia) => String(fascia.fasciaOraria));
  } else {
    throw fasceJson;
  }
}

async function get_giorni() {
  // GET /api/giorni
  const response = await fetch(BASEURL + "/giorni");
  const giorniJson = await response.json();
  if (response.ok) {
    return giorniJson.map((giorno) => String(giorno.giorno));
  } else {
    throw giorniJson;
  }
}

async function get_infoCorrelazioni() {
  const response = await fetch(BASEURL + "/sovrapposizioni");
  console.log(response)
  if (response.ok) {
    const infoCorrJson = await response.json();
    return infoCorrJson.map((infoCorrRow) => InfoCorrelazione.from(infoCorrRow));
  } else {
    console.log("Response is not ok")
    throw Error;
  }
}

const API = {
  get_Insegnamenti, get_PianoAllocazione, get_pianoAllocazioneID_INC_withDocenti, get_Insegnamenti_withOrientamento,
  get_corsiDiLaurea, get_Orientamenti, get_Orientamenti_Cdl, get_corsiDiLaurea_withTipoCdl, get_pianoAllocazioneOrientamento_withDocenti,
  get_fasceOrarie, get_giorni, get_pianoAllocazioneDocente, get_docenti, get_infoCorrelazioni, get_slots_pianoAllocazione,
};
export default API;
