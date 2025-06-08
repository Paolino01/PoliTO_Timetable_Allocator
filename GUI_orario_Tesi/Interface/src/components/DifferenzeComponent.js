import { Row, Table, Dropdown, Container, Col, Badge, Popover, OverlayTrigger, Tooltip } from 'react-bootstrap';

const EMPTY_VALUE = "sconosciuto";
const LEN_TITOLO = 18;

function Slot(props) {
    const { slot, giorno, color } = props;
    console.log(slot)
    console.log(color)
  
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
          <Badge className={'text-light ' + color}>
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
    const { slots, slotsOtherTimetable, giorno} = props;
  
    return (
      <td>
        {slots.map((slot) => <Slot slot={slot} giorno={giorno} color="bg-danger"></Slot>)}
        {slotsOtherTimetable.map((slot) => <Slot slot={slot} giorno={giorno} color={"bg-warning"}></Slot>)}
      </td>
    )
  }
  
  
  function SlotsFasciaOraria(props) {
    const { slots, slotsOtherTimetable, giorni } = props;
  
    return (
      <>
        {giorni.map((giorno) => 
          <>
            <SlotMerged slots={slots.hasOwnProperty(giorno) ? slots[giorno] : []} slotsOtherTimetable={slotsOtherTimetable.hasOwnProperty(giorno) ? slotsOtherTimetable[giorno] : []} giorno={giorno} />
          </>
        )}
      </>
    )
  }


function TableOrario(props) {
  const { loading, listSlot, listSlotOtherTimetable, currPianoAllocazione, fasceOrarie, giorni, currInsegnamento} = props;

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

  let resOtherTimetable = {};
  fasceOrarie.forEach(fascia => {
    resOtherTimetable[fascia] = listSlotOtherTimetable
      .filter((slot) => (slot.fasciaOraria === fascia) && (slot.ID_INC === currInsegnamento.ID_INC))
      .reduce((group, slot) => {
        const { giorno } = slot;
        group[giorno] = group[giorno] ?? [];
        group[giorno].push(slot);
        return group;
      }, {});
  });

  return (
    <>
      {loading ? <span>🕗 Please wait, loading Piano allocazione... 🕗</span> :
        <Container fluid>
            <div>
              <div>
                <span className='bg-warning py-1 px-2 rounded-pill text-white font-weight-bold'>Yellow</span> previous timetable
              </div>
              <div className='my-3'>
                <span className='bg-danger py-1 px-2 rounded-pill text-white font-weight-bold'>Red</span> this timetable
              </div>
            </div>
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
                        <SlotsFasciaOraria slots={res.hasOwnProperty("8.30-10.00") ? res["8.30-10.00"] : {}} giorni={giorni}
                          slotsOtherTimetable={resOtherTimetable.hasOwnProperty("8.30-10.00") ? resOtherTimetable["8.30-10.00"] : {}} />
                    </tr>
                    <tr>
                        <td>10.00-11.30</td>
                        <SlotsFasciaOraria slots={res.hasOwnProperty("10.00-11.30") ? res["10.00-11.30"] : {}} giorni={giorni}
                          slotsOtherTimetable={resOtherTimetable.hasOwnProperty("10.00-11.30") ? resOtherTimetable["10.00-11.30"] : {}} />
                    </tr>
                    <tr>
                        <td>11.30-13.00</td>
                        <SlotsFasciaOraria slots={res.hasOwnProperty("11.30-13.00") ? res["11.30-13.00"] : {}} giorni={giorni}
                          slotsOtherTimetable={resOtherTimetable.hasOwnProperty("11.30-13.00") ? resOtherTimetable["11.30-13.00"] : {}} />
                    </tr>
                    <tr>
                        <td>13.00-14.30</td>
                        <SlotsFasciaOraria slots={res.hasOwnProperty("13.00-14.30") ? res["13.00-14.30"] : {}} giorni={giorni}
                          slotsOtherTimetable={resOtherTimetable.hasOwnProperty("13.00-14.30") ? resOtherTimetable["13.00-14.30"] : {}} />
                    </tr>
                    <tr>
                        <td>14.30-16.00</td>
                        <SlotsFasciaOraria slots={res.hasOwnProperty("14.30-16.00") ? res["14.30-16.00"] : {}} giorni={giorni}
                          slotsOtherTimetable={resOtherTimetable.hasOwnProperty("14.30-16.00") ? resOtherTimetable["14.30-16.00"] : {}} />
                    </tr>
                    <tr>
                        <td>16.00-17.30</td>
                        <SlotsFasciaOraria slots={res.hasOwnProperty("16.00-17.30") ? res["16.00-17.30"] : {}} giorni={giorni}
                          slotsOtherTimetable={resOtherTimetable.hasOwnProperty("16.00-17.30") ? resOtherTimetable["16.00-17.30"] : {}} />
                    </tr>
                    <tr>
                        <td>17.30-19.00</td>
                        <SlotsFasciaOraria slots={res.hasOwnProperty("17.30-19.00") ? res["17.30-19.00"] : {}} giorni={giorni}
                          slotsOtherTimetable={resOtherTimetable.hasOwnProperty("17.30-19.00") ? resOtherTimetable["17.30-19.00"] : {}} />
                    </tr>
                </tbody>
            </Table>
        </Container>
      }</>
  )
}



function DifferenzeComponent(props) {
    const { loading, listCdl, tipoCdl, setTipoCdl, currCdl, setCurrCdl, currOrientamento, listOrientamenti, setCurrOrientamento,
      periodoDidattico, setPeriodoDidattico, listSlot, listSlotOtherTimetable, listPianiAllocazione, currPianoAllocazione, setCurrPianoAllocazione,
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
                <TableOrario loading={loading} listSlot={listSlot} listSlotOtherTimetable={listSlotOtherTimetable} currPianoAllocazione={currPianoAllocazione}
                fasceOrarie={fasceOrarie} giorni={giorni} currInsegnamento={currInsegnamento} listInfoCorr={listInfoCorr} fullListSlot={fullListSlot} fullListInsegnamenti={fullListInsegnamenti}/>
            </Row>
          </Container>
        }
      </>
    );
  }
  
  export default DifferenzeComponent;