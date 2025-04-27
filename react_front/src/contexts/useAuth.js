import { useContext,createContext,Children, useEffect, useState } from "react";
import { is_authenticated } from "../endpoints/api";
import {useNavigate} from 'react-router-dom';
import { register , login} from "../endpoints/api";


const AuthContext = createContext();

export const AuthProvider= ({children}) => {

    const [user,setUser]=useState(null);
    const [isAuthenticated,setIsAuthenticated]=useState(false);
    const [loading,setLoading] = useState(true);
    const nav = useNavigate();


    const get_authenticated= async ()=> {
        try{
            const authData = await is_authenticated();
            console.log("Authdata:" ,authData.username)
            console.log("type:",typeof authData.username)
            if (authData.username !="") {
                setUser(authData.username);
                setIsAuthenticated(true);
            } else {
                setUser("");
                setIsAuthenticated(false);
            }
            if (authData.username ===""){
                setUser("");
                setIsAuthenticated(false);
            }
        } catch (error) {
            setUser(null);
            setIsAuthenticated(false);
        } finally {
            setLoading(false);
        }

        console.log("fianl",user)
    };


    const loginUser = async (username, password) => {
        const user = await login(username, password)
        if (user) {
          setUser(user)
          nav('../movies')
        } else {
          alert('Incorrect username or password')
        }
    }

    const registerUser = async (username, password, confirm_password) => {
        try {
          if (password === confirm_password) {
            await register(username, password)
            alert('User successfully registered')
            nav('/login')
          }
        } catch {
          alert('error registering user')
        }
      }


    useEffect(()=>{
        get_authenticated();
    },[window.location.pathname])
    return(
        <AuthContext.Provider value={{user,isAuthenticated,loading,get_authenticated,registerUser,loginUser}}>
            {children}
        </AuthContext.Provider>
    )
}

export const useAuth = () => useContext(AuthContext);