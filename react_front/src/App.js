
import './App.css';
import{BrowserRouter as Router ,Routes ,Route}from "react-router-dom"
import Login from './routes/login';
import Movies from './routes/movies';
import Detail from './routes/detail';
import Votes from './routes/myvotes';
import Register from './routes/sign-up';
import { ChakraProvider } from '@chakra-ui/react';
import { AuthProvider } from './contexts/useAuth';
import PrivateRoute from './components/private_route';

function App() {
  return (
    <ChakraProvider>
      <Router>
        <AuthProvider>
          <Routes>
            <Route path='/login' element={<Login/>}/>
            <Route path='/movies' element={<Movies/>}/>
            <Route path='/movies/:movieID' element={<Detail/>}/>
            <Route path='/sign-up' element={<Register/>}/>
            <Route path='/my-ratings' element={<PrivateRoute><Votes/></PrivateRoute>}/>
          </Routes>
        </AuthProvider>
      </Router>
    </ChakraProvider>

  );
}

export default App;
