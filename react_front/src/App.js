
import './App.css';
import{BrowserRouter as Router ,Routes ,Route}from "react-router-dom"
import Login from './routes/login';
import Movies from './routes/movies';
import Detail from './routes/detail';
import { ChakraProvider } from '@chakra-ui/react';
function App() {
  return (
    <ChakraProvider>
      <Router>
        <Routes>
          <Route path='/login' element={<Login/>}/>
          <Route path='/movies' element={<Movies/>}/>
          <Route path='/movies/:movieID' element={<Detail/>}/>
        </Routes>
      </Router>
    </ChakraProvider>

  );
}

export default App;
