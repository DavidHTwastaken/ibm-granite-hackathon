import {HashRouter as Router, Route, Routes} from "react-router-dom";
import Main from "./Pages/Main";
import About from "./Pages/About";
import { Navbar } from "./Components/Navbar";

function App() {

  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Main/>} />
        <Route path="/about" element={<About/>} />
      </Routes>
    </Router>
  );
}

export default App; 