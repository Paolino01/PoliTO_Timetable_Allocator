import { Row, Table, Dropdown, Container, Col, Badge, Popover, OverlayTrigger, FormControl } from 'react-bootstrap';
import React, { useState } from 'react';

const EMPTY_VALUE = "sconosciuto";
const LEN_TITOLO = 18;


function Slot(props) {
  const { slot, giorno } = props;

  const strDoc = slot.listDocenti.reduce((prev, doc) => prev.concat(", ", doc));

  const popover = (
    <Popover>
      <Popover.Title as='h6'>{slot.insegnamento.titolo}
      </Popover.Title>
      <Popover.Content>
        {"Docenti: " + strDoc}<br></br>
        {"Studenti: " + slot.insegnamento.nStudentiFreq}<br></br>
        {"Tipo lezione: " + slot.tipoLez}<br></br>
        {slot.tipoErogazione === "Presenza" ? "Tipo locale: " + slot.tipoLocale : "Erogazione in remoto"}
      </Popover.Content>
    </Popover>
  );

  return (
    <OverlayTrigger placement={giorno !== 'Ven' ? 'right' : 'left'} trigger='click' delay={{ show: 250, hide: 300 }} overlay={popover}>
      <Badge className='bg-danger text-light ml-1 mt-1'>
        {(slot.insegnamento.titolo.length > LEN_TITOLO ? slot.insegnamento.titolo.substring(0, LEN_TITOLO) : slot.insegnamento.titolo) + " " + slot.idSlot}
      </Badge>
    </OverlayTrigger>
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

function TableDocente(props) {
  const { loading, listSlot, periodoDidattico, currPianoAllocazione, currDocente, fasceOrarie, giorni } = props;

  if (listSlot.length === 0 || periodoDidattico === EMPTY_VALUE || currPianoAllocazione === EMPTY_VALUE || fasceOrarie.length === 0) {
    return <span>⚠️ Dati mancanti... ⚠️</span>
  }

  let res = {};
  fasceOrarie.forEach(fascia => {
    res[fascia] = listSlot
      .filter((slot) => slot.fasciaOraria === fascia)
      .reduce((group, slot) => {
        const { giorno } = slot;
        group[giorno] = group[giorno] ?? [];
        group[giorno].push(slot);
        return group;
      }, {});
  });

  return (
    <>
      {loading ? <span>🕗 Please wait, loading Orario docente... 🕗</span> :
        <Table>
          <thead>
            <th>{"Orario " + currDocente}</th>
            <th>Lunedì</th>
            <th>Martedì</th>
            <th>Mercoledì</th>
            <th>Giovedì</th>
            <th>Vernerdì</th>
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
      }</>
  )
}

// Component with the menu to choose the orientation and the other options
function DocentiComponent(props) {
  const { loading, listSlot, listPianiAllocazione, currPianoAllocazione, setCurrPianoAllocazione, currDocente, setCurrDocente, listDocenti,
    fasceOrarie, giorni } = props;

  // https://react-bootstrap.github.io/components/dropdowns/
  // forwardRef again here!
  // Dropdown needs access to the DOM of the Menu to measure it
  const CustomMenu = React.forwardRef(
    ({ children, style, className, 'aria-labelledby': labeledBy }, ref) => {
      const [value, setValue] = useState('');

      return (
        <div
          ref={ref}
          style={style}
          className={className}
          aria-labelledby={labeledBy}
        >
          <FormControl
            autoFocus
            className="mx-3 my-2 w-auto"
            placeholder="Type to filter..."
            onChange={(e) => setValue(e.target.value)}
            value={value}
          />
          <ul className="list-unstyled">
            {React.Children.toArray(children).filter(
              (child) =>
                !value || child.props.children.toLowerCase().startsWith(value.toLowerCase()),
            )}
          </ul>
        </div>
      );
    },
  );

  return (
    <>
      {loading ?
        <span>🕗 Please wait, loading Docenti... 🕗</span> :
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
            <Col xs={2}>Docente: </Col>
          </Row>
          <Row>
            <Col xs={2}>
              <Dropdown>
                <Dropdown.Toggle variant="secondary" id="dropdown-basic">
                  {currDocente}
                </Dropdown.Toggle>
                <Dropdown.Menu as={CustomMenu}>
                  {listDocenti.map((docente, index) => <Dropdown.Item key={index} onClick={e => setCurrDocente(listDocenti[index].Cognome)}>{docente.Cognome}</Dropdown.Item>)}
                </Dropdown.Menu>
              </Dropdown>
            </Col>
          </Row>
          <Row className='mt-4'>
            <TableDocente loading={loading} listSlot={listSlot} currPianoAllocazione={currPianoAllocazione} currDocente={currDocente}
              fasceOrarie={fasceOrarie} giorni={giorni} />
          </Row>
        </Container>
      }
    </>
  );
}

export default DocentiComponent;