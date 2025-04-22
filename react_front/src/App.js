
import './App.css';
import{BrowserRouter as Router ,Routes ,Route}from "react-router-dom"
import Login from './routes/login';
import Movies from './routes/movies';
function App() {
  return (
    <Router>
      <Routes>
        <Route path='/login' element={<Login/>}/>
        <Route path='/movies' element={<Movies/>}/>
      </Routes>
    </Router>
  );
}

export default App;
