import { Row, Table, Dropdown, Container, Col } from 'react-bootstrap';



function Insegnamento(props) {
  const { ins } = props;

  return (
    <tr>
      <td>{ins.ID_INC}</td>
      <td>{ins.titolo}</td>
      <td>{ins.CFU}</td>
      <td>{ins.titolare}</td>
      <td>{ins.nStudenti}</td>
      <td>{ins.tipoInsegnamento}</td>
      <td>{ins.alfabetica}</td>
    </tr>
  )
}

function InsegnamentiTable(props) {
  const { loading, listInsegnamenti, periodoDidattico } = props;

  return (
    <>
      {loading ? <span>🕗 Please wait, loading Insegnamenti Table... 🕗</span> :
        <Table>
          <thead>
            <th>ID_INC</th>
            <th>Titolo</th>
            <th>CFU</th>
            <th>Titolare</th>
            <th>Numero iscritti</th>
            <th>Tipo insegnamento</th>
            <th>Alfabetica</th>
          </thead>
          <tbody>
            {listInsegnamenti.filter((ins) => ins.periodoDidattico === periodoDidattico).map((ins) => <Insegnamento ins={ins}></Insegnamento>)}
          </tbody>
        </Table>
      }</>
  )
}

// Component with the menu to choose the orientation and the other options
function InsegnamentiComponent(props) {
  const { loading, listCdl, tipoCdl, setTipoCdl, currCdl, setCurrCdl, currOrientamento, listOrientamenti, setCurrOrientamento,
    listInsegnamenti, periodoDidattico, setPeriodoDidattico } = props;

  return (
    <>
      {loading ?
        <span>🕗 Please wait, loading Insegnamenti... 🕗</span> :
        <Container fluid className='mt-1'>
          <Row>
            <Col xs={2}>Tipo CDL</Col>
            <Col>Nome CDL</Col>
          </Row>
          <Row>
            <Col xs={2}>
              <Dropdown>
                <Dropdown.Toggle variant="primary" id="dropdown-basic">
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
                <Dropdown.Toggle variant="primary" id="dropdown-basic">
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
                <Dropdown.Toggle variant="primary" id="dropdown-basic">
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
          <Row className='mt-4'>
            <InsegnamentiTable loading={loading} listInsegnamenti={listInsegnamenti} periodoDidattico={periodoDidattico} />
          </Row>
        </Container>
      }
    </>
  );
}

export default InsegnamentiComponent;