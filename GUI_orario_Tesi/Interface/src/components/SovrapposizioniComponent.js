import { Row, Table, Dropdown, Container, Col, Badge, Popover, OverlayTrigger, Tooltip } from 'react-bootstrap';

const EMPTY_VALUE = "sconosciuto";
const LEN_TITOLO = 18;

function Slot(props) {
    const { slot, giorno } = props;
  
    // console.log(slot)
    const strDoc = slot.listDocenti.reduce((prev, doc) => prev.concat(", ", doc));
  
    const popover = (
      <Popover>
        <Popover.Title as='h6'>{slot.insegnamento.titolo + (slot.insegnamento.alfabetica !== "0" ? " - alf" + String(slot.insegnamento.alfabetica) : "")}
        </Popover.Title>
        <Popover.Content>
          {"Docenti: " + strDoc}<br></br>
          {"Studenti: " + slot.insegnamento.nStudentiFreq}<br></br>
          {"Tipo lezione: " + slot.tipoLez}<br></br>
          {slot.tipoErogazione === "Presenza" ? "Tipo locale: " + slot.tipoLocale : "Erogazione in remoto"}
        </Popover.Content>
      </Popover>
    );
  
    if (slot.insegnamento.tipoInsegnamento === "Obbligatorio" || slot.insegnamento.tipoInsegnamento === "Obbligatorio_a_scelta") {
      return (
        <OverlayTrigger placement={giorno !== 'Ven' ? 'right' : 'left'} trigger='click' delay={{ show: 250, hide: 300 }} overlay={popover}>
          <Badge className='bg-danger text-light'>
            {(slot.insegnamento.titolo.length > LEN_TITOLO ? slot.insegnamento.titolo.substring(0, LEN_TITOLO) : slot.insegnamento.titolo) + " " + slot.idSlot}
          </Badge>
        </OverlayTrigger>
      )
    }
    if (slot.insegnamento.tipoInsegnamento === "Tabella_a_scelta") {
      return (
        <OverlayTrigger placement={giorno !== 'Ven' ? 'right' : 'left'} trigger='click' delay={{ show: 250, hide: 300 }} overlay={popover}>
          <Badge className='bg-warning text-dark'>
            {(slot.insegnamento.titolo.length > LEN_TITOLO ? slot.insegnamento.titolo.substring(0, LEN_TITOLO) : slot.insegnamento.titolo) + " " + slot.idSlot}
          </Badge>
        </OverlayTrigger>
      )
    }
    if (slot.insegnamento.tipoInsegnamento === "Credito_libero") {
      return (
        <OverlayTrigger placement={giorno !== 'Ven' ? 'right' : 'left'} trigger='click' delay={{ show: 250, hide: 300 }} overlay={popover}>
          <Badge className='bg-success text-light'>
            {(slot.insegnamento.titolo.length > LEN_TITOLO ? slot.insegnamento.titolo.substring(0, LEN_TITOLO) : slot.insegnamento.titolo) + " " + slot.idSlot}
          </Badge>
        </OverlayTrigger>
      )
    }
    if (slot.insegnamento.tipoInsegnamento === "Sconosciuto") {
      return (
        <OverlayTrigger placement={giorno !== 'Ven' ? 'right' : 'left'} trigger='click' delay={{ show: 250, hide: 300 }} overlay={popover}>
          <Badge className='bg-success text-light'>
            {(slot.insegnamento.titolo.length > LEN_TITOLO ? slot.insegnamento.titolo.substring(0, LEN_TITOLO) : slot.insegnamento.titolo) + " " + slot.idSlot}
          </Badge>
        </OverlayTrigger>
      )
    }
    return (
      <></>
    )
  }
  
  function SlotMerged(props) {
    const { slots, giorno } = props;
  
    return (
      <td>
        {slots.map((slot) => <Slot slot={slot} giorno={giorno}></Slot>)}
      </td>
    )
  }
  
  
  function SlotsFasciaOraria(props) {
    const { slots, giorni } = props;
  
    return (
      <>
        {giorni.map((giorno) => <SlotMerged slots={slots.hasOwnProperty(giorno) ? slots[giorno] : []} giorno={giorno} />)}
      </>
    )
  }

  function CorrelazioniGiornoFascia(props){
    const {correlazioni, giorno, docUnavailable} = props

    let res_green = []
    let res_red = []
    let res_orange = []
    console.log(docUnavailable)
    if(docUnavailable){
      res_red.push("DOCENTE NON DISPONBIILE ")
    }
    else{
      for (let el of correlazioni) {
        if (el.corr !== 0){
          if(el.corr < 40)
            res_green.push(el.titolo.toString() + "  " + el.corr.toString())
          else if(el.corr < 80)
            res_orange.push(el.titolo.toString() + "  " + el.corr.toString())
          else
            res_red.push(el.titolo.toString() + "  " + el.corr.toString())
        }
      }
    }
    let bg = ""
    if(res_red.length > 0 )
      bg = "bg-danger"
    else if(res_orange.length > 0)
      bg = "bg-warning"
    else
      bg = "bg-success"
    

    return (
      <td className={bg}>
        
        {res_red.map((r) => <h6>
                          <Badge className="bg-light">
                            {r}
                          </Badge>
                        </h6>)}
        {res_orange.map((r) => <h6>
                          <Badge className="bg-light">
                            {r}
                          </Badge>
                        </h6>)}
        {res_green.map((r) => <h6>
                          <Badge className="bg-light">
                            {r}
                          </Badge>
                        </h6>)}
      </td>
    )
  }

  function ListCorrelazioni(props) {
    const {correlazioni, giorni, otherSlotDocente} = props
    return (
      <>
        {giorni.map((giorno) => <CorrelazioniGiornoFascia correlazioni={correlazioni.hasOwnProperty(giorno) ? correlazioni[giorno].sort((a,b) => b.corr - a.corr) : []} giorno={giorno} docUnavailable={otherSlotDocente.hasOwnProperty(giorno) ? otherSlotDocente[giorno] : false}></CorrelazioniGiornoFascia>)}
      </>
    )
  }


