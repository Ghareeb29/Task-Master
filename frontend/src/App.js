import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginRegister from "./components/loginRegister/loginRegister";
import Dash from "./components/dash/dash";
import Alltasks from './components/dash/alltasks';
import ImportantTasks from './components/dash/importantTasks';




function App() {
  return (
    <div className='relative'>
      <Router>
      <Routes>
        <Route path="/" element={<LoginRegister />} />
        <Route path="/dash" element={<Dash />}>
          <Route path="alltasks" element={<Alltasks />} />
          <Route path="importantTasks" element={<ImportantTasks />} />
        </Route>
      </Routes>
    </Router>
    </div>
    
  );
};

export default App;
