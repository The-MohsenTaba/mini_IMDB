import axios from 'axios'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
const BASE_URL = "http://127.0.0.1:8000/"
const LOGIN_URL = "http://localhost:8000/api/token/"
const REFRESH_URL = `${LOGIN_URL}refresh/`
const LOGOUT_URL = "http://127.0.0.1:8000/logout/"
const MY_VOTES = "http://127.0.0.1:8000/my-votes/"
const AUTH_URL = "http://127.0.0.1:8000/authenticated"

axios.defaults.withCredentials = true;



export const is_authenticated = async ()=>{


    const response = await axios.get("http://localhost:8000/authenticated",
        {withCredentials:true}
    );
    console.log("data",response.data)
    return response.data
};

export const login = async (username , password)=> {
    


    const response = await axios.post(LOGIN_URL,
        {username:username , password:password},
        {withCredentials:true}
    )
    return(
        response.data.success
    )


}

export const refresh_token = async()=> {
    await axios.post(REFRESH_URL,
        {},
        {withCredentials:true}
    )
    return true
}

const call_refresh = async(error,func) => {
    if(error.response && error.response.status === 401){
        const tokenRefreshed = await refresh_token();
        if (tokenRefreshed){
            const retryResponse = await func();
            return retryResponse.data
        }
    }
    return false
}

export const post_vote = async(rating)=>{
    try {
        const response = await axios.post(
            "http://localhost:8000/movies/:movieID",
            {"rating":rating},
            {withCredentials:true}
        )
        return response.data
    }catch(error){
        return call_refresh(error,
            axios.post("http://localhost:8000/movies/:movieID",{"rating":rating},{withCredentials:true}
        ))
    }
}

export const register = async (username, password) => {
    const response = await axios.post("http://localhost:8000/sign-up/", {username,password}, { withCredentials: true });
    return response.data;
};


export const logout = async () => {
    try {
        // First make a GET request to ensure cookies are set
        await axios.get('http://localhost:8000/', { withCredentials: true });
        
        // Then make the logout request
        const response = await axios.post(
            'http://localhost:8000/logout/',
            {},
            {
                withCredentials: true,
                headers: {
                    'Content-Type': 'application/json',
                }
            }
        );
        return response.data.success;
    } catch (error) {
        console.error('Logout error:', error);
        return false;
    }
};