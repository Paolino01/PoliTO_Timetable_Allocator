import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import { Container, Row, Alert, Col } from 'react-bootstrap';
import { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

import Navigation from './Navigation.js';
import InsegnamentiComponent from './components/InsegnamentiComponent.js';
import OrarioComponent from './components/OrarioComponent.js';
import API from './API.js'
import DocentiComponent from './components/DocentiComponent';
import SovrapposizioniComponent from './components/SovrapposizioniComponent.js';
import DifferenzeComponent from './components/DifferenzeComponent.js';


const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds));
}
const EMPTY_VALUE = "sconosciuto";

function App() {
  const [loading, setLoading] = useState(true);
  const [dirty, setDirty] = useState(true);
  const [moving, setMoving] = useState(0);
  const [fasceOrarie, setFasceOrarie] = useState([]);
  const [giorni, setGiorni] = useState(["Lun", "Mar", "Mer", "Gio", "Ven"]);

  const [tipoCdl, setTipoCdl] = useState(EMPTY_VALUE);
  const [listCdl, setListCdl] = useState([]);
  const [currCdl, setCurrCdl] = useState(listCdl.length > 0 ? listCdl[0].nomeCdl : EMPTY_VALUE);
  const [listOrientamenti, setListOrientamenti] = useState([]);
  const [currOrientamento, setCurrOrientamento] = useState(listOrientamenti.length > 0 ? listOrientamenti[0].orientamento : EMPTY_VALUE);
  const [listInsegnamenti, setListInsegnamenti] = useState([]);
  const [fullListInsegnamenti, setFullListInsegnamenti] = useState([]);
  const [currInsegnamento, setCurrInsegnamento] = useState(listInsegnamenti.length > 0 ? listInsegnamenti[0] : EMPTY_VALUE);
  const [periodoDidattico, setPeriodoDidattico] = useState(EMPTY_VALUE);

  const [listPianiAllocazione, setListPianiAllocazione] = useState([]);
  const [currPianoAllocazione, setCurrPianoAllocazione] = useState(listPianiAllocazione.length > 0 ? listPianiAllocazione[0].pianoAllocazione : EMPTY_VALUE);
  const [listSlot, setListSlot] = useState([]);
  const [listSlotOtherTimetable, setListSlotOtherTimetable] = useState([]);
  const [fullListSlot, setFullListSlot] = useState([])
  const [listInfoCorr, setListInfoCorr] = useState([]);
  const [listDocenti, setListDocenti] = useState([]);
  const [currDocente, setCurrDocente] = useState(listDocenti.length > 0 ? listDocenti[0].Cognome : EMPTY_VALUE);


  const _setTipoCdl = (_tipoCdl) => {
    setTipoCdl(_tipoCdl);
    setCurrCdl(EMPTY_VALUE);
    setCurrOrientamento(EMPTY_VALUE);
    setPeriodoDidattico(EMPTY_VALUE);
    setCurrDocente(EMPTY_VALUE);
    setCurrInsegnamento(EMPTY_VALUE);
    setDirty(true);
  }
  const _setCurrCdl = (_currCdl) => {
    setCurrCdl(_currCdl);
    setCurrOrientamento(EMPTY_VALUE);
    setPeriodoDidattico(EMPTY_VALUE);
    setCurrDocente(EMPTY_VALUE);
    setCurrInsegnamento(EMPTY_VALUE);
    setDirty(true);
  }
  const _setPeriodoDidattico = (_periodoDidattico) => {
    setPeriodoDidattico(_periodoDidattico);
    setCurrDocente(EMPTY_VALUE);
    setCurrInsegnamento(EMPTY_VALUE);
    setDirty(true);
  }
  const _setCurrOrientamento = (_currOrient) => {
    setCurrOrientamento(_currOrient);
    setCurrDocente(EMPTY_VALUE);
    setPeriodoDidattico(EMPTY_VALUE);
    setCurrDocente(EMPTY_VALUE);
    setCurrInsegnamento(EMPTY_VALUE);
    setDirty(true);
  }
  const _setCurrPianoAllocazione = (_currPiano) => {
    setCurrPianoAllocazione(_currPiano);
    setTipoCdl(EMPTY_VALUE);
    setCurrCdl(EMPTY_VALUE);
    setCurrOrientamento(EMPTY_VALUE);
    setPeriodoDidattico(EMPTY_VALUE);
    setCurrDocente(EMPTY_VALUE);
    setCurrInsegnamento(EMPTY_VALUE);
    setDirty(true);
  }
  const _setCurrDocente = (_currDocente) => {
    setCurrDocente(_currDocente);
    setTipoCdl(EMPTY_VALUE);
    setCurrCdl(EMPTY_VALUE);
    setCurrOrientamento(EMPTY_VALUE);
    setPeriodoDidattico(EMPTY_VALUE);
    setDirty(true);
  }

  const _setCurrInsegnamento =  (_currInsegnamento) => {
    setCurrInsegnamento(_currInsegnamento);
    setCurrDocente(EMPTY_VALUE);
    setDirty(true);
  }


  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setFasceOrarie(await API.get_fasceOrarie());
      setListInfoCorr(await API.get_infoCorrelazioni());
      setFullListInsegnamenti(await API.get_Insegnamenti());
      // setGiorni(await API.get_giorni()); non li carica in ordine
      setLoading(false);
    }
    load(); // called once
  }, []);



  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setListCdl(await API.get_corsiDiLaurea_withTipoCdl(tipoCdl));
      setLoading(false);
      setDirty(false);
    }
    if (dirty && tipoCdl !== EMPTY_VALUE) {
      load();
    }else if(dirty){
      setListCdl([]);
    }
  }, [moving, tipoCdl]);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setListOrientamenti(await API.get_Orientamenti_Cdl(currCdl, tipoCdl));
      setLoading(false);
      setDirty(false);
    }
    if (dirty && currCdl != EMPTY_VALUE && tipoCdl != EMPTY_VALUE) {
      load();
    } else if (dirty) {
      setListOrientamenti([]);
      setDirty(false);
    }
  }, [moving, currCdl, tipoCdl]);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setListInsegnamenti(await API.get_Insegnamenti_withOrientamento(currOrientamento, currCdl, tipoCdl));
      setLoading(false);
      setDirty(false);
    }
    if (dirty && currCdl != EMPTY_VALUE && tipoCdl != EMPTY_VALUE && currOrientamento != EMPTY_VALUE) {
      load();
    } else if (dirty) {
      setListInsegnamenti([]);
      setDirty(false);
    }
  }, [moving, currCdl, tipoCdl, currOrientamento]);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setListPianiAllocazione(await API.get_PianoAllocazione());
      setListDocenti(await API.get_docenti());
      setLoading(false);
      setDirty(false);
    }
    if (dirty) {
      load();
    }
  }, [moving])

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      let _listSlot = await API.get_pianoAllocazioneOrientamento_withDocenti(currPianoAllocazione, tipoCdl, currCdl, currOrientamento, periodoDidattico);
      let _listSlotOtherTimetable = await API.get_other_timetable(tipoCdl, currCdl, currOrientamento, periodoDidattico);
      let _fullListSlot = await API.get_slots_pianoAllocazione(currPianoAllocazione)
      setListSlot(_listSlot.map((slot) => slot.expandSlot()).flat());
      console.log(_listSlotOtherTimetable)
      setListSlotOtherTimetable(_listSlotOtherTimetable.map((slot) => slot).flat());
      setFullListSlot(_fullListSlot.map((slot) => slot.expandSlot()).flat())
      setLoading(false);
      setDirty(false);
    }
    const load1 = async () => {
      setLoading(true);
      let _listSlot = await API.get_pianoAllocazioneDocente(currPianoAllocazione, currDocente);
      setListSlot(_listSlot.map((slot) => slot.expandSlot()).flat());
      setLoading(false);
      setDirty(false);
    }
    if (dirty && currPianoAllocazione !== EMPTY_VALUE && tipoCdl !== EMPTY_VALUE && currCdl !== EMPTY_VALUE && currOrientamento !== EMPTY_VALUE
      && periodoDidattico !== EMPTY_VALUE && currDocente === EMPTY_VALUE) {
      load();
    } else if (dirty && currPianoAllocazione !== EMPTY_VALUE && tipoCdl === EMPTY_VALUE && currCdl === EMPTY_VALUE &&
      currOrientamento === EMPTY_VALUE && periodoDidattico === EMPTY_VALUE && currDocente !== EMPTY_VALUE) {
      load1();
    } else if (dirty) {
      setListSlot([]);
    }

  }, [moving, currPianoAllocazione, currCdl, currOrientamento, tipoCdl, periodoDidattico, currDocente])


  return (<Router>
    <Navigation setMoving={setMoving}></Navigation>
    <Container fluid className='pl-0'>
      <Switch>

        <Route path="/insegnamenti">
          <InsegnamentiComponent loading={loading} listCdl={listCdl} tipoCdl={tipoCdl} setTipoCdl={_setTipoCdl} currCdl={currCdl}
            setCurrCdl={_setCurrCdl} currOrientamento={currOrientamento} listOrientamenti={listOrientamenti} listInsegnamenti={listInsegnamenti}
            setCurrOrientamento={_setCurrOrientamento} periodoDidattico={periodoDidattico} setPeriodoDidattico={_setPeriodoDidattico} />
        </Route>

        <Route path="/pianoAllocazione">
          <OrarioComponent loading={loading} listCdl={listCdl} tipoCdl={tipoCdl} setTipoCdl={_setTipoCdl} currCdl={currCdl}
            setCurrCdl={_setCurrCdl} currOrientamento={currOrientamento} listOrientamenti={listOrientamenti}
            setCurrOrientamento={_setCurrOrientamento} periodoDidattico={periodoDidattico} setPeriodoDidattico={_setPeriodoDidattico}
            listSlot={listSlot} listPianiAllocazione={listPianiAllocazione} currPianoAllocazione={currPianoAllocazione}
            setCurrPianoAllocazione={_setCurrPianoAllocazione} fasceOrarie={fasceOrarie} giorni={giorni} />
        </Route>

        <Route path="/docenti">
          <DocentiComponent loading={loading} listSlot={listSlot} listPianiAllocazione={listPianiAllocazione} 
            currPianoAllocazione={currPianoAllocazione} setCurrPianoAllocazione={_setCurrPianoAllocazione}
            currDocente={currDocente} setCurrDocente={_setCurrDocente} listDocenti={listDocenti}
            fasceOrarie={fasceOrarie} giorni={giorni} />
        </Route>

        <Route path="/sovrapposizioni">
          <SovrapposizioniComponent loading={loading} listCdl={listCdl} tipoCdl={tipoCdl} setTipoCdl={_setTipoCdl} currCdl={currCdl}
            setCurrCdl={_setCurrCdl} currOrientamento={currOrientamento} listOrientamenti={listOrientamenti}
            setCurrOrientamento={_setCurrOrientamento} periodoDidattico={periodoDidattico} setPeriodoDidattico={_setPeriodoDidattico}
            listSlot={listSlot} listPianiAllocazione={listPianiAllocazione} currPianoAllocazione={currPianoAllocazione}
            setCurrPianoAllocazione={_setCurrPianoAllocazione} fasceOrarie={fasceOrarie} giorni={giorni} 
            listInsegnamenti={listInsegnamenti.filter((ins) => ins.periodoDidattico === periodoDidattico)} currInsegnamento={currInsegnamento} setCurrInsegnamento={_setCurrInsegnamento}
            listInfoCorr={listInfoCorr} fullListSlot={fullListSlot } fullListInsegnamenti={fullListInsegnamenti}/>
        </Route>

        <Route path="/differenze_orario">
          <DifferenzeComponent loading={loading} listCdl={listCdl} tipoCdl={tipoCdl} setTipoCdl={_setTipoCdl} currCdl={currCdl}
            setCurrCdl={_setCurrCdl} currOrientamento={currOrientamento} listOrientamenti={listOrientamenti}
            setCurrOrientamento={_setCurrOrientamento} periodoDidattico={periodoDidattico} setPeriodoDidattico={_setPeriodoDidattico}
            listSlot={listSlot} listSlotOtherTimetable={listSlotOtherTimetable} listPianiAllocazione={listPianiAllocazione} currPianoAllocazione={currPianoAllocazione}
            setCurrPianoAllocazione={_setCurrPianoAllocazione} fasceOrarie={fasceOrarie} giorni={giorni} 
            listInsegnamenti={listInsegnamenti.filter((ins) => ins.periodoDidattico === periodoDidattico)} currInsegnamento={currInsegnamento} setCurrInsegnamento={_setCurrInsegnamento}
            listInfoCorr={listInfoCorr} fullListSlot={fullListSlot } fullListInsegnamenti={fullListInsegnamenti}/>
        </Route>

        <Route path="/" render={() =>
          <Row>
            {loading ? <span>🕗 Please wait, loading... 🕗</span> : <></>
            }
          </Row>
        } />
      </Switch>

    </Container>
  </Router>);
}

export default App;