function TableOrario(props) {
  const { loading, listSlot, periodoDidattico, currPianoAllocazione, fasceOrarie, giorni, currInsegnamento, listInfoCorr, fullListSlot, fullListInsegnamenti} = props;

  if (listSlot.length === 0 || currPianoAllocazione === EMPTY_VALUE || fasceOrarie.length === 0 || currInsegnamento === EMPTY_VALUE) {
    return <span>⚠️ Dati mancanti... ⚠️</span>
  }

  let res = {};
  fasceOrarie.forEach(fascia => {
    res[fascia] = listSlot
      .filter((slot) => (slot.fasciaOraria === fascia) && (slot.ID_INC === currInsegnamento.ID_INC))
      .reduce((group, slot) => {
        const { giorno } = slot;
        group[giorno] = group[giorno] ?? [];
        group[giorno].push(slot);
        return group;
      }, {});
  });

  let correlazioni = {};
  let otherSlotDocente = {};
  let currListInfoCorr = listInfoCorr.filter((infoCorr) => (infoCorr.ID_INC_1 === currInsegnamento.ID_INC) || (infoCorr.ID_INC_2 === currInsegnamento.ID_INC))
  fasceOrarie.forEach(fascia => {
    console.log(otherSlotDocente)
    correlazioni[fascia] = {}
    otherSlotDocente[fascia] = {}
    giorni.forEach((giorno) => {
      correlazioni[fascia][giorno] = []
      otherSlotDocente[fascia][giorno] = false
      let slotsSameFasciaOra = fullListSlot
      .filter((slot) => (slot.fasciaOraria === fascia) && (slot.giorno === giorno) && (slot.ID_INC !== currInsegnamento.ID_INC))

      let ids_with_corr = slotsSameFasciaOra
      .map((slot) => slot.ID_INC)

      slotsSameFasciaOra.forEach((slot) => {
        if(slot.listDocenti.includes(currInsegnamento.titolare)){
          otherSlotDocente[fascia][giorno] = true
        }
      })
      
      ids_with_corr.forEach((id) => {
          for (let infoCorr of currListInfoCorr) {
            if((infoCorr.ID_INC_1 === id) || (infoCorr.ID_INC_2 === id)) {
              let ins = fullListInsegnamenti.filter((ins) => ins.ID_INC === id)
              let newDict = {
                "otherId": id,
                "corr": infoCorr.correlazione,
                "titolo": ins.length !== 0 ? ins[0].titolo : "No titolo"
              }
              correlazioni[fascia][giorno].push(newDict)
              break
            }
          }
      })
    })
  });

  

  return (
    <>
      {loading ? <span>🕗 Please wait, loading Piano allocazione... 🕗</span> :
        <Container fluid>
            <Table>
                <thead>
                    <th>{currPianoAllocazione}</th>
                    <th>Lunedì</th>
                    <th>Martedì</th>
                    <th>Mercoledì</th>
                    <th>Giovedì</th>
                    <th>Venerdì</th>
                </thead>
                <tbody>
                    <tr>
                        <td>8.30-10.00</td>
                        <SlotsFasciaOraria slots={res.hasOwnProperty("8.30-10.00") ? res["8.30-10.00"] : {}} giorni={giorni} />
                    </tr>
                    <tr>
                        <td>10.00-11.30</td>
                        <SlotsFasciaOraria slots={res.hasOwnProperty("10.00-11.30") ? res["10.00-11.30"] : {}} giorni={giorni} />
                    </tr>
                    <tr>
                        <td>11.30-13.00</td>
                        <SlotsFasciaOraria slots={res.hasOwnProperty("11.30-13.00") ? res["11.30-13.00"] : {}} giorni={giorni} />
                    </tr>
                    <tr>
                        <td>13.00-14.30</td>
                        <SlotsFasciaOraria slots={res.hasOwnProperty("13.00-14.30") ? res["13.00-14.30"] : {}} giorni={giorni} />
                    </tr>
                    <tr>
                        <td>14.30-16.00</td>
                        <SlotsFasciaOraria slots={res.hasOwnProperty("14.30-16.00") ? res["14.30-16.00"] : {}} giorni={giorni} />
                    </tr>
                    <tr>
                        <td>16.00-17.30</td>
                        <SlotsFasciaOraria slots={res.hasOwnProperty("16.00-17.30") ? res["16.00-17.30"] : {}} giorni={giorni} />
                    </tr>
                    <tr>
                        <td>17.30-19.00</td>
                        <SlotsFasciaOraria slots={res.hasOwnProperty("17.30-19.00") ? res["17.30-19.00"] : {}} giorni={giorni} />
                    </tr>
                </tbody>
            </Table>
            <Table className='mt-4'>
                <thead>
                    <th>{currPianoAllocazione}</th>
                    <th>Lunedì</th>
                    <th>Martedì</th>
                    <th>Mercoledì</th>
                    <th>Giovedì</th>
                    <th>Venerdì</th>
                </thead>
                <tbody>
                    <tr>
                        <td>8.30-10.00</td>
                        <ListCorrelazioni correlazioni={correlazioni.hasOwnProperty("8.30-10.00") ? correlazioni["8.30-10.00"] : {}} giorni={giorni} otherSlotDocente={otherSlotDocente.hasOwnProperty("8.30-10.00") ? otherSlotDocente["8.30-10.00"] : {}} />
                    </tr>
                    <tr>
                        <td>10.00-11.30</td>
                        <ListCorrelazioni correlazioni={correlazioni.hasOwnProperty("10.00-11.30") ? correlazioni["10.00-11.30"] : {}} giorni={giorni} otherSlotDocente={otherSlotDocente.hasOwnProperty("10.00-11.30") ? otherSlotDocente["10.00-11.30"] : {}}/>
                    </tr>
                    <tr>
                        <td>11.30-13.00</td>
                        <ListCorrelazioni correlazioni={correlazioni.hasOwnProperty("11.30-13.00") ? correlazioni["11.30-13.00"] : {}} giorni={giorni} otherSlotDocente={otherSlotDocente.hasOwnProperty("11.30-13.00") ? otherSlotDocente["11.30-13.00"] : {}}/>
                    </tr>
                    <tr>
                        <td>13.00-14.30</td>
                        <ListCorrelazioni correlazioni={correlazioni.hasOwnProperty("13.00-14.30") ? correlazioni["13.00-14.30"] : {}} giorni={giorni} otherSlotDocente={otherSlotDocente.hasOwnProperty("13.00-14.30") ? otherSlotDocente["13.00-14.30"] : {}}/>
                    </tr>
                    <tr>
                        <td>14.30-16.00</td>
                        <ListCorrelazioni correlazioni={correlazioni.hasOwnProperty("14.30-16.00") ? correlazioni["14.30-16.00"] : {}} giorni={giorni} otherSlotDocente={otherSlotDocente.hasOwnProperty("14.30-16.00") ? otherSlotDocente["14.30-16.00"] : {}}/>
                    </tr>
                    <tr>
                        <td>16.00-17.30</td>
                        <ListCorrelazioni correlazioni={correlazioni.hasOwnProperty("16.00-17.30") ? correlazioni["16.00-17.30"] : {}} giorni={giorni} otherSlotDocente={otherSlotDocente.hasOwnProperty("16.00-17.30") ? otherSlotDocente["16.00-17.30"] : {}}/>
                    </tr>
                    <tr>
                        <td>17.30-19.00</td>
                        <ListCorrelazioni correlazioni={correlazioni.hasOwnProperty("17.30-19.00") ? correlazioni["17.30-19.00"] : {}} giorni={giorni} otherSlotDocente={otherSlotDocente.hasOwnProperty("17.30-19.00") ? otherSlotDocente["17.30-19.00"] : {}}/>
                    </tr>
                </tbody>
            </Table>
        </Container>
      }</>
  )
}



