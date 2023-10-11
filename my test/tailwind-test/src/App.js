import {BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Layout from "./components/shared/Maga";
import Dashboard from "./components/Dashboard";
import ProjectsSelector from "./components/ProjectsSelector";
import CreateDevice from "./components/CreateDevice";

function App() {
  return (
<Router>
  <Routes>
    <Route path="/" element={<ProjectsSelector/>}>
      <Route index element={<ProjectsSelector/>}/>
      {/* <Route path="dashboard" element={<Dashboard/>}/> */}
    </Route>
    <Route path="/projects" element={<ProjectsSelector/>} />
    <Route path="/maga" element={<Layout/>} />
    <Route path="/createdevice" element={<CreateDevice/>} />
  </Routes>
</Router>    
  );
}

export default App;
