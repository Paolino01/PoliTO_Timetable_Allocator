import { Navbar, Nav } from 'react-bootstrap/';
import { NavLink } from 'react-router-dom';



const Navigation = (props) => {
  const { setMoving } = props;

  return (
    <Navbar bg="info" variant="dark">
      <Navbar.Toggle aria-controls="left-sidebar" />
      <Navbar.Brand href="/">
        Orario
      </Navbar.Brand>

      <Nav className="mr-auto">
        <Nav.Link as={NavLink} to="/pianoAllocazione" onClick={() => setMoving((old) => !old)}>Piano allocazione</Nav.Link>
        <Nav.Link as={NavLink} to="/insegnamenti" onClick={() => setMoving((old) => !old)}>Insegnamenti</Nav.Link>
        <Nav.Link as={NavLink} to="/docenti" onClick={() => setMoving((old) => !old)}>Docenti</Nav.Link>
        <Nav.Link as={NavLink} to="/sovrapposizioni" onClick={() => setMoving((old) => !old)}>Sovrapposizioni</Nav.Link>
        <Nav.Link as={NavLink} to="/differenze_orario" onClick={() => setMoving((old) => !old)}>Differenze orario</Nav.Link>
      </Nav>

    </Navbar>
  )
}

export default Navigation;