import {HashRouter as Router, Route, Routes} from "react-router-dom";
import { Main } from "./Pages/Main";
import { About } from "./Pages/About";
function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Main/>} />
        <Route path="/about" element={<About/>} />
      </Routes>
    </Router>
  );
}

export default App; 