function SovrapposizioniComponent(props) {
    const { loading, listCdl, tipoCdl, setTipoCdl, currCdl, setCurrCdl, currOrientamento, listOrientamenti, setCurrOrientamento,
      periodoDidattico, setPeriodoDidattico, listSlot, listPianiAllocazione, currPianoAllocazione, setCurrPianoAllocazione,
      fasceOrarie, giorni, listInsegnamenti, currInsegnamento, setCurrInsegnamento, listInfoCorr, fullListSlot, fullListInsegnamenti} = props;
  
    return (
      <>
        {loading ?
          <span>🕗 Please wait, loading Slot... 🕗</span> :
          <Container fluid className='mt-1'>
            <Row className='mt-2'>
              <Col xs={1}>Piano allocazione:</Col>
              <Col>
                <Dropdown>
                  <Dropdown.Toggle variant="primary" id="dropdown-basic">
                    {currPianoAllocazione}
                  </Dropdown.Toggle>
                  <Dropdown.Menu>
                    {listPianiAllocazione.map((pianoAlloc, index) => <Dropdown.Item key={index} onClick={e => setCurrPianoAllocazione(listPianiAllocazione[index].pianoAllocazione)}>{pianoAlloc.pianoAllocazione}</Dropdown.Item>)}
                  </Dropdown.Menu>
                </Dropdown>
              </Col>
            </Row>
            <Row className='mt-3'>
              <Col xs={2}>Tipo CDL</Col>
              <Col>Nome CDL</Col>
            </Row>
            <Row>
              <Col xs={2}>
                <Dropdown>
                  <Dropdown.Toggle variant="secondary" id="dropdown-basic">
                    {tipoCdl}
                  </Dropdown.Toggle>
                  <Dropdown.Menu>
                    <Dropdown.Item key={0} onClick={e => setTipoCdl("Z")}>{"Z"}</Dropdown.Item>
                    <Dropdown.Item key={1} onClick={e => setTipoCdl("1")}>{"1"}</Dropdown.Item>
                  </Dropdown.Menu>
                </Dropdown>
              </Col>
              <Col>
                <Dropdown>
                  <Dropdown.Toggle variant="secondary" id="dropdown-basic">
                    {currCdl}
                  </Dropdown.Toggle>
                  <Dropdown.Menu>
                    {listCdl.map((cdl, index) => <Dropdown.Item key={index} onClick={e => setCurrCdl(listCdl[index].nomeCdl)}>{cdl.nomeCdl}</Dropdown.Item>)}
                  </Dropdown.Menu>
                </Dropdown>
              </Col>
            </Row>
            <Row className='mt-2'>
              <Col xs={2}>Periodo didattico</Col>
              <Col>Orientamento</Col>
            </Row>
            <Row>
              <Col xs={2}>
                <Dropdown>
                  <Dropdown.Toggle variant="secondary" id="dropdown-basic">
                    {periodoDidattico}
                  </Dropdown.Toggle>
                  <Dropdown.Menu>
                    <Dropdown.Item key={0} onClick={e => setPeriodoDidattico("1-1")}>{"1-1"}</Dropdown.Item>
                    <Dropdown.Item key={1} onClick={e => setPeriodoDidattico("2-1")}>{"2-1"}</Dropdown.Item>
                    {tipoCdl === "1" ?
                      <Dropdown.Item key={2} onClick={e => setPeriodoDidattico("3-1")}>{"3-1"}</Dropdown.Item> : <></>}
                  </Dropdown.Menu>
                </Dropdown>
              </Col>
              <Col>
                <Dropdown>
                  <Dropdown.Toggle variant="secondary">
                    {currOrientamento}
                  </Dropdown.Toggle>
                  <Dropdown.Menu>
                    {listOrientamenti.map((orient, index) => <Dropdown.Item key={index} onClick={e => setCurrOrientamento(listOrientamenti[index].orientamento)}>{orient.orientamento}</Dropdown.Item>)}
                  </Dropdown.Menu>
                </Dropdown>
              </Col>
            </Row>
            <Row className='mt-2'>
              <Col xs={2}>Insegnamento</Col>
            </Row>
            <Row>
                <Col xs={2}>
                    <Dropdown>
                        <Dropdown.Toggle variant="secondary">
                        {currInsegnamento.titolo}
                        </Dropdown.Toggle>
                        <Dropdown.Menu className='mb-5'>
                        {listInsegnamenti.map((ins, index) => <Dropdown.Item key={index} onClick={e => setCurrInsegnamento(ins)}>{ins.titolo}</Dropdown.Item>)}
                        </Dropdown.Menu>
                    </Dropdown>
                </Col>
            </Row>
            <Row className='mt-4'>
                <TableOrario loading={loading} listSlot={listSlot} periodoDidattico={periodoDidattico} currPianoAllocazione={currPianoAllocazione}
                fasceOrarie={fasceOrarie} giorni={giorni} currInsegnamento={currInsegnamento} listInfoCorr={listInfoCorr} fullListSlot={fullListSlot} fullListInsegnamenti={fullListInsegnamenti}/>
            </Row>
          </Container>
        }
      </>
    );
  }
  
  export default SovrapposizioniComponent;